"use client"

import React, { useEffect, useState } from 'react';
import { ExerciseCreationPatientBasicInfo } from "@/src/api"
import { MdPlayArrow } from 'react-icons/md';
import "./BriefingModal.css";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

const BriefingModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const caseDescription = '3 year old boy with broken arm.';
  const vignette = 'A 3-year-old boy is brought to the ED by his mother after falling from a playground equipment. He is holding his left arm and appears to be in significant pain. The arm is slightly swollen and has an obvious deformity.';
  const basicInfo: ExerciseCreationPatientBasicInfo = {
    age: '3 years old',
    sex: 'Male',
    weight: '15 kg',
    height: '80 cm',
  };

  const [isFadingOut, setIsFadingOut] = useState(false);

  useEffect(() => {
    if (!isOpen) setIsFadingOut(false);
  }, [isOpen]);

  const handleStartClick = () => {
    setIsFadingOut(true);
    setTimeout(() => {
      onClose();
      setIsFadingOut(false);
    }, 300);
  };

  return (
    <div className={`fixed inset-0 flex items-center justify-center z-20 ${isOpen || isFadingOut ? 'block' : 'hidden'} ${isFadingOut ? 'fade-out-briefing' : ''}`}>
      <div className="fixed inset-0 bg-gray-900 bg-opacity-90 z-10 backdrop"></div>
      <div className="bg-gray-700 p-6 rounded-lg w-1/2 shadow-xl z-30 text-white">
        <h1 className="text-lg font-medium mb-4">{caseDescription}</h1>
        <p className="border border-gray-500 p-2 rounded mb-6">{vignette}</p>
        <h2 className="text-md font-semibold mb-2">Basic Info</h2>
        <ul className="list-disc pl-5 mb-6">
          <li>Age: {basicInfo.age}</li>
          <li>Sex: {basicInfo.sex}</li>
          <li>Weight: {basicInfo.weight}</li>
          <li>Height: {basicInfo.height}</li>
        </ul>
        <div className="flex justify-center">
          <button type="button" className="bg-green-500 text-white hover:bg-green-400 px-4 py-2 rounded-lg mt-6 flex items-center" onClick={handleStartClick}>
          Start
            <MdPlayArrow className="ml-2"/>
          </button>
        </div>
      </div>
    </div>
  );
};

export default BriefingModal;
