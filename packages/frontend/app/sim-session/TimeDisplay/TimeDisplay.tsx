import { useSessionStore } from '@/app/storage/SessionStore';
import React, { useState, useEffect } from 'react';

const TimeDisplay: React.FC = () => {
    const exerciseTimeSeconds = useSessionStore((state) => state.exerciseTimeSeconds);

    // This function will convert the elapsed total seconds into a time format (HH:mm:ss)
    const formatTime = (totalSeconds: number) => {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds - hours * 3600) / 60);
        const seconds = totalSeconds - hours * 3600 - minutes * 60;

        const formatNumber = (val: number) => (`0${val}`).slice(-2); // Ensures 2 digits

        return `${formatNumber(hours)}:${formatNumber(minutes)}:${formatNumber(seconds)}`;
    };

    return (
        <div>
            <h2>{formatTime(exerciseTimeSeconds)}</h2>
        </div>
    );
};

export default TimeDisplay;
