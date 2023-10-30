"use client"

import React, { CSSProperties, useEffect } from 'react';
import patientImage from './patient.png';
import patientSkinBasic from './patient-skin-basic.png';
import patientBlueOverlay from "./patient-body-blue.png";
import { StaticImageData } from 'next/image';
import { TEST_fullConnectionData, useDeviceStore } from '@/app/storage/DeviceStore';
import { SIO_ConnectedDevices, IVAccessParams, IVAccessLocation, IOAccessLocation } from '@/src/scribe/scribetypes';
import PerceptionList from './PerceptionList/PerceptionList';

type LayeredImage = {
    img: StaticImageData;
    alt: string;
};

type Label = {
    component: React.ReactNode; // This will hold the actual component
    x: number; // position
    y: number; // position
};

type SimpleLabelProps = {
    text: string;
    className?: string;
    style?: CSSProperties;
};

const SimpleLabel: React.FC<SimpleLabelProps> = ({ text, className, style }) => {
    return (
        <div
            className={`bg-white rounded px-2 py-1 shadow text-xs scale-90 ${className}`}
            style={style}>
            {text}
        </div>
    );
};

enum CircleLabelStatus {
    Ready = 'ready',
    Pending = 'pending',
    Unavailable = 'unavailable'
}

interface CircleLabelProps {
    label: string;
    status?: CircleLabelStatus;
    tooltip?: string;
}

const CircleLabel: React.FC<CircleLabelProps> = ({ label, status, tooltip }) => {
    // Define color based on IV status
    let bgColor;
    switch (status) {
        case CircleLabelStatus.Ready:
            bgColor = '#28a745'; // green for success/ready
            break;
        case CircleLabelStatus.Pending:
            bgColor = '#ffc107aa'; // yellow for pending
            break;
        case CircleLabelStatus.Unavailable:
        default:
            bgColor = '#dc354566'; // red for inactive
            break;
    }

    const circleStyle = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        width: '30px',
        height: '30px',
        borderRadius: '50%',
        border: '1px solid #000',
        fontSize: '0.75rem',
        color: '#fff', // Let's choose white text color for better contrast
        backgroundColor: bgColor, // Use the dynamic background color
        boxShadow: '0px 0px 2px #888',
        lineHeight: '24px', // This can help in text centering. It should be equal to the height to vertically center the text.
        transform: 'translate(-50%, -50%)', // This is to center the circle
    };

    return (
        <div style={circleStyle} title={`${label} ${tooltip} ${status}`}>
            {label}
        </div>
    );
};


function getIVLabels(connectedDevices: SIO_ConnectedDevices): Label[] {
    const label_locations: { [key in IVAccessLocation]: { x: number, y: number } } = {
        'right hand': { x: 35, y: 53 },
        'left hand': { x: 65, y: 53 }
    };

    if (!connectedDevices.iv_access) {
        return [];
    }

    const labels: Label[] = [];
    connectedDevices.iv_access.forEach((iv, index) => {
        const label = label_locations[iv.location];
        if (label) {
            labels.push({
                component: <CircleLabel label='IV' status={CircleLabelStatus.Ready} />,
                x: label.x,
                y: label.y
            });
        }
    });
    return labels;
}

function getIOLabels(connectedDevices: SIO_ConnectedDevices): Label[] {
    const left_label_locations: { [key in IOAccessLocation]: { x: number, y: number } } = {
        'distal femur': { x: 57, y: 65 },
        'distal tibia': { x: 57, y: 77 },
        'proximal tibia': { x: 57, y: 70 },
    };

    if (!connectedDevices.io_access) {
        return [];
    }

    const labels: Label[] = [];
    connectedDevices.io_access.forEach((io, index) => {
        const label_location = left_label_locations[io.location];
        const x = io.side == 'right' ? label_location.x : 100 - label_location.x;

        if (label_location) {
            labels.push({
                component: <CircleLabel label="IO" status={CircleLabelStatus.Ready} tooltip={`${io.side} ${io.location}`} />,
                x: x,
                y: label_location.y
            });
        }
    });
    return labels;
}


function getEKGLabels(connectedDevices: SIO_ConnectedDevices): Label[] {
    if (!connectedDevices.ekg_connected) {
        return [];
    }

    return [{
        component: <CircleLabel label="EKG" status={CircleLabelStatus.Ready} />,
        x: 50,
        y: 42
    }];
}

function getNIBPLabels(connectedDevices: SIO_ConnectedDevices): Label[] {
    if (!connectedDevices.nibp) {
        return [];
    }

    return [{
        component: <CircleLabel label="NIBP" status={CircleLabelStatus.Ready} />,
        x: 66,
        y: 39
    }];
}

function getPulseOximeterLabels(connectedDevices: SIO_ConnectedDevices): Label[] {
    if (!connectedDevices.nibp) {
        return [];
    }

    return [{
        component: <CircleLabel label="SpO2" status={CircleLabelStatus.Ready} />,
        x: 34,
        y: 59
    }];
}


const PatientVisualization: React.FC = () => {
    const connectedDevices = useDeviceStore(state => state.connectedDevices);
    const setDeviceState = useDeviceStore(state => state.setDeviceState);
    const [labels, setLabels] = React.useState<Label[]>([]);

    useEffect(() => {
        // console.log("Connected devices: ", connectedDevices);

        setLabels(
            getIVLabels(connectedDevices)
                .concat(getIOLabels(connectedDevices))
                .concat(getEKGLabels(connectedDevices))
                .concat(getNIBPLabels(connectedDevices))
                .concat(getPulseOximeterLabels(connectedDevices))
        );
    }, [connectedDevices]);

    useEffect(() => {
        // setDeviceState(TEST_fullConnectionData);
    }, []);

    const static_labels: Label[] = [
        {
            component: <SimpleLabel text="Audible Snoring" />,
            x: 61,
            y: 23
        },
        {
            component: <SimpleLabel text="Shallow breathing" className="transform -translate-x-1/2" />,
            x: 50,
            y: 45
        },
        {
            component: <SimpleLabel text="Eyes open, responsive" className="transform -translate-x-1/2" />,
            x: 50,
            y: 15
        },
    ];

    const layers: LayeredImage[] = [
        { img: patientImage, alt: "Base patient" },
        { img: patientSkinBasic, alt: "Patient skin" },
        { img: patientBlueOverlay, alt: "Patient blue overlay" }
    ];

    const onImageClick = (event: React.MouseEvent<HTMLImageElement>) => {
        const target = event.target as HTMLImageElement;

        // Get the image's bounding box, which contains its dimensions and position info.
        const rect = target.getBoundingClientRect();

        // Calculate click position in the image as a percentage.
        const x = ((event.clientX - rect.left) / rect.width) * 100;
        const y = ((event.clientY - rect.top) / rect.height) * 100;

        // Round the percentages to the nearest integer.
        const roundedX = Math.round(x);
        const roundedY = Math.round(y);

        // Create the label template
        const labelTemplate = `{ text: 'New Label', x: ${roundedX}, y: ${roundedY} }`;

        // Log the template to the console for easy copying.
        console.log(labelTemplate);
    };


    return (
        <div className="relative w-full h-full border rounded-lg overflow-hidden bg-[#ebfff8]" title="Bed">
            <div className="absolute inset-0 w-full h-full text-black left-32"
                style={{ height: "130%", top: "-15%" }}>
                {layers.map((layer, index) => (
                    <img
                        key={`layer-${index}`}
                        src={layer.img.src}
                        alt={layer.alt}
                        className="absolute top-0 left-0 h-full w-auto object-cover"
                        style={{ zIndex: index + 1, left: "50%", transform: "translateX(-50%)" }}
                        onClick={onImageClick}
                    />
                ))}

                {labels.map((label, index) => (
                    <div
                        key={`label-${index}`}
                        className="absolute"
                        style={{ left: `${label.x}%`, top: `${label.y}%`, zIndex: 100 }} // positions label based on coordinates
                    >
                        {label.component}
                    </div>
                ))}


            </div>

            {/* <div className="absolute bottom-0 z-30 p-1 text-center w-full">
                <span className="bg-black bg-opacity-70 text-white py-1 px-2 rounded">
                    [Snoring sounds]
                </span>
            </div> */}

            <div className='absolute top-0 left-2 w-60'>
                <PerceptionList />
            </div>


        </div>
    );
};

export default PatientVisualization;
