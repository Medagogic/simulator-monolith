from __future__ import annotations
from fastapi import APIRouter

from packages.server.sim_app.exercise_creation.imported.simulation_types_old import Vitals
from packages.server.sim_app.exercise_creation.exercise_creation_types import ExerciseCreationParams, GeneratedExerciseData, ExerciseCreationVitalSigns, ExerciseCreationABCDE, ExerciseCreationFutureState
from packages.medagogic_sim.gpt.medagogic_gpt import gpt, GPTMessage, MODEL_GPT4
import asyncio


prompt_template="""
Create a description for a medical simulation, using accurate medical knowledge and data, for a training scenario. We will then use this data to progress through a training simulation. This should be a critical case with rapid intervention required, and the patient in rapid decline into shock and seizure. We need all patient info, vital signs, symptoms, etc. You are only to deal with the patient state and it's progression, you do not need to discuss any diagnoses, plans, objectives, or other "metadata" for the simulation.
Do not duplicate information - if it is listed in one area, it shouldn't be listed again in another entry.

Additionally, you should include some information about how the patients state will be changing over time.
Do NOT include any interventions or actions in the state progression. This progression should assume that no actions are taken to help the patients condition.
Any actions which are taken will be handled by another worker, and will modify the document you generate here at a later time.

The scenario description:
{patient_info}

Hidden information:
{simulation_instructions}

It is ESSENTIAL that all information you provide is medically accurate and fitting with the above description.

Use the following as examples. Match this format.

# Patient Profile
## Basic Information
- Age: 4 years old
- Sex: Female
- Weight: 15 kg
- Height: 100 cm

## Background Information
Fever and cough for the last 4 days. Last 24 hours tired, not showing interest in anything, decreased intake of food and liquids, no urinary output since yesterday. Has been using her inhalers regularly the last few days without improvement.

# Simulation Instructions
<The hidden information as a markdown list>

# Current Patient State
## Vital Signs
- Temperature: 38.4°C
- Heart Rate: 170 bpm
- Respiratory Rate: 50 breaths/min
- Blood Pressure: 70/50 mmHg
- Blood Glucose: 240 mg/dL
- Oxygen Saturation: 85%
- Capillary Refill: 3 seconds

## ABCDE
- A: Snoring/gurgling sounds. No free airway.
- B: Intercostal and jugular retractions. Decreased air entry with bilateral ronchi and slight wheezing, symmetrical.
- C: Greypale skin. Cold and slightly mottled extremities. No signs of organ enlargement.
- D: P on AVPU scale (responds to pain stimuli). Pupils are normal.
- E: No rash, no bruising or sores.

# State Progression
## Future Events
- Tonic-clonic seizure if blood glucose isn't resolved by @ 8 minutes
- If seizure is resolved, patient enters persistent hypotension

## Vital Signs
- Temperature: 39.5°C @ 10 minutes
- Heart Rate: 220 bpm @ 5 minutes
- Respiratory Rate: 55 breaths/min @ 7 minutes
- Blood Pressure: 60/30 mmHg @ 3 minutes
- Blood Glucose: No change
- Oxygen Saturation: 63% @ 5 minutes
- Capillary Refill: 6 seconds @ 3 minutes

## ABCDE
- A: No change
- B: No change
- C: No change
- D: U on AVPU scale (unresponsive). @ 5 minutes
- E: No change



# Patient Profile
## Basic Information
- Age: 3 years old
- Sex: Male
- Weight: 15 kg
- Height: 80 cm

## Background Information
Patient was playing at the playground when he fell from a height, landing on his arm, resulting in a broken arm. Patient is brought to the pediatric emergency room.

# Simulation Instructions
<The hidden information as a markdown list>

# Current Patient State
## Vital Signs
- Temperature: 37.5°C
- Heart Rate: 140 bpm
- Respiratory Rate: 30 breaths/min
- Blood Pressure: 90/60 mmHg
- Oxygen Saturation: 95%
- Blood Glucose: 110 mg/dL
- Capillary Refill: 2 seconds

## ABCDE
- A: Airway is patent
- B: Breathing is labored
- C: Circulation is compromised due to pain and anxiety
- D: AVPU: A (Alert); Pupils: equal, round, and reactive to light
- E: Exposed broken arm with swelling and deformity

# State Progression
## Future Events
- If given paracetamol, patient will go into anaphylactic shock

## Vital Signs
- Temperature: No change
- Heart Rate: 150 bpm @ 5 minutes
- Respiratory Rate: 35 breaths/min @ 7 minutes
- Blood Pressure: 85/55 mmHg @ 5 minutes
- Blood Glucose: No change
- Oxygen Saturation: 91% @ 5 minutes
- Capillary Refill: 4 seconds @ 5 minutes

## ABCDE
- A: No change
- B: Breathing is increasingly labored @ 10 minutes
- C: Circulation continues to be compromised, with blood pressure dropping @ 10 minutes
- D: Increasingly restless and agitated @ 10 minutes
- E: Increasing swelling and deformity of broken arm @ 10 minutes
"""



def prompt(patient_info: str, simulation_instructions: str) -> str:
    return prompt_template.format(patient_info=patient_info, simulation_instructions=simulation_instructions)


async def generate_exercise(patient_info: str, simulation_instructions: str="N/A") -> str:
    messages = [GPTMessage(role="user", content=prompt(patient_info=patient_info, simulation_instructions=simulation_instructions))]
    full_response = await gpt(messages, model=MODEL_GPT4, max_tokens=1000)
    return full_response



from packages.server.web_architecture.static_api import StaticAPIHandler
from packages.server.sim_app.exercise_creation.imported.markdownexercise import MarkdownExercise

class ExerciseCreatorAPI(StaticAPIHandler):
    def __init__(self, router: APIRouter):
        super().__init__(router)
        self.router.post("/generate_exercise")(self.handle_generate)


    async def handle_generate(self, params: ExerciseCreationParams) -> GeneratedExerciseData:
        patient_info_str = f"""
{params.basic_info.age} {params.basic_info.sex} ({params.basic_info.height}, {params.basic_info.weight}).

Conditions/sympoms: {params.exerciseDescription}
        """

        generated = await generate_exercise(patient_info=patient_info_str, simulation_instructions=params.simulationInstructions)

        print(generated)

        exercise = MarkdownExercise.from_markdown(generated)

        patientName = {
            "male": "Bjorn",
            "female": "Greta"
        }[params.basic_info.sex.lower()]

        sim_instructions = exercise.simulation_instructions
        if isinstance(sim_instructions, list):
            sim_instructions = "\n - ".join(sim_instructions)
        
        progression_events = exercise.progression.events
        if isinstance(progression_events, list):
            progression_events = "\n - ".join(progression_events)

        return GeneratedExerciseData(
            patientName=patientName,
            basicInfo=params.basic_info,
            backgroundInformation=exercise.patient_background,
            simulationInstructions=sim_instructions,
            vitalSigns=ExerciseCreationVitalSigns(
                temperature=f"{exercise.current_state.vital_signs.temperature} °C",
                heartRate=f"{exercise.current_state.vital_signs.heart_rate} bpm",
                respiratoryRate=f"{exercise.current_state.vital_signs.respiratory_rate} breaths/min",
                bloodPressure=f"{exercise.current_state.vital_signs.blood_pressure[Vitals.SYSTOLIC]:0.1f}/{exercise.current_state.vital_signs.blood_pressure[Vitals.DIASTOLIC]:0.1f} mmHg",
                bloodGlucose=f"{exercise.current_state.vital_signs.blood_glucose} mmoL/L",
                oxygenSaturation=f"{exercise.current_state.vital_signs.oxygen_saturation} %",
                capillaryRefill=f"{exercise.current_state.vital_signs.capillary_refill} seconds"
            ),
            ABCDE=ExerciseCreationABCDE(
                A=exercise.current_state.abcde.a,
                B=exercise.current_state.abcde.b,
                C=exercise.current_state.abcde.c,
                D=exercise.current_state.abcde.d,
                E=exercise.current_state.abcde.e
            ),
            future=ExerciseCreationFutureState(
                events=progression_events,
                vitalSigns=ExerciseCreationVitalSigns(
                    temperature="?",
                    heartRate="",
                    respiratoryRate="",
                    bloodPressure="",
                    bloodGlucose="",
                    oxygenSaturation="",
                    capillaryRefill=""
                ),
                ABCDE=ExerciseCreationABCDE(
                    A="?",
                    B="",
                    C="",
                    D="",
                    E=""
                )
            )
        )


if __name__ == "__main__":
    async def main():
        exercise = await generate_exercise(
            patient_info = "A 3 year old with acute asthma exacerbation.",
            simulation_instructions = ""
        )
        print(exercise)

    asyncio.run(main())