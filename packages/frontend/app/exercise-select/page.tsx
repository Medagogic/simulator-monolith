"use client"

import React from 'react';
import { APIProvider } from '../socketio/APIContext';
import ExerciseList from './ExerciseList';


const ExerciseListPage: React.FC = () => {
    return (
        <APIProvider>
            <ExerciseList />
        </APIProvider>
    )
}

export default ExerciseListPage;