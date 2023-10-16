"use client"

import { useState, FC } from 'react';
import { parse as marked } from 'marked';
import "./ExerciseReview.css";
import SectionWrapper from './SectionWrapper';
import { useExerciseStore } from './ExerciseStore';
import ABCDERenderer from './ABCDERenderer';
import VitalsRenderer from './VitalsRenderer';


type SectionData = {
    open: boolean;
    edited: boolean;
};


const ExerciseReview: FC = () => {
    const { exerciseData } = useExerciseStore(state => ({ exerciseData: state.exerciseData }));
    const [sectionsState, setSectionsState] = useState<Record<string, SectionData>>({
        basic: { open: false, edited: false },
        background: { open: false, edited: false },
        instructions: { open: false, edited: false },
        initialVital: { open: false, edited: false },
        initialABCDE: { open: false, edited: false },
        future: { open: false, edited: false }
    });

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

    // const handleStatusChange = (section: string, status: SectionStatus, comment: string) => {
    //     // You might want to handle status as well if needed
    //     setComments({ ...comments, [section]: comment || '' });
    // }

    const toggleSection = (section: string) => {
        const updatedState = { ...sectionsState };
        updatedState[section].open = !updatedState[section].open;
        setSectionsState(updatedState);
    };

    const handleStatusChange = (section: string, comment: string) => {
        setComments({ ...comments, [section]: comment || '' });

        const updatedState = { ...sectionsState };
        updatedState[section].edited = true;
        setSectionsState(updatedState);
    };

    const setEdited = (section: string) => {
        const updatedState = { ...sectionsState };
        updatedState[section].edited = true;
        setSectionsState(updatedState);
    }

    return (
        <div className="p-6 bg-gray-100 min-h-screen">
            {/* Basic Information */}
            <SectionWrapper
                title="Basic Information"
                onStatusChange={(status, comment) => handleStatusChange('basic', comment)}
                isOpen={sectionsState.basic.open}
                isEdited={sectionsState.basic.edited}
                onToggle={() => toggleSection('basic')}>
                <p><strong>Name:</strong> {exerciseData.patientName}</p>
                <p><strong>Age:</strong> {exerciseData.basicInfo.age}</p>
                <p><strong>Sex:</strong> {exerciseData.basicInfo.sex}</p>
                <p><strong>Height:</strong> {exerciseData.basicInfo.height}</p>
                <p><strong>Weight:</strong> {exerciseData.basicInfo.weight}</p>
            </SectionWrapper>

            {/* Background Information */}
            <SectionWrapper
                title="Background Information"
                onStatusChange={(status, comment) => handleStatusChange('background', comment)}
                isOpen={sectionsState.background.open}
                isEdited={sectionsState.background.edited}
                onToggle={() => toggleSection('background')}
                >
                <p>{exerciseData.backgroundInformation}</p>
            </SectionWrapper>

            {/* Simulation Instructions */}
            <SectionWrapper
                title="Simulation Instructions"
                onStatusChange={(status, comment) => handleStatusChange('instructions', comment)}
                isOpen={sectionsState.instructions.open}
                isEdited={sectionsState.instructions.edited}
                onToggle={() => toggleSection('instructions')}
                >
                <div
                    className="markdown-content"
                    dangerouslySetInnerHTML={{ __html: marked(exerciseData.simulationInstructions) }}
                ></div>
            </SectionWrapper>

            {/* Initial Vital Signs */}
            <SectionWrapper
                title="Initial Vital Signs"
                onStatusChange={(status, comment) => handleStatusChange('initialVital', comment)}
                isOpen={sectionsState.initialVital.open}
                isEdited={sectionsState.initialVital.edited}
                onToggle={() => toggleSection('initialVital')}
                >
                <VitalsRenderer vitalData={exerciseData.vitalSigns} onChange={(key, value) => {
                    useExerciseStore.setState(state => {
                        setEdited('initialVital');
                        const newExerciseData = { ...state.exerciseData };
                        newExerciseData.vitalSigns[key] = value;
                        return { exerciseData: newExerciseData };
                    });
                }} />
            </SectionWrapper>

            {/* Initial ABCDE */}
            <SectionWrapper
                title="Initial ABCDE"
                onStatusChange={(status, comment) => handleStatusChange('initialABCDE', comment)}
                isOpen={sectionsState.initialABCDE.open}
                isEdited={sectionsState.initialABCDE.edited}
                onToggle={() => toggleSection('initialABCDE')}
                >
                <ABCDERenderer abcdeData={exerciseData.aBCDE} onChange={(key, value) => {
                    useExerciseStore.setState(state => {
                        setEdited('initialABCDE');
                        const newExerciseData = { ...state.exerciseData };
                        newExerciseData.aBCDE[key] = value;
                        return { exerciseData: newExerciseData };
                    });
                }} />
            </SectionWrapper>

            {/* Future Section */}
            <SectionWrapper
                title="Future Section"
                onStatusChange={(status, comment) => handleStatusChange('future', comment)}
                isOpen={sectionsState.future.open}
                isEdited={sectionsState.future.edited}
                onToggle={() => toggleSection('future')}
                >
                {/* Future Events */}
                <div className="mb-6">
                    <h3 className="text-xl font-medium mb-2">Events</h3>
                    <div
                        className="markdown-content"
                        dangerouslySetInnerHTML={{ __html: marked(exerciseData.future.events) }}
                    ></div>
                </div>

                {/* Future Vital Signs */}
                <div className="mb-6">
                    <h3 className="text-xl font-medium mb-2">Future Vital Signs</h3>
                    <VitalsRenderer vitalData={exerciseData.future.vitalSigns} onChange={(key, value) => {
                        useExerciseStore.setState(state => {
                            
                            const newExerciseData = { ...state.exerciseData };
                            newExerciseData.future.vitalSigns[key] = value;
                            return { exerciseData: newExerciseData };
                        });
                    }} />
                </div>

                {/* Future ABCDE */}
                <div>
                    <h3 className="text-xl font-medium mb-2">Future ABCDE</h3>
                    <ABCDERenderer abcdeData={exerciseData.future.aBCDE} onChange={(key, value) => {
                        useExerciseStore.setState(state => {
                            setEdited('future');
                            const newExerciseData = { ...state.exerciseData };
                            newExerciseData.future.aBCDE[key] = value;
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
