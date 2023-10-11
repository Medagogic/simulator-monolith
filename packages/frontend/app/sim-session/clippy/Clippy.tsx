"use client";

import React, { useState } from 'react';
import mockData from "./mock.json";
import { useChatStore } from '@/app/chatter/ChatStore';

const clippy = mockData;

interface SuggestionProps {
    data: { description: string; command: string };
    onClick: (data: { description: string; command: string }) => void;
}

const Suggestion: React.FC<SuggestionProps> = ({ data, onClick }) => (
    <div 
        onClick={() => onClick(data)} 
        className="bg-gray-700 p-2 my-1 rounded-md cursor-pointer hover:bg-gray-600 transition-all"
    >
        <p className="text-white text-sm font-semibold">{data.description}</p>
        <p className="text-gray-400 text-xs mt-1">{data.command}</p>
    </div>
);

interface ClippyProps {
    onClick: (data: { description: string; command: string }) => void;
}

const Clippy: React.FC<ClippyProps> = ({ onClick }) => {
    const [suggestions, setSuggestions] = useState(clippy.suggestions);
    const sendMessage = useChatStore((state) => state.sendMessage);

    function handleClick(data: { description: string; command: string }) {
        sendMessage(data.command);
        onClick(data);
        const updatedSuggestions = suggestions.filter((suggestion) => suggestion.command !== data.command);
        setSuggestions(updatedSuggestions);
    }

   return (
    <div className="bg-#222 rounded-lg">
        {/* <h2 className="text-white text-sm font-bold mb-3">Advisor</h2> */}
        {suggestions.map((suggestion, index) => (
            <Suggestion 
                key={index}
                data={suggestion}
                onClick={handleClick}
            />
        ))}
    </div>
   );
};

export default Clippy;
