"use client"

import React, { useState } from 'react';
import { useAPI } from '../socketio/APIContext';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';



interface FileObject {
    file: File | null,
    metadata: File | null
}



const ExerciseUploader: React.FC = () => {
    const api = useAPI();
    const [uploadedFiles, setUploadedFiles] = useState<FileObject>({ file: null, metadata: null });
    const [successMessage, setSuccessMessage] = useState<string | null>(null);


    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: string) => {
        const file = e.target.files?.[0] || null;

        if (type === 'exercise') {
            if (!file?.name.endsWith('.txt')) {
                toast.error('Exercise file must be a .txt file.');
                return;
            }
            if (file?.name.includes('metadata')) {
                toast.error('Exercise file cannot contain the word "metadata".');
                return;
            }

            setUploadedFiles(prevState => ({ ...prevState, file }));
        } else if (type === 'metadata') {
            if (!file?.name.endsWith('.txt')) {
                toast.error('Metadata file must be a .txt file.');
                return;
            }
            if (!file?.name.includes('metadata')) {
                toast.error('Metadata file must contain the word "metadata".');
                return;
            }

            setUploadedFiles(prevState => ({ ...prevState, metadata: file }));
        }
    }

    const handleUpload = () => {
        if (!uploadedFiles.file || !uploadedFiles.metadata) {
            return;
        }
        uploadExercise(uploadedFiles.file, uploadedFiles.metadata);
    }

    function uploadExercise(file: File, metadata: File) {
        const readFile = (file: File) => {
            return new Promise<string>((resolve, reject) => {
                const reader = new FileReader();

                reader.onload = (e) => {
                    const contents = e.target?.result;
                    resolve(contents as string);
                };

                reader.onerror = (e) => {
                    reject(new Error("Failed to read file"));
                };

                reader.readAsText(file);
            });
        };

        const exerciseName = file.name.replace('.txt', '');

        Promise.all([
            readFile(file),
            readFile(metadata)
        ]).then(([fileContents, metadataContents]) => {
            api.uploadExerciseStaticApiExercisesUploadPost({
                exerciseModel: {
                    exerciseName: exerciseName,
                    exerciseData: fileContents,
                    exerciseMetadata: metadataContents,
                    tags: ["medagogic", "development"]
                }
            })
                .then((response) => {
                    console.log("Success:", response);
                    toast.success(`Uploaded ${exerciseName}`);
                });
        }).catch((error) => {
            console.log("An error occurred:", error);
            toast.error('Failed to upload exercise.');
        });
    }

    return (
        <div className="bg-gray-800 p-2 text-white w-full h-full flex items-center justify-center text-sm">
            <div className="bg-gray-800 p-2 rounded-lg shadow-lg w-full max-w-md text">
                <h1 className="text-2xl mb-6 text-center">Upload Exercise</h1>
                <div className="flex flex-col gap-2">
                    <div className="flex flex-col gap-2">
                        <label htmlFor="exerciseFile" className="font-semibold">Choose exercise.txt:</label>
                        <input
                            className="p-1 rounded bg-gray-200 text-black focus:outline-none focus:border-blue-500"
                            type="file"
                            id="exerciseFile"
                            onChange={(e) => handleFileChange(e, 'exercise')}
                        />
                    </div>

                    <div className="flex flex-col gap-2">
                        <label htmlFor="metadataFile" className="font-semibold">Choose metadata.txt:</label>
                        <input
                            className="p-1 rounded bg-gray-200 text-black focus:outline-none focus:border-blue-500"
                            type="file"
                            id="metadataFile"
                            onChange={(e) => handleFileChange(e, 'metadata')}
                        />
                    </div>

                    <button className="p-2 rounded bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:border-blue-700" onClick={handleUpload}>
                        Upload
                    </button>
                </div>
            </div>

            <ToastContainer />
        </div>
    );
}

export default ExerciseUploader;
