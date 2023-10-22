
import file_thumbnail from './files/file.png';
import React, { useCallback, useState, useRef, FC } from 'react';
import { FiUpload, FiActivity } from 'react-icons/fi';


type Props = {
    onFileProcessed: (thumbnail: string) => void;
};

const FileDropZone: FC<Props> = ({ onFileProcessed }) => {
    const [isDraggingOver, setIsDraggingOver] = useState(false);
    const [processing, setProcessing] = useState(false);

    const onDrop = useCallback(async (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        const data = e.dataTransfer.getData("text");
        setIsDraggingOver(false);
        setProcessing(true);
        onFileProcessed(data);
    }, [onFileProcessed]);


    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDraggingOver(true);
    };

    const handleDragLeave = () => {
        setIsDraggingOver(false);
    };

    const dropZoneStyle = isDraggingOver ? "border-blue-500 bg-gray-600" : "border-gray-400 bg-gray-700";

    return (
        <div
            onDrop={onDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`border-4 border-dashed w-80 h-80 mx-auto my-auto rounded-lg flex justify-center items-center ${dropZoneStyle}`}
        >
            {processing ? <FiActivity className="fas fa-upload text-white text-3xl" /> : <FiUpload className="fas fa-upload text-white text-3xl"></FiUpload>}
        </div>
    );
};


type DragDropPageProps = {
    onFileProcessedCallback: (newThumbnail: string) => void;
  };


const DragDropPage: FC<DragDropPageProps> = ({ onFileProcessedCallback }) => {
    const [thumbnailVisible, setThumbnailVisible] = useState(true);
    const dragImageRef = useRef<HTMLImageElement | null>(null);
  
    const onFileProcessed = (newThumbnail: string) => {
      setThumbnailVisible(false);
      onFileProcessedCallback(newThumbnail);
    };

    const handleDragStart = (e: React.DragEvent<HTMLImageElement>, thumbnail: string) => {
        e.dataTransfer.setData("text", thumbnail);
        if (dragImageRef.current) {
            e.dataTransfer.setDragImage(dragImageRef.current, 0, 0);
        }
    };

    return (
        <div className="relative h-screen w-screen bg-gray-700 flex items-center justify-center">
            {thumbnailVisible && (
            <img
                src={file_thumbnail.src}
                alt="File"
                draggable
                onDragStart={(e) => handleDragStart(e, 'Thumbnail Data')}
                className="absolute top-1/2 left-4 transform -translate-y-1/2 max-h-60"
                ref={dragImageRef}
            />
            )}
            <FileDropZone onFileProcessed={onFileProcessed} />
        </div>
    );
};

export default DragDropPage;
