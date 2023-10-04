"use client"

import React, { useEffect, useState } from 'react';
import InitialParametersForm, { generateDefaultData, InitialParametersFormState } from './InitialParametersForm';
import { motion, AnimatePresence } from 'framer-motion';


enum FormStage {
    Initial,
    Generating,
    NextForm
}

const FormContainer: React.FC = () => {
    const [basicExerciseData, setBasicExerciseData] = useState<InitialParametersFormState>(generateDefaultData("3 years"));
    const [formStage, setFormStage] = useState<FormStage>(FormStage.Initial);


    const handleDataSubmission = async (data: typeof basicExerciseData) => {
        // Update the central formData with data from the form component
        setBasicExerciseData(data);
        setFormStage(FormStage.Generating);
        console.log("Form data submitted:", data);

        await new Promise(resolve => setTimeout(resolve, 3000)); // 2 seconds delay
        setFormStage(FormStage.NextForm);
    };

    return (
        // <InitialParametersForm onSubmit={handleDataSubmission} defaultData={initialParameters} />

        <div className='overflow-hidden'>
        <AnimatePresence mode="sync">
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
                    {basicExerciseData.age}
                    Generating...
                </motion.div>
            )}

            {formStage === FormStage.NextForm && (
                <motion.div
                    key="nextForm"
                    initial={{ x: '100%' }}
                    animate={{ x: '0%' }}
                    exit={{ x: '-100%' }}
                    transition={{ duration: 0.5 }}
                >
                    {/* Your next form goes here */}
                    Next Form Content...
                </motion.div>
            )}
        </AnimatePresence>
        </div>
    );
};

export default FormContainer;
