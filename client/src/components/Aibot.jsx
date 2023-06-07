import React from 'react';
import Navbar from './Navbar';
import Lottie from 'lottie-react';
import animationData from '../assets/134013-student-with-laptop.json';
import animationData1 from '../assets/39701-robot-bot-3d.json';

const Tutor = () => {
  const avatarNarration = 'Hello! I am Luna, your tutor. How can I assist you today?';

  const handleReply = () => {
    // Handle the reply button functionality here
  };

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center justify-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <div className="h-3/4 flex flex-col justify-center">
          <div className="bg-slate-100 rounded-lg shadow-lg px-60 py-16 h-full mt-4 mb-28 w-auto">
            <div className="flex items-center py-8 px-16">
              <div className="w-24 h-24 rounded-full bg-orange-600 flex-shrink-0">
                <Lottie animationData={animationData1} loop autoplay />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-800">Luna</p>
                <p className="text-gray-500 text-sm">{avatarNarration}</p>
              </div>
            </div>
          </div>
        </div>
        <div className="h-1/4 flex items-center justify-center">
          <div className="max-w-xl bg-slate-100 rounded-lg shadow-lg p-4 fixed bottom-4">
            <div className="flex items-center">
              <div className="w-24 h-24 rounded-full bg-green-500 flex-shrink-0">
                <Lottie animationData={animationData} loop autoplay />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-800">Me</p>
                <div className="flex items-center justify-between mt-2">
                  <input
                    type="text"
                    className="w-full mr-4 bg-white rounded-lg py-2 px-3 focus:outline-none"
                    placeholder="Enter your message"
                  />
                  <button
                    className="bg-blue-500 text-white rounded-lg py-2 px-4 hover:bg-blue-600 transition-colors"
                    onClick={handleReply}
                  >
                    Reply
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tutor;
