"use client"
import React, { useState } from 'react';
import DragDropPage from "./DragDropPage"
import NeonateInfo from './NeonatInfo';

const SlideshowPage: React.FC = () => {
    const [draggingComplete, setDraggingComplete] = useState(false);
    const [generatingExercise, setGeneratingExercise] = useState(false);
    const [finishedGenerating, setFinishedGenerating] = useState(false);

    const handleFileDropped = () => {
        setDraggingComplete(true);

        const fade_gap = 500;

        setTimeout(() => {
            setGeneratingExercise(true);

            setTimeout(() => {
                setGeneratingExercise(false);

                setTimeout(() => {
                    setFinishedGenerating(true);
                }, fade_gap);
            }, 2000)
        }, fade_gap);
    };

    return (
        <div className="h-screen w-screen flex items-center justify-center bg-gray-700">
            <div className={`${draggingComplete ? 'opacity-0' : 'opacity-100'} transition-opacity duration-500 z-10`}>
                <DragDropPage onFileProcessedCallback={handleFileDropped} />
            </div>
            <div className={`${generatingExercise ? 'opacity-100' : 'opacity-0'} absolute transition-opacity duration-500 text-white text-xl`}>
                Generating exercises...
            </div>
            <div className={`${finishedGenerating ? 'opacity-100' : 'opacity-0'} absolute transition-opacity duration-500 text-white text-xl`}>
                <div className='flex flex-col justify-center'>
                    <div className="text-white text-2xl font-semibold mb-4">Generated 5 exercises!</div>
                    <ul className="list-decimal list-inside">
                        <li className="text-white text-xl">Neonate - Hypoxic-Ischemic Encephalopathy (HIE)</li>
                        <li className="text-white text-xl">Infant - Febrile Seizure</li>
                        <li className="text-white text-xl">Toddler - Dravet Syndrome</li>
                        <li className="text-white text-xl">School-Aged Child - Previous Brain Injury</li>
                        <li className="text-white text-xl">Early-Teen - Unknown Seizure Etiology</li>
                    </ul>
                    <NeonateInfo />
                </div>
            </div>
        </div>
    );
};

export default SlideshowPage;
