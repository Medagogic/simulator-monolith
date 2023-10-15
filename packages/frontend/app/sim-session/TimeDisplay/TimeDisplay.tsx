import React, { useState, useEffect } from 'react';

const TimeDisplay: React.FC = () => {
    const [secondsElapsed, setSecondsElapsed] = useState(0);

    // This function will convert the elapsed total seconds into a time format (HH:mm:ss)
    const formatTime = (totalSeconds: number) => {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds - hours * 3600) / 60);
        const seconds = totalSeconds - hours * 3600 - minutes * 60;

        const formatNumber = (val: number) => (`0${val}`).slice(-2); // Ensures 2 digits

        return `${formatNumber(hours)}:${formatNumber(minutes)}:${formatNumber(seconds)}`;
    };

    // Use the useEffect hook to set up an interval that updates the elapsed time
    useEffect(() => {
        const intervalId = setInterval(() => {
            setSecondsElapsed((prev) => prev + 1);
        }, 1000); // Update every second

        // Clean up the interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h2>{formatTime(secondsElapsed)}</h2>
        </div>
    );
};

export default TimeDisplay;
