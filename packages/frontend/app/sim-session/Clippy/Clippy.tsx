"use client";

import React, { useState } from 'react';
import { useChatStore } from '@/app/chatter/ChatStore';
import { useChatterIO } from '@/app/socketio/SocketContext';

const clippy = {
    "suggestions": [
        {
            "description": "Introduce yourself to the team",
            "command": "Hi, I'm your team lead. Let's start by introducing ourselves."
        },
        {
            "description": "Start by assessing the airway",
            "command": "Nurse, please assess the airway patency."
        },
        {
            "description": "Prepare IV fluids",
            "command": "Let's prepare IV fluids please."
        }
    ]
}

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
    const chatterIO = useChatterIO();

    function handleClick(data: { description: string; command: string }) {
        onClick(data);
        const updatedSuggestions = suggestions.filter((suggestion) => suggestion.command !== data.command);
        setSuggestions(updatedSuggestions);

        if (chatterIO) {
            chatterIO.sendMessage(data.command);
        } else {
            throw new Error("chatterIO is null");
        }
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
