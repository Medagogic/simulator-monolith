"use client"

import React, { useState, useEffect } from 'react';
import { InfinitySpin } from 'react-loader-spinner';
import { InitialParametersFormState } from './InitialParametersForm';
import "./InitialGenerationLoader.css"


interface DataDisplayProps {
    data: InitialParametersFormState;
}

const InitialGenerationLoader: React.FC<DataDisplayProps> = ({ data }) => {
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Simulate some data fetching
        const timer = setTimeout(() => setIsLoading(false), 2000);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="flex justify-center items-center min-h-screen flex-col">
            <div className='prose'>
            <h1>Generating Exercise...</h1>
            <div className="p-4 info-container">
                <div className="mb-2">
                    <strong>Age:</strong> {data.age}
                </div>
                <div className="mb-2">
                    <strong>Sex:</strong> {data.sex}
                </div>
                <div className="mb-2">
                    <strong>Description:</strong> {data.description}
                </div>
                <div className="mb-2">
                    <strong>Simulation Instructions:</strong> {data.simulationInstructions}
                </div>
                <div className="mb-2">
                    <strong>Weight:</strong> {data.weight} kg
                </div>
                <div className="mb-2">
                    <strong>Height:</strong> {data.height} cm
                </div>
            </div>
            </div>
            <InfinitySpin
                width='200'
                color="grey"
            />
        </div>
    );
};

export default InitialGenerationLoader;
