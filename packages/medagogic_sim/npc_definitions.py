from typing import Final, List
from pydantic import BaseModel

class NPCDefinition(BaseModel):
    name: str
    role: str
    specialities: List[str]
    years_of_experience: int


NPC_DEFINITIONS: Final[List[NPCDefinition]] = [
    NPCDefinition(name="Dr Johnson", role="Pediatric ER Physician", 
                  specialities=["Pediatric emergency medicine", "Trauma management", "Advanced airway management"], 
                  years_of_experience=10),
    
    NPCDefinition(name="Nurse Smith", role="Pediatric ER Nurse", 
                  specialities=["Pediatric nursing", "IV insertion", "Vital signs monitoring"], 
                  years_of_experience=6),
    
    NPCDefinition(name="Nurse Taylor", role="Pediatric ER Nurse", 
                  specialities=["Pediatric nursing", "Medication administration", "Wound care"], 
                  years_of_experience=8),
    
    NPCDefinition(name="Dr Patel", role="Pediatric ER Resident Physician", 
                  specialities=["Pediatric emergency medicine", "Patient assessment", "Basic airway management"], 
                  years_of_experience=3),
    
    NPCDefinition(name="Dr Williams", role="Pediatric Anesthesiologist", 
                  specialities=["Pediatric anesthesia", "Advanced airway management", "Sedation"], 
                  years_of_experience=12)
]
