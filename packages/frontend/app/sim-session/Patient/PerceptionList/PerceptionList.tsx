
"use client";

import { FiWind } from 'react-icons/fi';
import { BiUser } from 'react-icons/bi';
import { BsLungs, BsEye } from 'react-icons/bs';
import { useState, useEffect } from 'react';

const perceptionData = {
    "Breathing sounds": "Snoring, gurgling, bilateral ronchi, slight wheezing",
    "Consciousness": "Responds to pain stimuli",
    "Chest movements": "Intercostal retractions, jugular retractions",
    "Skin": "Greypale, cold, slightly mottled"
};

const PerceptionList: React.FC = () => {

    const getIconForPerception = (key: string) => {
        let className = "h-5 w-5 text-green-500";

        switch (key) {
            case 'Breathing sounds':
                return <FiWind className={className} />;
            case 'Consciousness':
                return <BsEye className={className} />;
            case 'Chest movements':
                return <BsLungs className={className} />;
            case 'Skin':
                return <BiUser className={className} />;
            default:
                return null;
        }
    };

    return (
        <div className="space-y-2 w-full text-white">
            <style>
                {`
                .alert {
                    mouse-events: none;
                }
                .shimmer {
                    position: absolute;
                    top: 0;
                    right: 0;
                    bottom: 0;
                    left: 0;
                    animation: shimmer 2.5s infinite linear;
                    background-color: #ff2222;
                    opacity: 0;
                    box-shadow: 0 0 10px 0px #ff0000;
                    mouse-events: none;
                  }
                  
                  @keyframes shimmer {
                    0% {
                      opacity: 0;
                    }
                    20% {
                        opacity: 0.2;
                    }
                    40% {
                      opacity: 0;
                    }

                  }
                `}
            </style>

            {Object.entries(perceptionData).map(([key, value], index) => (
                <div key={key} className="relative bg-gray-800 p-2 rounded shadow-md flex items-center space-x-2 alert">
                    <div className={`shimmer`} style={{ animationDelay: `${index / 10}s` }}></div>
                    {getIconForPerception(key)}
                    <div>
                        <div className="font-bold text-m">{key}</div>
                        <div className="text-xs text-gray-300">{value}</div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PerceptionList;