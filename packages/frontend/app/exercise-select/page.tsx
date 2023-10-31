"use client"

import React from 'react';
import { APIProvider } from '../socketio/APIContext';
import ExerciseList from './ExerciseList';
import ExerciseUploader from './ExerciseUploader';


const ExerciseListPage: React.FC = () => {
    return (
        <APIProvider>
            {/* <ExerciseList /> */}
            <ExerciseUploader />
        </APIProvider>
    )
}

export default ExerciseListPage;