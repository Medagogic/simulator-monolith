from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase
from packages.medagogic_sim.history import sim_history
from packages.medagogic_sim.main import MedagogicSimulator
from packages.medagogic_sim.exercise.describe_perception import describe_perception, perception_dict_to_markdown
import asyncio
from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage, MODEL_GPT35



async def get_drug_suggestions(simulator: MedagogicSimulator):
    system_prompt = """
The user will provide you with information about the current state of a patient in a critical care (ICU) simulation scenario. You should use all information provided to suggest medications and doses which the student could use to stabilise the patient, in the next 5-10 minutes.

Note: We are only interested in medications and similar treatments, not devices (ie oxygen), procedures (ie chin lift), or assessments (ie check blood pressure).

Give one treatment or medication to administer, including dosage information, administration route, method, or any other required information. Focus on the order of ABCDE.
""".strip()
    
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
    
    messages = [SystemMessage(system_prompt), UserMessage(sim_state)]
    full_response = await gpt(messages, model="gpt-4-turbo-preview")

    return full_response


async def process_drug_list(drug_suggestion_text: str):
    system_message = """
Take the list from the user and calculate doses for a 16kg patient.
Give one specific drug and dose combo per line. Do not give any explanation. If multiple options are given, split them into one per line.
You must calculate the appropriate dosages, and be precise - do not give a range, give a specific value.
""".strip()
    
    messages = [SystemMessage(system_message), UserMessage(drug_suggestion_text)]
    full_response = await gpt(messages, model="gpt-4-turbo-preview")

    return full_response


if __name__ == "__main__":
    async def main():
        simulator = MedagogicSimulator()

        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Obtain IV access", params=[]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect ventilator", params=["AC", "0.5"]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect EKG/ECG", params=[]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect BP monitor", params=[]))
        simulator.context.device_interface.handle_call(ActionDatabase.CallData(name="Connect pulse oximeter", params=[]))

        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Obtain IV access", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect ventilator", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect EKG/ECG", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect BP monitor", npc_name="Nurse Smith"))
        simulator.context.history.add_event(sim_history.Evt_CompletedIntervention(content="Connect pulse oximeter", npc_name="Nurse Smith"))

        while True:
            drug_suggestion_text = await get_drug_suggestions(simulator)
            print(drug_suggestion_text)

            print("\n####################\n")

            drug_list = await process_drug_list(drug_suggestion_text)
            print(drug_list)
            
            actions = drug_list.strip().split("\n")
            action = actions[0]
            print(f"Action: {action}")
            await simulator.process_user_input(action)


        # print(simulator.context.metadata.case_description + "\n")

        # print(simulator.context.metadata.vignette + "\n")

        # print(simulator.context.get_exposed_vitals().to_markdown() + "\n")

        # for manager in simulator.context.device_interface.all_managers:
        #     if manager.is_connected:
        #         print(f"{manager.get_state()}")

        # perception = await describe_perception(simulator.context.simulation)
        # print(perception_dict_to_markdown(perception) + "\n")

        # await simulator.dr_clippy.update_advice_task
        # print(simulator.dr_clippy.cached_output)

        # print("# Expected Actions")
        # for a in simulator.context.metadata.expected_actions:
        #     print(a)

        # exit()



        simulator.context.get_exposed_vitals()


        while True:
            await asyncio.sleep(1)

    asyncio.run(main())