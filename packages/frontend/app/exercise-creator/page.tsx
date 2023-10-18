"use client"

import React, { useEffect, useState } from 'react';
import InitialParametersForm, { generateDefaultData, InitialParametersFormState } from './InitialParametersForm';
import { motion, AnimatePresence } from 'framer-motion';
import InitialGenerationLoader from './InitialGenerationLoader';
import ExerciseReview from './ExerciseReview';
import { useExerciseStore } from './ExerciseStore';
import { DefaultApi, Configuration, ExerciseCreationParams, ExerciseCreationPatientBasicInfo, ErrorContext } from "@/src/api";


enum FormStage {
    Initial,
    Generating,
    EvaluateGeneratedExercise
}

const FormContainer: React.FC = () => {
    const [basicExerciseData, setBasicExerciseData] = useState<InitialParametersFormState>(generateDefaultData("3 years"));
    const [formStage, setFormStage] = useState<FormStage>(FormStage.Initial);
    // const [generatedExercise, setGeneratedExercise] = useState<GeneratedExerciseData | null>(null);

    const api = new DefaultApi(new Configuration({
        basePath: 'http://localhost:5000',
        middleware: [
            {
                async onError(context: ErrorContext) {
                    console.log(context.error);
                }
            }
        ]
    }));


    const handleDataSubmission = async (data: typeof basicExerciseData) => {
        // Update the central formData with data from the form component
        setBasicExerciseData(data);
        setFormStage(FormStage.Generating);
        console.log("Form data submitted:", data);

        // await new Promise(resolve => setTimeout(resolve, 3000)); // 2 seconds delay

        const basicInfo: ExerciseCreationPatientBasicInfo = {
            age: data.age,
            weight: `${data.weight} kg`,
            height: `${data.height} cm`,
            sex: data.sex
        }
        const params: ExerciseCreationParams = {
            basicInfo: basicInfo,
            exerciseDescription: data.description,
            simulationInstructions: data.simulationInstructions,
        }
        console.log(params);
        const generatedExercise = await api.handleGenerateStaticApiGenerateExercisePost({
            exerciseCreationParams: params
        });

        useExerciseStore.setState({ exerciseData: generatedExercise });

        await new Promise(resolve => setTimeout(resolve, 1000));
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
