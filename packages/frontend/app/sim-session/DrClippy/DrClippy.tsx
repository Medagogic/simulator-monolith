"use client";

import React, { useEffect, useState } from 'react';
import { useChatterIO } from '@/app/socketio/SocketContext';
import { useDrClippyStore } from '@/app/storage/DrClippyStore';


interface SuggestionProps {
    advice: string;
    onClick: (advice: string) => void;
}

const Suggestion: React.FC<SuggestionProps> = ({ advice, onClick }) => (
    <div 
        onClick={() => onClick(advice)} 
        className="bg-green-600 p-2 my-1 rounded-md cursor-pointer hover:bg-gray-600 transition-all"
    >
        <p className="text-white text-xs">{advice}</p>
        {/* <p className="text-gray-400 text-xs mt-1">{advice}</p> */}
    </div>
);

interface ClippyProps {
    onClick: (data: { description: string; command: string }) => void;
}

const DrClippySuggestions: React.FC<ClippyProps> = ({ onClick }) => {
    const drClippyOutput = useDrClippyStore((state) => state.drClippyOutput);
    const chatterIO = useChatterIO();

    useEffect(() => {
        console.log("drClippyOutput", drClippyOutput);
    }, [drClippyOutput]);

    function handleClick(advice: string) {
        // onClick(data);
        // const updatedSuggestions = suggestions.filter((suggestion) => suggestion.command !== data.command);
        // setSuggestions(updatedSuggestions);

        if (chatterIO) {
            // chatterIO.sendMessage(advice);
        } else {
            throw new Error("chatterIO is null");
        }
    }

   return (
    <div className="bg-gray-700 rounded-md p-2">
        {drClippyOutput != null && drClippyOutput.advice != null && (
            <>
            <p className="text-white text-m font-semibold">Advisor</p>
        {drClippyOutput!.advice.map((suggestion, index) => (
            <Suggestion 
                key={index}
                advice={suggestion}
                onClick={handleClick}
            />
        ))}
        </>
        )}
    </div>
   );
};

export default DrClippySuggestions;
