"use client"
import React, { useState } from 'react';
import slide1 from './slides/1.svg';
import slide2 from './slides/2.svg';
import slide3 from './slides/3.svg';
import slide4 from './slides/4.svg';

const Slideshow: React.FC = () => {
  const slides = [slide1, slide2, slide3, slide4];
  const [currentSlide, setCurrentSlide] = useState(0);

  const handleForwardClick = () => {
    setCurrentSlide((prevSlide) => (prevSlide + 1) % slides.length);
  };

  const handleBackClick = () => {
    setCurrentSlide((prevSlide) => (prevSlide - 1 + slides.length) % slides.length);
  };

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-gray-700">
      <div
        className="absolute left-0 w-1/4 h-full cursor-pointer z-10"
        onClick={handleBackClick}
        style={{ cursor: 'w-resize' }}
      ></div>
      <div
        className="absolute right-0 w-3/4 h-full cursor-pointer z-10"
        onClick={handleForwardClick}
      ></div>
      {slides.map((slide, index) => (
        <img
          key={index}
          src={slide.src}
          alt={`Slide ${index + 1}`}
          className={`absolute w-full h-full transition-all ease duration-300 ${
            currentSlide === index ? 'opacity-100' : 'opacity-0'
          }`}
        />
      ))}
    </div>
  );
};

export default Slideshow;
