import { ExerciseModel } from '@/src/api';
import React, { useEffect, useState } from 'react';
import { useAPI } from '../socketio/APIContext';
import "./ExerciseList.css";


interface SuggestionProps {
    exerciseModel: ExerciseModel;
    onClick: (advice: ExerciseModel) => void;
}


const ExerciseListEntry: React.FC<SuggestionProps> = ({ exerciseModel, onClick }) => (
    <div
        onClick={() => onClick(exerciseModel)}
        className="bg-gray-700 p-2 my-1 rounded-md cursor-pointer hover:bg-gray-600 transition-all grow-in"
    >
        <p className="text-white text-m font-bold">{exerciseModel.exerciseName}</p>

        <div className='w-full flex gap-2'>
            {exerciseModel.tags.map((tag, index) => (
                <span key={index} className="text-gray-300 text-xs mt-1 bg-gray-500 rounded-full px-2 py-1">
                    {tag}
                </span>
            ))}
        </div>
    </div>
);


const ExerciseList: React.FC = () => {
    const api = useAPI();
    const [nameFilter, setNameFilter] = useState<string>('');
    const [tagFilter, setTagFilter] = useState<string[]>([]);
    const [exercises, setExercises] = useState<ExerciseModel[]>([]);
    let requestCounter = 0;

    useEffect(() => {
        requestCounter++;
        const currentRequest = requestCounter;

        RefreshExercises(currentRequest);
    }, [nameFilter, tagFilter]);


    function RefreshExercises(currentRequest: number) {
        api.searchExercisesStaticApiExercisesListGet(
            {
                nameFilter: nameFilter,
                tagFilter: tagFilter
            }
        ).then((response) => {
            if (currentRequest === requestCounter) {
                setExercises(response);
            }
        })
    }
    

    function reset() {
        setNameFilter('');
        setTagFilter([]);
    }


    return (
        <div className="bg-gray-800 p-4 text-white w-full h-full">
            <div className="flex items-center mb-4 text-sm text-gray-700 w-full justify-center flex-wrap gap-2">
                <input
                    type="text"
                    placeholder="Search by name"
                    value={nameFilter}
                    onChange={(e) => setNameFilter(e.target.value)}
                    className="dark:bg-gray-700 p-2 rounded border"
                />
                <input
                    type="text"
                    placeholder="Filter by tag"
                    value={tagFilter}
                    onChange={(e) => setTagFilter(e.target.value.split(','))}
                    className="dark:bg-gray-700 p-2 rounded border"
                />
                <button className="p-2 rounded bg-blue-500 text-white hover:bg-blue-600" onClick={reset}>
                    Reset
                </button>
            </div>
            <ul className="dark:text-gray-300 text-sm">
                {exercises.map((exercise, index) => (
                    <ExerciseListEntry key={index} exerciseModel={exercise} onClick={console.log} />
                ))}
            </ul>

        </div>
    );
};

export default ExerciseList;