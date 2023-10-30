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
from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase, TaskCall

from packages.medagogic_sim.action_db.input_classifier import ActionClassifier


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
    dialog: str
    actions_list: Optional[List[str]] = None
    action_models: Optional[List[TaskCall]] = None


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

## Current Patient State

{self.context.simulation.getExercise().to_markdown(include_progression=False)}
        """
        return state
    
    def get_actions_markdown(self, user_input: str) -> str:
        return self.action_db.get_relevant_actions_markdown(user_input)
    

class ReasonableRequestResponse(BaseModel):
    passed: bool
    explanation: Optional[str] = None
    detected_actions: Optional[str] = None


class RightBrain(BrainBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_classifier = ActionClassifier.load()


    async def is_reasonable_request(self, instruction_from_team_lead: str) -> ReasonableRequestResponse:
        difficulty_nohelp = """
Decide if the request is logical. This is an educational experience for the Team Lead. Allow the Team Lead to make incorrect treatments, and do not correct them if you believe they are focusing on the wrong thing. Don't think about medical accuracy or treatment methods, only check for logical or logistical problems.
""".strip()
        
        difficulty_fullhelp = """
Decide if the request is possible and medically sound based on the information above.
""".strip()


        system_prompt = f"""
This is a virtual simulation training exercise for pediatric emergencies.

{self.full_world_state}

The user will provide you a request which the Team Lead in the simulation is requesting a medical professional to perform. {difficulty_nohelp} Your reply must be either "Yes" if the full request is okay, or "No".

If the request involves multiple actions, they will be enacted by one individual, sequentially. Therefore, you must consider the entire request as a sequence of actions where an earlier action may faciliate a later action.

If you respond with "Yes", you must also include some dialog to the Team Lead to inform of intent to perform the request - it's good to echo the Team Lead's request back, for example if "Let's get IV access" is appropriate, respond "Yes: Starting IV access". If "Let's get the clothes off and check the torso for signs of injuries" is appropriate, respond "Yes: I'll get the clothes removed and then check for injuries".

If you respond with "No", you must also include some dialog to the Team Lead to explain why, eg "No: We don't have IV access yet." or "No: That isn't an appropriate action".

Then provide a markdown list of the relevant actions.
        """.strip()

        user_prompt = f"""
{instruction_from_team_lead}
        """.strip()

        messages = [
            SystemMessage(content=system_prompt),
            # SystemMessage(content=""),
            UserMessage(content=user_prompt)
        ]

        gpt_response = (await gpt(messages, self.model, temperature=self.temperature)).strip()

        first_line = gpt_response.split("\n")[0]
        actions_text = gpt_response[len(first_line):].strip()

        logger.debug(f"`{instruction_from_team_lead}` -> Is reasonable: `{first_line}`")
        logger.debug(f"Actions: {actions_text}")

        if not first_line.lower().startswith("no:") and not first_line.lower().startswith("yes:"):
            logger.error(f"Invalid response: {first_line}")
            raise ValueError(f"Invalid response: {first_line}")
        elif first_line.lower().startswith("yes:"):
            explanation = first_line[4:].strip()
            return ReasonableRequestResponse(passed=True, explanation=explanation, detected_actions=actions_text)
        else:
            explanation = first_line[3:].strip()
            return ReasonableRequestResponse(passed=False, explanation=explanation)


    async def do_check(self, instruction_from_team_lead: str) -> RightBrainResponse:
        reasonable_result = await self.is_reasonable_request(instruction_from_team_lead)

        if not reasonable_result.passed:
            if not reasonable_result.explanation:
                raise ValueError("No explanation provided for unreasonable request")
            return RightBrainResponse(decision=RightBrainDecision.NO, dialog=reasonable_result.explanation)
        
        input_to_classifier = f"""
{reasonable_result.detected_actions}

{instruction_from_team_lead}
        """.strip()

        classified_function_calls = await self.action_classifier.get_function_calls(input_to_classifier)

        if classified_function_calls is None or len(classified_function_calls) == 0:
            logger.warning(f"No function calls detected for input: `{input_to_classifier}`")
            return RightBrainResponse(decision=RightBrainDecision.NOT_A_COMMAND, dialog="There's no command in the instruction text.", actions_list=None)
        
        logger.debug(f"Classified function calls: {classified_function_calls}")

        task_calls = [self.context.action_db.get_action_from_call(function_call, instruction_from_team_lead) for function_call in classified_function_calls]  

        logger.debug(f"Task calls: {[t.call_data if t else None for t in task_calls]}")

        found_all_tasks = len(task_calls) == len(classified_function_calls) and all([task_call is not None for task_call in task_calls])

        logger.debug(f"Found all tasks: {found_all_tasks}")

        decision = RightBrainDecision.YES if found_all_tasks else RightBrainDecision.NO
        dialog: str = reasonable_result.explanation     # type: ignore
        actions_list = classified_function_calls
        action_models: List[TaskCall] = task_calls  # type: ignore

        return RightBrainResponse(decision=decision, dialog=dialog, actions_list=actions_list, action_models=action_models)
       

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

        result_rb: RightBrainResponse = await self.right_brain.do_check(command_text)

        if result_rb.decision == RightBrainDecision.YES:
            self.on_dialog.on_next(result_rb.dialog)
            if result_rb.actions_list:
                logger.debug(f"{command_text} -> {result_rb.actions_list}")
                self.on_actions.on_next(result_rb.action_models)
        else:
            self.on_dialog.on_next(result_rb.dialog)

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
            # run_test("get iv access", RightBrainDecision.YES, ["Obtain IV access"]),
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
            # run_test("Get IV access and give 0.3mg epinephrine stat, then monitor for improvement", RightBrainDecision.YES, ["Obtain IV access", "Administer medication", "Monitor for change"]),
            # run_test("Prepare bolus of 120 milliliters of ringers lactate", RightBrainDecision.YES, ["Prepare bolus"]),
            # run_test("Prepare bolus of 120 milliliters of ringers lactate and administer when IV access is established", RightBrainDecision.YES, ["Prepare bolus", "Wait", "Administer bolus"]),
            # run_test("Let's get a background history from his mother please", RightBrainDecision.YES, ["Talk to parent"]),
            run_test("Prep the amputation kit, we need to amputate the patient's leg", RightBrainDecision.NO),
        ]

        for test in tests:
            await test
            await asyncio.sleep(3)

    asyncio.run(main())