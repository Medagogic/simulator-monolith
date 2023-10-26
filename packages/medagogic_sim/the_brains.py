from __future__ import annotations
from enum import Enum
import re
import time
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npc import MedicalNPC

import asyncio
from packages.medagogic_sim.gpt.medagogic_gpt import MODEL_GPT35, MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage
from rx.subject import Subject
from packages.medagogic_sim.actions_for_brains import ActionDatabase, TaskCall


import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.INFO)


class RightBrainDecision(Enum):
    NONE = "NONE"
    YES = "YES"
    NO = "NO"
    MORE_INFO = "MORE INFO"
    NOT_A_COMMAND = "NOT A COMMAND"

class RightBrainResponse(BaseModel):
    decision: RightBrainDecision = RightBrainDecision.NONE
    info: str
    actions_list: Optional[List[str]]
    full_response: str

class LeftBrainResponse(BaseModel):
    dialog: str


class BrainBase:
    def __init__(self, context: ContextForBrains, action_db: ActionDatabase, model: str=MODEL_GPT4, temperature: float=0) -> None:
        self.context = context
        self.action_db = action_db
        self.model = model
        self.temperature = temperature
        self.show_usage = False


    @property
    def full_world_state(self) -> str:
        device_lines = self.context.device_interface.full_state_markdown(only_connected=False)
        devices = "\n".join([f" - {l}" for l in device_lines])

        history = self.context.history.get_cached_summary()

        state = f"""
# World State

## Devices

{devices}

## History

{history}

{self.context.interventions_markdown}

## Current Patient State

{self.context.simulation.getExercise().to_markdown(include_progression=False)}
        """
        return state
    
    def get_actions_markdown(self, user_input: str) -> str:
        return self.action_db.get_relevant_actions_markdown(user_input)
    

class RightBrain(BrainBase):
    async def do_check(self, check_text: str) -> RightBrainResponse:
        system_message = f"""
Decide wether the user's request is possible based on the current simulation state.

In your explanations, you are to roleplay as a doctor in the simulation. Stay in character as a medical professional in a high-stress acture care emergency room scenario. This is a training simulation, so you can't do anything wrong. Be as realistic as possible. Be concise, and use proper medical terminology. It is best to mirror the user's input for good closed-loop communication. Do not explain medical concepts or reasoning to the user, they are a trained medical professional. You are to only explain why the user's input is not possible, or what additional information is required. Be short. Be concise. Be realistic. Use "Telegraphic Style", where you focus on the most crucial words and omit articles, conjunctions, or other "filler" elements where possible. Telegraphic style: Uses essential words, omits filler, concise, clear.

Your response must be one of the following:
YES
MORE INFO
NO
NONE

If YES:
    - Provide a comma separated list of actions to perform, as <action 1 name> (<parameter 1>, <parameter 2>, ...), <action 2 name> (<parameter 1>, <parameter 2>, ...), ...
    - eg: `Obtain IV access, Administer medication (normal saline, 500mL, IV)`
    - eg: `Give oxygen via non-rebreather mask (15L/min)`
    - eg: `Assess airway`
    - eg: `Prepare bolus, Chin lift`

If MORE INFO:
    - Provide a brief description of what additional information is required

If NO:
    - Provide a brief explanation of why the action is not possible

If NONE:
    - State that there is no instruction

For example:

Example 1: User input is possible, single action
```
YES: Obtain IV access
```

Example 2: User input is possible, but more information is required
```
MORE INFO: What size needle?
```

Example 3: User input is not possible due to simulation state
```
NO: We don't have IV access yet.
```

Example 4: User input is not possible due to simulation state
```
NO: Blood pressure monitor is already connected.
```

Example 5: User input is possible with multiple actions
```
YES: Give oxygen via non-rebreather mask (15L/min), Titrate oxygen (> 94%)
```

Example 6: User input is impossible because one of the actions is not possible
```
NO: We don't have IV access yet.
```

Example 7: User input is possible due to order of actions
```
YES: Obtain IV access, Administer medication (normal saline, 500mL, IV)
```

Example 8: User input is not an instruction
```
NONE: No instruction.
```

- NOTE: You may re-order the actions if this will help the requirements be filled better.
- NOTE: All parameters for actions must be specified in the response.
- NOTE: It may be possible to imply parameters from the user's input, and you should do so if possible.
- NOTE: Do not spend time asking for superfluous information which you would yourself know in an emergency room setting.
- NOTE: You should only assess the `requirements` of the first action you would perform.
        """

        messages = [
            SystemMessage(content=system_message),
            SystemMessage(content=self.full_world_state),
            SystemMessage(content=self.get_actions_markdown(check_text)),
            UserMessage(content=check_text)
        ]

        response = await gpt(messages, self.model, temperature=self.temperature)

        a, b = response.split(":", 1)

        decision: RightBrainDecision = RightBrainDecision(a.strip().upper())
        info = b.strip()

        actions_list: Optional[List[str]] = None
        if decision == RightBrainDecision.YES:
            actions_list = self.split_actions(info)

        return RightBrainResponse(decision=decision, info=info, actions_list=actions_list, full_response=response)

    @staticmethod
    def split_actions(actions_string) -> List[str]:
        # The regex pattern matches commas not enclosed by parentheses
        pattern = r',(?![^()]*\))'
        actions = re.split(pattern, actions_string)
        # Strip leading/trailing white spaces
        actions = [action.strip() for action in actions]
        return actions



class LeftBrain(BrainBase):

    async def generate_yes(self, user_input: str) -> LeftBrainResponse:
        messages: List[GPTMessage] = [
            SystemMessage(content="Reply to the user to confirm that you will take the action they have told you to perform. Stay in character as a medical professional in a high-stress acture care emergency room scenario. This is a training simulation, so you can't do anything wrong. Be as realistic as possible. Be concise, and use proper medical terminology. It is best to mirror the user's input for good closed-loop communication. Do not say 'I will', rather just start with the verbs. For example, if the user said 'Give 2mg of epinephrine IV', you could reply with 'Giving 2mg of epinephrine IV'."),
            UserMessage(content=user_input)
        ]

        response = await gpt(messages, self.model, temperature=self.temperature)

        return LeftBrainResponse(dialog=response)
    

    async def generate_more_info(self, user_input: str) -> LeftBrainResponse:
        messages: List[GPTMessage] = [
            SystemMessage(content="Reply to the user to ask them for the information required to complete the instructions they are giving, based on the data in the actions list. Be brief and concise, and do not ask for information you don't need. Don't ask for information which the user has already given. You may ask for clarifications if something is unclear. Keep your response as short as possible. For example, if the user said 'We need to get IO access', you could reply with 'What size needle?'. Do not repeat the user's input, they know the context. You are a medical professional in a high-stress acture care emergency room scenario. This is a training simulation, so you can't do anything wrong. Be as realistic as possible. You do not need to include any context in your response, the user already knows the context."),
            SystemMessage(content=self.full_world_state),
            SystemMessage(content=self.get_actions_markdown(user_input)),
            UserMessage(content=user_input)
        ]

        response = await gpt(messages, self.model, temperature=self.temperature)

        return LeftBrainResponse(dialog=response)
    

class PersonalityBrain:
    def __init__(self, context: ContextForBrains) -> None:
        self.context = context

    async def generate_response(self, input_text: str, who_am_i: str) -> str:
        messages: List[GPTMessage] = [
            SystemMessage(content=f"""
{self.context.simulation.getExercise().to_markdown(include_progression=False)}

You are:
{who_am_i}

This is a virtual simulated training environment in an emergency room setting. Reply to the user. Be brief and concise. Do not repeat the user's input, they know the context. You are a medical professional in a high-stress acture care emergency room scenario. This is a training simulation, so you can't do anything wrong. Be as realistic as possible. You do not need to include any context in your response, the user already knows the context. Use "Telegraphic Style", where you focus on the most crucial words and omit articles, conjunctions, or other "filler" elements where possible. Telegraphic style: Uses essential words, omits filler, concise, clear.

Stay in character in your response. The user is in the Team Lead role in this emergency scenario, reply appropriately. This is the first message in the simulation.
""".strip() 
            ),
            UserMessage(content=input_text)
        ]

        response = await gpt(messages, MODEL_GPT4, temperature=0)

        return response



class NPCBrain:
    def __init__(self, context: ContextForBrains, npc: MedicalNPC) -> None:
        self.context = context
        self.npc = npc

        model: str=MODEL_GPT4
        self.right_brain = RightBrain(context, model=model, action_db=context.action_db, temperature=0)
        self.left_brain = LeftBrain(context, model=model, action_db=context.action_db, temperature=0)
        self.personality_brain = PersonalityBrain(context)

        self.on_error = Subject()
        self.on_dialog = Subject()
        self.on_actions = Subject()


    async def is_instruction(self, command_text: str) -> bool:
        prompt = f"""
Is the following an instruction, command, or request for an action to be performed?
"{command_text}"
If yes, reply with "YES"
If no, reply with "NO"
Do not include any other text in your response.
        """
        response = await gpt([UserMessage(content=prompt)], model=MODEL_GPT35, temperature=0)
        return response.strip().upper() == "YES"
    

    async def process_user_input(self, command_text: str) -> RightBrainDecision:
        if command_text.strip() == "":
            raise ValueError("User input is empty")
        
        who_am_i = self.npc.markdown_summary()
        
        is_instruction = await self.is_instruction(command_text)
        if not is_instruction:
            dialog = await self.personality_brain.generate_response(command_text, who_am_i)
            self.on_dialog.on_next(dialog)
            return RightBrainDecision.NOT_A_COMMAND

        start_time = time.time()

        tasks = [
            self.right_brain.do_check(command_text),
            self.left_brain.generate_yes(command_text),
            self.left_brain.generate_more_info(command_text),
        ]

        results = await asyncio.gather(*tasks)
        result_rb: RightBrainResponse = results[0]
        result_lb_yes: LeftBrainResponse = results[1]
        result_lb_moreinfo: LeftBrainResponse = results[2]

        if result_rb.decision == RightBrainDecision.YES:
            self.on_dialog.on_next(result_lb_yes.dialog)

            if result_rb.actions_list:
                logger.debug(f"{command_text} -> {result_rb.actions_list}")
                action_models = [self.context.action_db.get_action_from_call(action_call, command_text) for action_call in result_rb.actions_list]
                self.on_actions.on_next(action_models)
        elif result_rb.decision == RightBrainDecision.MORE_INFO:
            self.on_dialog.on_next(result_lb_moreinfo.dialog)
        else:
            self.on_error.on_next(result_rb.info)

        logger.debug(f"process_user_input took {time.time() - start_time:.2f}s for {command_text}")

        return result_rb.decision
    

if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npc import get_test_npc

    logger.setLevel(logging.DEBUG)

    async def main() -> None:
        context = ContextForBrains()

        npc = get_test_npc(context)
        full_brain = npc.brain

        async def run_test(command_text: str, expected_result: RightBrainDecision, expected_actions: List[str]=[]) -> bool:
            nonlocal full_brain

            recieved_errors: List[str] = []
            recieved_dialogs: List[str] = []
            recieved_actions: List[List[TaskCall]] = []

            full_brain.on_error.subscribe(lambda x: recieved_errors.append(x))
            full_brain.on_dialog.subscribe(lambda x: recieved_dialogs.append(x))
            full_brain.on_actions.subscribe(lambda x: recieved_actions.append(x))

            result = await full_brain.process_user_input(command_text)

            error: Optional[str] = None
            dialog: Optional[str] = None
            actions: Optional[List[TaskCall]] = []

            if len(recieved_errors) > 0:
                error = recieved_errors[0]
            if len(recieved_dialogs) > 0:
                dialog = recieved_dialogs[0]
            if len(recieved_actions) > 0:
                actions = recieved_actions[0]

            results_match = str(result) == str(expected_result)

            if not results_match: 
                logger.error(f"TEST FAILED ({command_text}): Expected {expected_result}, got {result}")
                return False
        
            if len(expected_actions) > 0 and not actions:
                logger.error(f"TEST FAILED ({command_text}): Expected {len(expected_actions)} actions, got none")
                return False

            if len(expected_actions) != len(actions):   # type: ignore
                logger.error(f"TEST FAILED ({command_text}): Expected {len(expected_actions)} actions, got {len(actions)}")    # type: ignore
                if actions:
                    logger.info([action.call_data for action in actions])
                return False
            
            if actions:
                logger.debug(f"ACTIONS: {[action.call_data for action in actions]}")
                for i in range(len(expected_actions)):
                    if expected_actions[i] != actions[i].call_data.name:   # type: ignore
                        logger.error(f"TEST FAILED ({command_text}): Expected action `{expected_actions[i]}`, got `{actions[i].call_data.name}`")
                        return False
                
            logger.info(f"TEST PASSED ({command_text}): {dialog and dialog or error}")
            return True


        tests = [
            # run_test("Chin lift", RightBrainDecision.YES, ["Chin lift"]),
            # run_test("Check airway and perform chin lift if necessary", RightBrainDecision.YES, ["Assess airway", "Chin lift"]),
            # run_test("Give 0.3mg of epinephrine IV", RightBrainDecision.NO),
            # run_test("Get IV access and give 0.3mg epinephrine stat", RightBrainDecision.YES, ["Obtain IV access", "Administer medication"]),
            # run_test("Connect BP monitor", RightBrainDecision.YES, ["Connect BP monitor"]),
            # run_test("Start her on oxygen via non-rebreather mask at 15L/min and titrate to maintain SpO2 > 94%", RightBrainDecision.YES, ["Give oxygen via non-rebreather mask", "Titrate oxygen"]),
            # run_test("Let's get IV access", RightBrainDecision.YES, ["Obtain IV access"]),
            # # run_test("We need to prepare to amputate the patient's leg", RightBrainDecision.NO),
            # run_test("Obtain IO access, right tibia", RightBrainDecision.MORE_INFO),
            # # run_test("Start intubation, 4mm ET tube", RightBrainDecision.NO),
            # run_test("Start with assessing the airway and perform a chin lift if needed", RightBrainDecision.YES, ["Assess airway", "Chin lift"]),
            # # run_test("Give albuterol 2.5mg via nebulizer and monitor for improvement", RightBrainDecision.NO),  # No free airway
            run_test("Get IV access and give 0.3mg epinephrine stat, then monitor for improvement", RightBrainDecision.YES, ["Obtain IV access", "Administer medication", "Monitor for change"]),
            # run_test("Prepare bolus of 120 milliliters of ringers lactate", RightBrainDecision.YES, ["Prepare bolus"]),
            # run_test("Prepare bolus of 120 milliliters of ringers lactate and administer when IV access is established", RightBrainDecision.YES, ["Prepare bolus", "Wait", "Administer bolus"]),
            # run_test("Let's get a background history from his mother please", RightBrainDecision.YES, ["Talk to parent"]),
        ]

        for test in tests:
            await test
            await asyncio.sleep(3)

    asyncio.run(main())