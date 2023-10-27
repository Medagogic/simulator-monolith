from typing import Any, Dict, List
from pydantic import BaseModel
from packages.server.sim_app.medsim import Router_MedSim, Session_MedSim
import json
import os
from pathlib import Path
import re
from packages.tools.scribe import ScribeEmitSchema, ScribeHandlerSchema
from packages.tools.scribe.src.scribe_helpers import get_field_info
import asyncio
import shutil

def generate_code(verbose=False) -> None:
    this_file = Path(os.path.realpath(__file__))
    this_dir = this_file.parent
    schema_dir = f"{this_dir}/schemas"
    generated_dir = f"{this_dir}/generated"

    if os.path.exists(schema_dir):
        shutil.rmtree(schema_dir)
    os.mkdir(schema_dir)

    if os.path.exists(generated_dir):
        shutil.rmtree(generated_dir)
    os.mkdir(generated_dir)

    emitted_events: List[ScribeEmitSchema] = Router_MedSim.scribe_get_all_emitted_events(Session_MedSim)
    handled_events: List[ScribeHandlerSchema] = Router_MedSim.scribe_get_all_handled_events(Session_MedSim)

    schema_properties: Dict[str, Dict] = {}

    for event_data in emitted_events:
        if event_data.data_type is not None and issubclass(event_data.data_type, BaseModel):
            schema = event_data.data_type.model_json_schema()
            filename = f"{schema['title']}.schema.json"
            schema["$id"] = filename
            schema["additionalProperties"] = False
            with open(f"{schema_dir}/{filename}", "w") as f:
                json.dump(schema, f, indent=4)
            schema_properties[event_data.emits_event] = {"$ref": f"schemas/{filename}"}
        else:
            schema_properties[event_data.emits_event] = get_field_info(event_data.data_schema)



    for handler_data in handled_events:
        arg_dict: Dict[str, Any] = handler_data.data_type

        properties_dict: Dict[str, Any] = {}

        for argid, argtype in arg_dict.items():
            if argtype is not None and issubclass(argtype, BaseModel):
                schema = argtype.model_json_schema()
                filename = f"{schema['title']}.schema.json"
                schema["$id"] = filename
                schema["additionalProperties"] = False
                with open(f"{schema_dir}/{filename}", "w") as f:
                    json.dump(schema, f, indent=4)
                
                arg_props = {"$ref": f"schemas/{filename}"}
            else:
                arg_props = get_field_info(handler_data.data_schema)
            
            properties_dict[argid] = arg_props
        
        name_for_schema = f"__server_{handler_data.handler_name}"
        schema_properties[name_for_schema] = {
            "type": "object",
            "properties": properties_dict,
            "additionalProperties": False,
        }

    emitted_event_names = [event_data.emits_event for event_data in emitted_events]

    schema_dict = {
        "$id": "Scribe Events",
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": schema_properties,
        "additionalProperties": False,
        "required": emitted_event_names
    }

    with open(f"{schema_dir}/scribe.schema.json", "w") as f:
        json.dump(schema_dict, f, indent=4)

    # run generate_events.sh
    import subprocess
    subprocess.run(["bash", f"{this_dir}/generate_events.sh"])

    prompt = """
Create an abstract typescript class `ScribeClient` which provides virtual functions for each element in ScribeEvents, with a single paramater "data" of the associated type. Do not provide any surrounding text, provide only the code.

For example:
```typescript
export interface ScribeEvents {
    another_function: DummyType;
    another: null;
    test_function: Object;
}
```

You should generate the code:
```typescript
import { DummyType } from "./scribetypes";

export abstract class ScribeClient {
    socket: Socket;
    on_another_function?(data: DummyType): void;
    on_another?(): void;
    on_test_function?(data: Object): void;

    constructor(socket: Socket) {
        this.socket = socket;
        subscribe(this, "another_function", this.on_another_function);
        subscribe(this, "another", this.on_another);
        subscribe(this, "test_function", this.on_test_function);
    }
}
```

For example:
```typescript
export interface ScribeEvents {
    chat_event: ChatEvent;
    chat_message: MessageFromNPC;
    patient_state: SimUpdateData;
}
```

Should result in the following code:
```typescript
import { ChatEvent, MessageFromNPC, SimUpdateData } from "./scribetypes";

export abstract class ScribeClient {
    socket: Socket;
    on_chat_event?(data: ChatEvent): void;
    on_chat_message?(data: MessageFromNPC): void;
    on_patient_state?(data: SimUpdateData): void;

    constructor(socket: Socket) {
        this.socket = socket;
        subscribe(this, "chat_event", this.on_chat_event);
        subscribe(this, "chat_message", this.on_chat_message);
        subscribe(this, "patient_state", this.on_patient_state);
    }
}
```

Generate the code for the following ScribeEvents object:

<SCHEMA>
    """

    ts_file_path = f"{generated_dir}/scribetypes.d.ts"

    with open(ts_file_path, "r") as f:
        ts_file_contents = f.read()


    # find all the lines in ts_file_contents which contain an element in emitted_event_names
    def is_emitted_event(line: str) -> bool:
        line = line.strip();
        for event_name in emitted_event_names:
            if event_name in line and "__server" not in line:
                return True
        return False

    lines = ts_file_contents.split("\n")
    lines = [line.strip() for line in lines if is_emitted_event(line)]
    sio_events_content = "\n".join(lines)

    # # Regular expression to extract the ScribeEvents interface content
    # pattern = re.compile(r'(export interface ScribeEvents \{.*?\})', re.DOTALL)
    # match = pattern.search(ts_file_contents)
    # if not match:
    #     raise Exception("Could not find ScribeEvents interface in scribetypes.d.ts")
    # sio_events_content = match.group(1)

    formatted_prompt = prompt.replace("<SCHEMA>", sio_events_content)

    emit_events_str = []
    for handled_event in handled_events:
        event_str = handled_event.handler_name[3:]
        event_variable = event_str.replace(" ", "_").replace("-", "_").upper()
        emit_events_str.append(f"\t{event_variable} = \"{event_str}\",")
    emit_events_consts = "\n".join(emit_events_str)
    emit_events_enum = f"""
export enum EmitEvent {{
{emit_events_consts}
}}
    """.strip()

    from packages.server.gpt.gpt_api import gpt, MODEL_GPT35, GPTMessage, Role, MODEL_GPT4

    async def main():
        show_progress="Generating ScribeClient..."
        # if not verbose:
        show_progress = True
        response = await gpt([GPTMessage(role=Role.USER, content=formatted_prompt)], model=MODEL_GPT4, show_progress=show_progress, max_tokens=1000)

        response = response.strip()
        response = response.replace("```typescript", "").replace("```", "").strip()

        generated_ts_content = """
/* eslint-disable */
/**
* This file was automatically generated by Scribe's codegen tool.
* This class was generated by GPT3.5, so godspeed and good luck.
*/

import { Socket } from 'socket.io-client';

<EMIT_EVENTS_ENUM>

function subscribe(obj: ScribeClient, event: string, callback?: (data: any) => void) {
    if (callback) {
        obj.socket.on(event, (data) => {
            callback.call(obj, data);
        });
    }
}

<CLASS>
    """.strip().replace("<EMIT_EVENTS_ENUM>", emit_events_enum).replace("<CLASS>", response)

        if not os.path.exists(generated_dir):
            os.mkdir(generated_dir)

        with open(f"{generated_dir}/ScribeClient.ts", "w") as f:
            f.write(generated_ts_content)
        with open(f"{generated_dir}/scribetypes.d.ts", "w") as f:
            f.write(ts_file_contents)

        frontend_folder = "packages/frontend/src/scribe"
        import shutil
        shutil.move(f"{generated_dir}/ScribeClient.ts", f"{frontend_folder}/ScribeClient.ts")
        shutil.move(f"{generated_dir}/scribetypes.d.ts", f"{frontend_folder}/scribetypes.d.ts")

        # remove generated_dir
        shutil.rmtree(generated_dir)

        print(f"Generated Scribe interface in frontent/src/scribe")

    asyncio.run(main())



if __name__ == "__main__":
    generate_code(verbose=True)