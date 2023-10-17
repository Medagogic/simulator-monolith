from typing import Dict, List

from pydantic import BaseModel
from packages.server.sim_app.sessionrouter import SimSessionRouter
import json
# get the location of this file
import os
from pathlib import Path
import re

from packages.server.web_architecture.sio_typing.sio_api_emitters import SIOEmitSchema
from packages.server.web_architecture.sio_typing.sio_api_handlers import get_field_info

this_file = Path(os.path.realpath(__file__))
this_dir = this_file.parent
schema_dir = f"{this_dir}/schemas"
generated_dir = f"{this_dir}/generated"

event_datas: List[SIOEmitSchema] = SimSessionRouter.SIO_EMIT_DATA

schema_properties: Dict[str, Dict] = {}

for event_data in event_datas:
    if event_data.real_type is not None and issubclass(event_data.real_type, BaseModel):
        schema = event_data.real_type.model_json_schema()
        filename = f"{schema['title']}.schema.json"
        schema["$id"] = filename
        schema["additionalProperties"] = False
        with open(f"{schema_dir}/{filename}", "w") as f:
            json.dump(schema, f, indent=4)
        schema_properties[event_data.event_name] = {"$ref": f"schemas/{filename}"}
    else:
        schema_properties[event_data.event_name] = get_field_info(event_data.data_schema)

required_fields = [event_data.event_name for event_data in event_datas]

schema_dict = {
    "$id": "SIO Events",
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": schema_properties,
    "additionalProperties": False,
    "required": required_fields
}

with open(f"{schema_dir}/sioevents.schema.json", "w") as f:
    json.dump(schema_dict, f, indent=4)


# run generate_events.sh
import subprocess
subprocess.run(["bash", f"{this_dir}/generate_events.sh"])

prompt = """
Create an abstract typescript class which provides virtual functions for each element in SIOEvents, with a single paramater "data" of the associated type. Do not provide any surrounding text, provide only the code.

For example:
export interface SIOEvents {
  another_function: DummyType;
  another: null;
  test_function: Object;
}

You should generate the code:
import {DummyType} from "./sioevents";

export abstract class SIOEventProcessor {
  socket: Socket;
  abstract on_another_function(data: DummyType): void;
  abstract on_another(): void;
  abstract on_test_function(data: Object): void;

  constructor(socket: Socket) {
    this.socket = socket;
    this.socket.on("another_function", (data: DummyType) => this.on_another_function(data));
    this.socket.on("another", () => this.on_another());
    this.socket.on("test_function", (data: Object) => this.on_test_function(data));
  }
}

Generate the code for the following SIOEvents object:

<SCHEMA>
"""

ts_file_path = f"{generated_dir}/sioevents.d.ts"

with open(ts_file_path, "r") as f:
    ts_file_contents = f.read()

# Regular expression to extract the SIOEvents interface content
pattern = re.compile(r'(export interface SIOEvents \{.*?\})', re.DOTALL)


# Search for the pattern
match = pattern.search(ts_file_contents)

if not match:
    raise Exception("Could not find SIOEvents interface in sioevents.d.ts")
    
sio_events_content = match.group(1)

formatted_prompt = prompt.replace("<SCHEMA>", sio_events_content)

print(formatted_prompt)

from packages.server.gpt.gpt_api import gpt, MODEL_GPT35, GPTMessage, Role

async def main():
    response = await gpt([GPTMessage(role=Role.USER, content=formatted_prompt)], model=MODEL_GPT35)
    print(response)

    output_text = """
/* eslint-disable */
/**
 * This file was automatically generated by packages/tools/generate_sio_class.py
 * GPT made this, so godspeed and good luck.
 */

import { Socket } from "socket.io";
<CLASS>
""".strip().replace("<CLASS>", response)

    with open(f"{generated_dir}/SIOEventProcessor.ts", "w") as f:
        f.write(output_text)
    with open(f"{generated_dir}/sioevents.d.ts", "w") as f:
        f.write(ts_file_contents)

    # Move the two files to packages/frontend/src/sioevents
    import shutil
    shutil.move(f"{generated_dir}/SIOEventProcessor.ts", f"packages/frontend/src/sioevents/SIOEventProcessor.ts")
    shutil.move(f"{generated_dir}/sioevents.d.ts", f"packages/frontend/src/sioevents/sioevents.d.ts")

import asyncio
asyncio.run(main())