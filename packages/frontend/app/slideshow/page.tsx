"use client"

import React, { useState, useEffect, useCallback } from 'react';

import DragDropPage from "./DragDropPage";
import ScenarioReviewPage from './scenario-review/page';
import Slideshow from './Slideshow';
import { useSearchParams, useRouter, usePathname } from 'next/navigation';

enum SlideshowState {
    Slideshow1 = 'slideshow1',
    DragDropDocument = 'dragdrop',
    GeneratingExercise = 'generating',
    ReviewingScenarios = 'reviewing',
}

const SlideshowPage: React.FC = () => {
    const router = useRouter();
    const searchParams = useSearchParams();
    const pathname = usePathname();

    const [currentState, setCurrentState] = useState(SlideshowState.Slideshow1);

    const createQueryString = useCallback(
        (name: string, value: string) => {
            const params = new URLSearchParams(searchParams)
            params.set(name, value)
            return params.toString()
        },
        [searchParams]
    )

    function toSlideshowState(value: string): SlideshowState {
        const state = (Object.values(SlideshowState) as string[]).includes(value) ? value as SlideshowState : undefined;
        if (state) {
            return state;
        } else {
            return SlideshowState.Slideshow1;
        }
      }

    const getInitialState = (): SlideshowState => {
        const stateParam = searchParams.get('state');
        if (!stateParam) {
            return SlideshowState.Slideshow1;
        }

        console.log("State param: `" + stateParam + "`");
        return toSlideshowState(stateParam);
    };

    useEffect(() => {
        const nextState = getInitialState();
        if (currentState !== nextState) {
            goToState(nextState);
        }
    }, [searchParams]);

    function goToState(state: SlideshowState) {
        router.push(pathname + '?' + createQueryString('state', state));
        setCurrentState(state);
    }

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
                timers.push(setTimeout(() => goToState(SlideshowState.ReviewingScenarios), generationTime));
                break;

            case SlideshowState.ReviewingScenarios:
                break;

            default:
                return;
        }

        return () => timers.forEach(timer => clearTimeout(timer));

    }, [currentState]);

    const handleFileDropped = () => {
        goToState(SlideshowState.GeneratingExercise);
    };

    function handleFirstSlidshowEnd() {
        console.log("First slideshow ended");
        goToState(SlideshowState.DragDropDocument)
    }

    function stateClassName(state: SlideshowState): string {
        return `${currentState === state ? 'opacity-100 z-10' : 'opacity-0'} transition-opacity duration-500 absolute`;
    }

    return (
        <div className="h-screen w-screen flex items-center justify-center bg-gray-700">
            <div className={`${stateClassName(SlideshowState.Slideshow1)}`}>
                <Slideshow onEnd={handleFirstSlidshowEnd} start_index={0} end_index={4} />
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
