actions_list = """
- Perform head tilt/chin lift maneuver
- Perform jaw thrust maneuver
- Administer high-flow oxygen via non-rebreather mask
- Suction airway to remove secretions
- Insert oropharyngeal airway if no gag reflex is present
- Prepare for endotracheal intubation if airway patency cannot be maintained
- Administer high-flow oxygen via non-rebreather mask at 15 liters per minute.
- Suction airway to clear secretions.
- Consider intubation if respiratory effort is inadequate or if there is a decreased level of consciousness.
- Increase FiO2 on the ventilator to 1.0 if hypoxemia persists.
- Administer salbutamol nebulizer 2.5 mg.
- Administer ipratropium bromide nebulizer 250 mcg.
- Perform chest physiotherapy to mobilize secretions.
- Administer 20 ml/kg of Ringer's acetate as a fluid bolus.
- Administer a second 20 ml/kg bolus of Ringer's acetate.
- Administer Cefotaxime 50 mg/kg IV.
- Administer a third 20 ml/kg bolus of Ringer's acetate if hypotension persists.
- Administer epinephrine infusion starting at 0.1 mcg/kg/min.
- Administer norepinephrine infusion starting at 0.1 mcg/kg/min if blood pressure remains low after fluid resuscitation.
- Administer 10 ml/kg packed red blood cells if there is evidence of significant anemia contributing to shock.
- Administer 1 mg/kg of dopamine if hypotension persists despite fluid and epinephrine/norepinephrine.
- Administer 0.5 mg/kg of dobutamine if signs of poor perfusion and cardiac dysfunction persist.
- Assess level of consciousness using AVPU scale (Alert, Voice, Pain, Unresponsive)
- Administer 10% glucose 2-5 ml/kg IV if hypoglycemic
- Administer naloxone 0.1 mg/kg IV if opioid overdose is suspected
- Administer mannitol 0.25-1 g/kg IV over 20 minutes if signs of increased intracranial pressure
- Administer midazolam 0.1-0.2 mg/kg IV if seizures occur
- Perform a pupillary light reflex test
- Administer 3% hypertonic saline 2-5 ml/kg IV over 10-20 minutes if signs of cerebral edema
- Administer thiamine 10-25 mg IV if suspicion of Wernicke's encephalopathy
- Remove clothing to assess for rashes, petechiae, or other skin lesions
- Apply warm blankets to prevent hypothermia
- Measure core body temperature using a rectal thermometer
- Cover patient with a sterile surgical drape if central lines or invasive procedures are anticipated
- Administer antipyretics: Paracetamol 15 mg/kg rectally or ibuprofen 10 mg/kg orally if temperature is above 38.5°C
""".strip().split("\n")

actions_list = [a.strip() for a in actions_list if len(a.strip()) > 0]

import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_openai_embedding(text):
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    return np.array(response['data'][0]['embedding'])

def find_most_similar(input_text, string_list):
    input_vector = get_openai_embedding(input_text)

    # Convert each string in the list to a vector
    string_vectors = [get_openai_embedding(string) for string in string_list]

    # Compute cosine similarities
    similarities = cosine_similarity([input_vector], string_vectors)[0]

    # Find the index of the most similar string
    most_similar_index = np.argmax(similarities)

    return string_list[most_similar_index], similarities[most_similar_index]

# Example usage
input_text = "Give 10mg of "
most_similar_string, similarity_score = find_most_similar(input_text, actions_list)

print(most_similar_string, similarity_score)