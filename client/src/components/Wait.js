import React from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '../assets/95241-uploading.json';

const Wait = () => {
  const quotes = [
    "Patience is not the ability to wait, but the ability to keep a good attitude while waiting.",
    "The two most powerful warriors are patience and time.",
    "Wait for the right moment.",
    "Good things come to those who wait.",
    "Trust the process.",
  ];

  const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

  const handleOpenGmail = () => {
    window.open('https://mail.google.com/', '_blank');
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-100">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-4xl font-bold mb-4"
      >
        <Lottie animationData={animationData} className='h-16'/>
        Program is under process
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-lg text-gray-600 text-center mb-8"
      >
        We will get back to you soon. Please check your email.
      </motion.p>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-lg text-gray-600 text-center mb-8"
      >
        {randomQuote}
      </motion.p>

      <motion.button
        initial={{ opacity: 0, scale: 0 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="bg-blue-500 text-white rounded px-4 py-2 hover:bg-blue-600"
        onClick={handleOpenGmail}
      >
        Open Gmail
      </motion.button>
    </div>
  );
};

export default Wait;
