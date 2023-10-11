"use client";

import React from 'react';
import mockData from "./mock.json";

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

const Clippy: React.FC<ClippyProps> = ({ onClick }) => (
    <div className="bg-#222 rounded-lg">
        {/* <h2 className="text-white text-sm font-bold mb-3">Advisor</h2> */}
        {clippy.suggestions.map((suggestion, index) => (
            <Suggestion 
                key={index}
                data={suggestion}
                onClick={onClick}
            />
        ))}
    </div>
);

export default Clippy;
