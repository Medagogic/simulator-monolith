"use client"
import React, { useState } from 'react';
import DragDropPage from "./DragDropPage"

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
            <div className={`${draggingComplete ? 'opacity-0' : 'opacity-100'} transition-opacity duration-500`}>
                <DragDropPage onFileProcessedCallback={handleFileDropped} />
            </div>
            <div className={`${generatingExercise ? 'opacity-100' : 'opacity-0'} absolute transition-opacity duration-500 text-white text-xl`}>
                Generating exercise...
            </div>
            <div className={`${finishedGenerating ? 'opacity-100' : 'opacity-0'} absolute transition-opacity duration-500 text-white text-xl`}>
                Exercise generated!
            </div>
        </div>
    );
};

export default SlideshowPage;
