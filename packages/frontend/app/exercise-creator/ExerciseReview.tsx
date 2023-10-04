"use client"

import { useState, FC } from 'react';
import { parse as marked } from 'marked';
import "./ExerciseReview.css";
import SectionWrapper, { SectionStatus } from './SectionWrapper';

type VitalSigns = {
    temperature: string;
    heartRate: string;
    respiratoryRate: string;
    bloodPressure: string;
    bloodGlucose: string;
    oxygenSaturation: string;
    capillaryRefill: string;
};

const vitalSignsLabels: { [key in keyof VitalSigns]: string } = {
    temperature: "Temperature",
    heartRate: "Heart Rate",
    respiratoryRate: "Respiratory Rate",
    bloodPressure: "Blood Pressure",
    bloodGlucose: "Blood Glucose",
    oxygenSaturation: "Oxygen Saturation",
    capillaryRefill: "Capillary Refill",
};

type ABCDE = {
    A: string;
    B: string;
    C: string;
    D: string;
    E: string;
};

export type GeneratedExerciseData = {
    patientName: string;
    patientAge: string;
    patientSex: string;
    patientHeight: string;
    patientWeight: string;
    backgroundInformation: string;
    simulationInstructions: string;
    initialVitalSigns: VitalSigns;
    initialABCDE: ABCDE;
    futureEvents: string;
    futureVitalSigns: VitalSigns;
    futureABCDE: ABCDE;
};

const ExerciseReview: FC<{ data: GeneratedExerciseData }> = ({ data }) => {
    const sections = ['basic', 'background', 'instructions', 'initialVital', 'initialABCDE', 'future'];

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
                <p><strong>Name:</strong> {data.patientName}</p>
                <p><strong>Age:</strong> {data.patientAge}</p>
                <p><strong>Sex:</strong> {data.patientSex}</p>
                <p><strong>Height:</strong> {data.patientHeight}</p>
                <p><strong>Weight:</strong> {data.patientWeight}</p>
            </SectionWrapper>

            {/* Background Information */}
            <SectionWrapper
                title="Background Information"
                onStatusChange={(status, comment) => handleStatusChange('background', status, comment)}>
                <p>{data.backgroundInformation}</p>
            </SectionWrapper>

            {/* Simulation Instructions */}
            <SectionWrapper
                title="Simulation Instructions"
                onStatusChange={(status, comment) => handleStatusChange('instructions', status, comment)}>
                <div
                    className="markdown-content"
                    dangerouslySetInnerHTML={{ __html: marked(data.simulationInstructions) }}
                ></div>
            </SectionWrapper>

            {/* Initial Vital Signs */}
            <SectionWrapper
                title="Initial Vital Signs"
                onStatusChange={(status, comment) => handleStatusChange('initialVital', status, comment)}>
                <ul>
                    {Object.entries(data.initialVitalSigns).map(([key, value]) => (
                        <li key={key}><strong>{vitalSignsLabels[key as keyof VitalSigns]}:</strong> {value}</li>
                    ))}
                </ul>
            </SectionWrapper>

            {/* Initial ABCDE */}
            <SectionWrapper
                title="Initial ABCDE"
                onStatusChange={(status, comment) => handleStatusChange('initialABCDE', status, comment)}>
                <ul>
                    {Object.entries(data.initialABCDE).map(([key, value]) => (
                        <li key={key}><strong>{key}:</strong> {value}</li>
                    ))}
                </ul>
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
                        dangerouslySetInnerHTML={{ __html: marked(data.futureEvents) }}
                    ></div>
                </div>

                {/* Future Vital Signs */}
                <div className="mb-6">
                    <h3 className="text-xl font-medium mb-2">Future Vital Signs</h3>
                    <ul>
                        {Object.entries(data.futureVitalSigns).map(([key, value]) => (
                            <li key={key}><strong>{vitalSignsLabels[key as keyof VitalSigns]}:</strong> {value}</li>
                        ))}
                    </ul>
                </div>

                {/* Future ABCDE */}
                <div>
                    <h3 className="text-xl font-medium mb-2">Future ABCDE</h3>
                    <ul>
                        {Object.entries(data.futureABCDE).map(([key, value]) => (
                            <li key={key}><strong>{key}:</strong> {value}</li>
                        ))}
                    </ul>
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
