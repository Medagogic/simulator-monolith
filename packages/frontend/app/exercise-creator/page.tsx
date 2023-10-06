"use client"

import React, { useEffect, useState } from 'react';
import InitialParametersForm, { generateDefaultData, InitialParametersFormState } from './InitialParametersForm';
import { motion, AnimatePresence } from 'framer-motion';
import InitialGenerationLoader from './InitialGenerationLoader';
import ExerciseReview from './ExerciseReview';
import { GeneratedExerciseData } from './ExerciseTypes';
import { useExerciseStore } from './ExerciseStore';


enum FormStage {
    Initial,
    Generating,
    EvaluateGeneratedExercise
}

const FormContainer: React.FC = () => {
    const [basicExerciseData, setBasicExerciseData] = useState<InitialParametersFormState>(generateDefaultData("3 years"));
    const [formStage, setFormStage] = useState<FormStage>(FormStage.Initial);
    // const [generatedExercise, setGeneratedExercise] = useState<GeneratedExerciseData | null>(null);

    useEffect(() => {
        setFormStage(FormStage.EvaluateGeneratedExercise);

        const tempExercise: GeneratedExerciseData = {
            patientName: "Greta",
            backgroundInformation: "Fever and cough for the last 4 days. Last 24 hours tired, not showing interest in anything, decreased intake of food and liquids, no urinary output since yesterday. Has been using her inhalers regularly the last few days without improvement.",
            patientAge: "4 years",
            patientWeight: "15 kg",
            patientHeight: "100 cm",
            patientSex: "female",
            simulationInstructions: `
- No change in patient state if bronchodialators are administered.
- The patient's mother is present and can answer basic questions about the patient's history - is extremely worried, panicked, stressed - \"hasn't been herself today\". 
- When first given fluids, rapid change: pulse 150 bpm, BP 80/50, cap refill 4 seconds. 
- Second fluids: pulse to 140bpm.
- No immediate change if antibiotics are administered.`,
            initialVitalSigns: {
                temperature: "38.4°C",
                heartRate: "170 bpm",
                respiratoryRate: "50 breaths/min",
                bloodPressure: "70/50 mmHg",
                bloodGlucose: "240 mg/dL",
                oxygenSaturation: "85%",
                capillaryRefill: "3 seconds"
            },
            initialABCDE: {
                A: "Snoring/gurgling sounds. No free airway.",
                B: "Intercostal and jugular retractions. Decreased air entry with bilateral ronchi and slight wheezing, symmetrical.",
                C: "Greypale skin. Cold and slightly mottled extremities. No signs of organ enlargement.",
                D: "P on AVPU scale (responds to pain stimuli). Pupils are normal.",
                E: "No rash, no bruising or sores."
            },
            futureEvents: "Tonic-clonic seizure if blood glucose isn't resolved by @ 8 minutes. If seizure is resolved, patient enters persistent hypotension.",
            futureVitalSigns: {
                temperature: "39.5°C @ 10 minutes",
                heartRate: "220 bpm @ 5 minutes",
                respiratoryRate: "55 breaths/min @ 7 minutes",
                bloodPressure: "60/30 mmHg @ 3 minutes",
                bloodGlucose: "No change",
                oxygenSaturation: "63% @ 5 minutes",
                capillaryRefill: "6 seconds @ 3 minutes"
            },
            futureABCDE: {
                A: "No change",
                B: "No change",
                C: "No change",
                D: "U on AVPU scale (unresponsive). @ 5 minutes",
                E: "No change"
            }
        };

        useExerciseStore.setState({ exerciseData: tempExercise });
    }, []);


    const handleDataSubmission = async (data: typeof basicExerciseData) => {
        // Update the central formData with data from the form component
        setBasicExerciseData(data);
        setFormStage(FormStage.Generating);
        console.log("Form data submitted:", data);

        await new Promise(resolve => setTimeout(resolve, 3000)); // 2 seconds delay
        setFormStage(FormStage.EvaluateGeneratedExercise);
    };

    return (
        <div className='overflow-hidden'>
        <AnimatePresence mode="wait">
            {formStage === FormStage.Initial && (
                <motion.div
                    key="initialForm"
                    initial={{ x: '100%' }}
                    animate={{ x: '0%' }}
                    exit={{ x: '-100%' }}
                    transition={{ duration: 0.5 }}
                >
                    <InitialParametersForm onSubmit={handleDataSubmission} defaultData={basicExerciseData} />
                </motion.div>
            )}

            {formStage === FormStage.Generating && (
                <motion.div
                    key="generating"
                    initial={{ x: '100%' }}
                    animate={{ x: '0%' }}
                    exit={{ x: '-100%' }}
                    transition={{ duration: 0.5 }}
                >
                    <InitialGenerationLoader data={basicExerciseData} />
                </motion.div>
            )}

            {formStage === FormStage.EvaluateGeneratedExercise && (
                <motion.div
                    key="nextForm"
                    initial={{ x: '100%' }}
                    animate={{ x: '0%' }}
                    exit={{ x: '-100%' }}
                    transition={{ duration: 0.5 }}
                >
                    <ExerciseReview />
                </motion.div>
            )}
        </AnimatePresence>
        </div>
    );
};

export default FormContainer;
