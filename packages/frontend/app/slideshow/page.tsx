"use client"
import React, { useState, useEffect } from 'react';
import DragDropPage from "./DragDropPage";
import ScenarioReviewPage from './scenario-review/page';
import Slideshow from './Slideshow';

enum SlideshowState {
    Slideshow1,
    DragDropDocument,
    GeneratingExercise,
    ReviewingScenarios,
}

const SlideshowPage: React.FC = () => {
    const [currentState, setCurrentState] = useState(SlideshowState.Slideshow1);

    useEffect(() => {
        const fadeGap = 500;

        const timers: NodeJS.Timeout[] = [];

        switch (currentState) {
            case SlideshowState.Slideshow1:
                return;

            case SlideshowState.DragDropDocument:
                return;

            case SlideshowState.GeneratingExercise:
                const generationTime = 2000;
                timers.push(setTimeout(() => setCurrentState(SlideshowState.ReviewingScenarios), generationTime));
                break;

            case SlideshowState.ReviewingScenarios:
                // Additional logic if any
                break;

            default:
                return;
        }

        return () => timers.forEach(timer => clearTimeout(timer));

    }, [currentState]);

    const handleFileDropped = () => {
        setCurrentState(SlideshowState.GeneratingExercise);
    };

    function handleFirstSlidshowEnd() {
        console.log("First slideshow ended");
        setCurrentState(SlideshowState.DragDropDocument)
    }

    function stateClassName(state: SlideshowState): string {
        return `${currentState === state ? 'opacity-100 z-10' : 'opacity-0'} transition-opacity duration-500 absolute`;
    }

    return (
        <div className="h-screen w-screen flex items-center justify-center bg-gray-700">
            <div className={`${stateClassName(SlideshowState.Slideshow1)}`}>
                <Slideshow onEnd={handleFirstSlidshowEnd}/>
            </div>
            <div className={`${stateClassName(SlideshowState.DragDropDocument)}`}>
                <DragDropPage onFileProcessedCallback={handleFileDropped} />
            </div>
            <div className={`${stateClassName(SlideshowState.GeneratingExercise)} text-white text-xl`}>
                Generating scenarios...
            </div>
            <div className={`${stateClassName(SlideshowState.ReviewingScenarios)} text-white`}>
                <ScenarioReviewPage />
            </div>
        </div>
    );
};

export default SlideshowPage;
