"use client"

import { useState, FC } from 'react';
import { parse as marked } from 'marked';
import "./ExerciseReview.css";
import SectionWrapper, { SectionStatus } from './SectionWrapper';
import { VitalSigns, vitalSignsLabels } from './ExerciseTypes';
import { useExerciseStore } from './ExerciseStore';
import ABCDERenderer from './ABCDERenderer';
import VitalsRenderer from './VitalsRenderer';


const ExerciseReview: FC = () => {
    const sections = ['basic', 'background', 'instructions', 'initialVital', 'initialABCDE', 'future'];
    const { exerciseData } = useExerciseStore(state => ({ exerciseData: state.exerciseData }));

    // 1. Create a state to hold the comments for each section
    const [comments, setComments] = useState<Record<string, string>>({
        basic: '',
        background: '',
        instructions: '',
        initialVital: '',
        initialABCDE: '',
        future: ''
    });

    // 2. Add a function to check if any comments have been written
    const hasComments = () => {
        return Object.values(comments).some(comment => comment.trim().length > 0);
    };

    const handleSubmit = () => {
        // 3. Send the comments to the server
        console.log(comments);
    }

    const handleStatusChange = (section: string, status: SectionStatus, comment: string) => {
        // You might want to handle status as well if needed
        setComments({ ...comments, [section]: comment || '' });
    }

    return (
        <div className="p-6 bg-gray-100 min-h-screen">
            {/* Basic Information */}
            <SectionWrapper
                title="Basic Information"
                onStatusChange={(status, comment) => handleStatusChange('basic', status, comment)}>
                <p><strong>Name:</strong> {exerciseData.patientName}</p>
                <p><strong>Age:</strong> {exerciseData.patientAge}</p>
                <p><strong>Sex:</strong> {exerciseData.patientSex}</p>
                <p><strong>Height:</strong> {exerciseData.patientHeight}</p>
                <p><strong>Weight:</strong> {exerciseData.patientWeight}</p>
            </SectionWrapper>

            {/* Background Information */}
            <SectionWrapper
                title="Background Information"
                onStatusChange={(status, comment) => handleStatusChange('background', status, comment)}>
                <p>{exerciseData.backgroundInformation}</p>
            </SectionWrapper>

            {/* Simulation Instructions */}
            <SectionWrapper
                title="Simulation Instructions"
                onStatusChange={(status, comment) => handleStatusChange('instructions', status, comment)}>
                <div
                    className="markdown-content"
                    dangerouslySetInnerHTML={{ __html: marked(exerciseData.simulationInstructions) }}
                ></div>
            </SectionWrapper>

            {/* Initial Vital Signs */}
            <SectionWrapper
                title="Initial Vital Signs"
                onStatusChange={(status, comment) => handleStatusChange('initialVital', status, comment)}>
                <VitalsRenderer vitalData={exerciseData.initialVitalSigns} onChange={(key, value) => {
                    useExerciseStore.setState(state => {
                        const newExerciseData = { ...state.exerciseData };
                        newExerciseData.initialVitalSigns[key] = value;
                        return { exerciseData: newExerciseData };
                    });
                }} />
            </SectionWrapper>

            {/* Initial ABCDE */}
            <SectionWrapper
                title="Initial ABCDE"
                onStatusChange={(status, comment) => handleStatusChange('initialABCDE', status, comment)}>
                <ABCDERenderer abcdeData={exerciseData.initialABCDE} onChange={(key, value) => {
                    useExerciseStore.setState(state => {
                        const newExerciseData = { ...state.exerciseData };
                        newExerciseData.initialABCDE[key] = value;
                        return { exerciseData: newExerciseData };
                    });
                }} />
            </SectionWrapper>

            {/* Future Section */}
            <SectionWrapper
                title="Future Section"
                onStatusChange={(status, comment) => handleStatusChange('future', status, comment)}>
                {/* Future Events */}
                <div className="mb-6">
                    <h3 className="text-xl font-medium mb-2">Events</h3>
                    <div
                        className="markdown-content"
                        dangerouslySetInnerHTML={{ __html: marked(exerciseData.futureEvents) }}
                    ></div>
                </div>

                {/* Future Vital Signs */}
                <div className="mb-6">
                    <h3 className="text-xl font-medium mb-2">Future Vital Signs</h3>
                    <VitalsRenderer vitalData={exerciseData.futureVitalSigns} onChange={(key, value) => {
                        useExerciseStore.setState(state => {
                            const newExerciseData = { ...state.exerciseData };
                            newExerciseData.futureVitalSigns[key] = value;
                            return { exerciseData: newExerciseData };
                        });
                    }} />
                </div>

                {/* Future ABCDE */}
                <div>
                    <h3 className="text-xl font-medium mb-2">Future ABCDE</h3>
                    <ABCDERenderer abcdeData={exerciseData.futureABCDE} onChange={(key, value) => {
                        useExerciseStore.setState(state => {
                            const newExerciseData = { ...state.exerciseData };
                            newExerciseData.futureABCDE[key] = value;
                            return { exerciseData: newExerciseData };
                        });
                    }} />
                </div>
            </SectionWrapper>


            <button className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-md"
                onClick={handleSubmit}>
                {hasComments() ? 'Regenerate' : 'Accept'}
            </button>
        </div>
    );
};

export default ExerciseReview;
