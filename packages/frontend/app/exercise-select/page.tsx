"use client"

import React from 'react';
import { APIProvider } from '../socketio/APIContext';
import ExerciseList from './ExerciseList';
import ExerciseUploader from './ExerciseUploader';


const ExerciseListPage: React.FC = () => {
    const adminMode = false;

    return (
        <APIProvider>
            {adminMode &&
                <h1>ADMIN MODE</h1>
            }
            <div className='flex flex-col items-center justify-center h-full'>
            <ExerciseList isAdmin={adminMode} />
            {adminMode && 
                <ExerciseUploader />
            }
            </div>
        </APIProvider>
    )
}

export default ExerciseListPage;