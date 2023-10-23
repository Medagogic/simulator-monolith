from __future__ import annotations
import json
import os
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions

import dotenv
dotenv.load_dotenv()


ACTIONS_HEADER = """Actions which you are capable of as part of the simulation:

- Action name ($param1 $param2)
    : Description: Description of the action
    : Requirement: Requirement which must be met for the action to be possible
    : Example input: Example of user input which would trigger this action, and the action which would be taken

Action List:
"""


class ActionExample(BaseModel):
    input: str
    action: str


class ActionModel(BaseModel):
    name: str
    description: str
    exampleInputs: List[str]
    exampleActions: Optional[List[str]] = None
    examples: List[Union[str, ActionExample]]
    requirements: List[str]
    animationId: str
    connectDeviceIDs: Optional[List[str]] = None
    type: str

    @property
    def markdown(self) -> str:
        requirements_list = "\n".join([f"\t: Requirement: {r}" for r in self.requirements])
        input_examples_list = "\n".join([f"\t: Example input: {e}" for e in self.exampleInputs])

        full_markdown = f"""
- {self.name}
\t: Description: {self.description}
        """.strip()

        if requirements_list.strip():
            full_markdown += "\n" + requirements_list

        for example in self.examples:
            if isinstance(example, str):
                full_markdown += f"\n\t: Example input: {example} -> {self.name}"
            else:
                full_markdown += f"\n\t: Example input: {example.input} -> {example.action}"
                # full_markdown += f"\n\t\t: Resulting action: {example.action}"
        
        return full_markdown.strip()
    

    @property
    def search_text(self) -> str:
        input_examples_list = "\n".join([f"\t{e}" for e in self.exampleInputs])

        full_markdown = f"""
- {self.name}
\t{self.description}
        """.strip()

        if input_examples_list.strip():
            full_markdown += "\n" + input_examples_list
        
        return full_markdown.strip()
    

class TaskCall(ActionModel):
    full_input: str
    call_data: ActionDatabase.CallData
    

def loadActions() -> List[ActionModel]:
    with open("packages/medagogic_sim/action_definitions.json", "r") as f:
        loaded_actions: List[Dict] = json.load(f)

    action_models: List[ActionModel] = []

    for action_dict in loaded_actions:
        model = ActionModel(**action_dict)
        action_models.append(model)

    return action_models


class ActionDatabase:
    def __init__(self):
        self.actions = loadActions()

        self.client: chromadb.API = chromadb.Client()

        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name="text-embedding-ada-002"
            )

        print("Creating ActionDB Index...")
        self.full_actions_collection = self.client.create_collection(
            name="full_actions", 
            embedding_function=openai_ef,
        )
        self.__prepare_full_actions_collection()

        print("Indexing complete.")

    def __prepare_full_actions_collection(self):
        documents=[action.search_text for action in self.actions]
        metadatas=[{"index": i} for i in range(len(self.actions))]

        self.full_actions_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=[f"{i}" for i in range(len(self.actions))]
        )

    def get_relevant_actions(self, user_input: str) -> List[ActionModel]:
        result = self.full_actions_collection.query(
            query_texts=[user_input],
            n_results=5,
        )

        action_ids = result["ids"][0]

        return [self.actions[int(i)] for i in action_ids]
    

    def get_relevant_actions_markdown(self, user_input: str) -> str:
        actions = self.get_relevant_actions(user_input)
        full_markdown = ACTIONS_HEADER + "\n" + "\n".join([a.markdown for a in actions])
        return full_markdown
    

    class CallData(BaseModel):
        name: str
        params: List[str]


    def __parse_call(self, call: str) -> CallData:
            pure_name: str = call
            params: List[str] = []

            if "(" in call:
                pure_name, params_str = call.split("(", 1)
                pure_name = pure_name.strip()
                params_str = params_str.replace(")", "").strip()
                params = params_str.split(",")
                params = [p.strip() for p in params]

            return ActionDatabase.CallData(name=pure_name, params=params)


    def get_action_from_call(self, call: str, full_input: str) -> TaskCall | None:
        call_data = self.__parse_call(call)
        
        for action in self.actions:
            action_call_data = self.__parse_call(action.name)

            if call_data.name.lower() == action_call_data.name.lower():
                TaskCall.update_forward_refs()
                task_call = TaskCall(**action.dict(), call_data=call_data, full_input=full_input)
                return task_call
            
        print(f"Error: No action found for call {call}")
                
        return None

if __name__ == "__main__":
    db = ActionDatabase()

    # actions_markdown = db.get_relevant_actions_markdown("Check the airway and perform a chin lift if needed")
    actions_markdown = db.get_relevant_actions_markdown("Let's get IV access and start fluids")
    print(actions_markdown)

    # action = db.get_action_from_call("Connect EKG/ECG")
    # print(action)