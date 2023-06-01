import React from 'react';
import Navbar from './Navbar';
const Tutor = () => {
  const avatarNarration = 'Hello! How can I assist you today?';
  const ourReply = 'We would like to learn about artificial intelligence.';
  const tutorImages = [
    'image1.jpg',
    'image2.jpg',
    'image3.jpg'
  ];

  return (
    <div>
      <Navbar />
    <div className="flex flex-col items-center justify-center py-10">
      <div className="w-full max-w-xl bg-gray-100 rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center">
          <div className="w-16 h-16 rounded-full bg-blue-500 flex-shrink-0"></div>
          <div className="ml-4">
            <p className="text-lg font-bold">AI Tutor</p>
            <p className="text-gray-500 text-sm">{avatarNarration}</p>
          </div>
        </div>
      </div>

      <div className="w-full max-w-xl bg-gray-100 rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center">
          <div className="w-16 h-16 rounded-full bg-green-500 flex-shrink-0"></div>
          <div className="ml-4">
            <p className="text-lg font-bold">You</p>
            <p className="text-gray-500 text-sm">{ourReply}</p>
          </div>
        </div>
      </div>

      <div className="w-full max-w-xl bg-gray-100 rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-medium mb-4">Related Images:</h3>
        <div className="grid grid-cols-3 gap-4">
          {tutorImages.map((image, index) => (
            <img key={index} src={image} alt={`Image ${index + 1}`} className="rounded-lg" />
          ))}
        </div>
      </div>
    </div>
    </div>
  );
};

export default Tutor;
