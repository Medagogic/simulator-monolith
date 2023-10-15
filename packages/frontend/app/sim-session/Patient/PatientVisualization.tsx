"use client"

import React, { useState } from 'react';
import patientImage from './patient.png';
import patientSkinBasic from './patient-skin-basic.png';
import patientBlueOverlay from "./patient-body-blue.png";
import { StaticImageData } from 'next/image';

type LayeredImage = {
    img: StaticImageData;
    alt: string;
};

type Label = {
    text: string;
    x: number;
    y: number;
};

const PatientVisualization: React.FC = () => {
    const labels: Label[]  = [
        { text: 'Head', x: 50, y: 10 },
        { text: 'Heart', x: 50, y: 70 },
        // ... more labels ...
    ];
    
    const layers: LayeredImage[] = [
        { img: patientImage, alt: "Base patient" },
        { img: patientSkinBasic, alt: "Patient skin" },
        { img: patientBlueOverlay, alt: "Patient blue overlay"}
        // ... other layers here in order
    ];

    return (
        <div className="relative w-full h-full border rounded-lg" title="Bed">
            <div className="absolute inset-0 w-full h-full bg-[#ebfff8]"> 
                {/* The background color is using JIT compilation syntax, ensure you are using Tailwind CSS v2.1.0 or later */}
                {layers.map((layer, index) => (
                    <img 
                        key={index}
                        src={layer.img.src} 
                        alt={layer.alt} 
                        className="absolute top-0 left-0 h-full w-auto object-cover" 
                        style={{ zIndex: index + 1 }} // Inline style for zIndex as there's no direct utility for it in Tailwind
                    />
                ))}

{labels.map((label) => (
                    <div 
                        key={label.id}
                        className="absolute"
                        style={{ left: `${label.x}px`, top: `${label.y}px` }} // positions label based on coordinates
                    >
                        <div className="bg-white rounded px-2 py-1 shadow text-xs" draggable>
                            {label.text}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PatientVisualization;
