from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase
from packages.medagogic_sim.history import sim_history
from packages.medagogic_sim.main import MedagogicSimulator
from packages.medagogic_sim.exercise.describe_perception import describe_perception, perception_dict_to_markdown
import asyncio
from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage, MODEL_GPT35



async def get_next_move(simulator: MedagogicSimulator, dr_clippy_suggestion: str):   
    perception = await describe_perception(simulator.context.simulation)
    perception_markdown = perception_dict_to_markdown(perception)

    sim_state = f"""
{simulator.context.metadata.case_description}

{simulator.context.metadata.vignette}

{simulator.context.get_exposed_vitals().to_markdown()}

{perception_markdown}

# Actions Taken So Far
{simulator.context.history.get_markdown()}
    """

    actions_list = simulator.context.action_db.get_relevant_actions_markdown(dr_clippy_suggestion, 8, shuffle=True)

    system_prompt = f"""
# Simulation State
{sim_state}

# Available Actions
{actions_list}

# Instructions
The user will provide you with information about the next priority to address in the patient's care. You should use all information provided to determine a specific action to perform.

Pick an available action from the list which satisfies the user's request. Do not provide any reasoning, just a single action with any required parameters.
""".strip()
    
    # print(system_prompt)
    
    user_message = dr_clippy_suggestion

    messages = [SystemMessage(system_prompt), UserMessage(user_message)]
    full_response = await gpt(messages, model="gpt-4-turbo-preview", temperature=0.1, cache_skip=True)

    print(full_response)

    return full_response


async def get_action_from_clippy(simulator: MedagogicSimulator):
    advice = simulator.dr_clippy.cached_output.advice[0]
    print(advice)
    tasks = []
    for i in range(3):
        task = get_next_move(simulator, advice)
        tasks.append(task)
    results = await asyncio.gather(*tasks)

    return results


if __name__ == "__main__":
    async def main():
        simulator = MedagogicSimulator()

        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Obtain IV access", params=[]))
        # simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect ventilator", params=["AC", "0.5"]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect EKG/ECG", params=[]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect BP monitor", params=[]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect pulse oximeter", params=[]))

        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Obtain IV access", npc_name="Nurse Smith"))
        # simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect ventilator", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect EKG/ECG", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect BP monitor", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect pulse oximeter", npc_name="Nurse Smith"))

        action_sequence = ["Jaw thrust", "Give oxygen via non-rebreather mask (15L/min)"]

        for action in action_sequence:
            reciept = simulator.context.simulation.applyUpdate(action)
            
            while not reciept.finished:
                await asyncio.sleep(1)

            simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content=action, npc_name="Nurse Smith"))

        if simulator.dr_clippy.update_advice_task is not None:
            await simulator.dr_clippy.update_advice_task
        else:
            await simulator.dr_clippy.recalculate_advice()

        clippy_actions = await get_action_from_clippy(simulator)
        print(clippy_actions)


        # simulator.context.get_exposed_vitals()


        # while True:
        #     await asyncio.sleep(1)

    asyncio.run(main())