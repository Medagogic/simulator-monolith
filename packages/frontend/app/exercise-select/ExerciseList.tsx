import { ExerciseModel } from '@/src/api';
import React, { useEffect, useState } from 'react';
import { useAPI } from '../socketio/APIContext';
import { FaTrash } from 'react-icons/fa';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import "./ExerciseList.css";


const confirmDelete = (itemName: string): Promise<boolean> => {
    return new Promise((resolve) => {
      confirmAlert({
        title: 'Confirm to delete',
        message: `Are you sure you want to delete ${itemName}?`,
        buttons: [
          {
            label: 'Yes',
            id: 'yes',
            onClick: () => {
              resolve(true);
            }
          },
          {
            label: 'No',
            id: 'no',
            onClick: () => {
              resolve(false);
            }
          }
        ]
      });
    });
  };

interface ExerciseListEntryProps {
    exerciseModel: ExerciseModel;
    onClick: (model: ExerciseModel) => void;
    isAdmin: boolean;
    onDelete?: (model: ExerciseModel) => void;
}


const ExerciseListEntry: React.FC<ExerciseListEntryProps> = ({ exerciseModel, onClick, isAdmin, onDelete }) => {
    const [shake, setShake] = useState(false);

    const toggleShake = () => setShake(!shake);

    async function handleDeleteClick(event: any) {
        event.stopPropagation();

        const result = await confirmDelete(exerciseModel.exerciseName);
        if (result) {
          console.log("Deleting exercise: " + exerciseModel.exerciseName);
        } else {
            console.log("Cancelled deleting exercise: " + exerciseModel.exerciseName);
        }
    }

    return (
        <div
            onClick={() => onClick(exerciseModel)}
            className={`bg-gray-700 p-2 my-1 rounded-md cursor-pointer hover:bg-gray-600 transition-all flex flex-row items-center ${shake ? 'shake' : ''}`}
        >
            <div className='flex-auto'>
                <p className="text-white text-m font-bold">{exerciseModel.exerciseName}</p>
                <div className='w-full flex gap-2'>
                    {exerciseModel.tags.map((tag, index) => (
                        <span key={index} className="text-gray-300 text-xs mt-1 bg-gray-500 rounded-full px-2 py-1">
                            {tag}
                        </span>
                    ))}
                </div>
            </div>
            <div>
                {isAdmin && (
                    <button
                        onClick={(e) => handleDeleteClick(e)}
                        onMouseEnter={toggleShake}
                        onMouseLeave={toggleShake}
                        className="bg-red-500 text-white rounded-full p-2 z-10"
                    >
                        <FaTrash />
                    </button>
                )}
            </div>
        </div>
    );
};


interface ExerciseListProps {
    isAdmin?: boolean;
}


const ExerciseList: React.FC<ExerciseListProps> = ({ isAdmin }) => {
    const api = useAPI();
    const [nameFilter, setNameFilter] = useState<string>('');
    const [tagFilter, setTagFilter] = useState<string[]>([]);
    const [exercises, setExercises] = useState<ExerciseModel[]>([]);
    const [adminMode, setAdminMode] = useState<boolean>(false);
    let requestCounter = 0;

    useEffect(() => {
        setAdminMode(isAdmin == true);
    }, [isAdmin]);

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

    function onDelete(exerciseModel: ExerciseModel) {
        console.log("Deleting exercise: " + exerciseModel.exerciseName);
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
                    <ExerciseListEntry key={index} exerciseModel={exercise} onClick={console.log} isAdmin={adminMode} onDelete={onDelete} />
                ))}
            </ul>

        </div>
    );
};

export default ExerciseList;