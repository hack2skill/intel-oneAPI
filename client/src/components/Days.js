import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { motion } from 'framer-motion';
import NavBar from './NavBar';
import Lottie from 'lottie-react';
import AnimationData from '../assets/100277-calendar-days.json';

const Days = () => {
  const history = useHistory();
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleStartDateChange = (event) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event) => {
    setEndDate(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));

    history.push(`/studyplanner?days=${days}`);
  };

  return (
    <div>
      <div className="w-screen">
        <NavBar />
        <div className="flex items-center justify-center h-screen w-screen bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-4">
          <div className='bg-white shadow-md rounded px-12 pt-6 pb-8 mb-4'>
          <Lottie options={{ loop: true, autoplay: true, animationData: AnimationData }} />
          <h2 className="text-center text-2xl font-bold mb-6">Schedule days</h2>

          <motion.form
            onSubmit={handleSubmit}
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="flex flex-col mb-4">
              <label className="text-lg mb-2">Start Date</label>
              <input
                type="date"
                className="p-2 border border-gray-400 rounded"
                value={startDate}
                onChange={handleStartDateChange}
                required
              />
            </div>
            <div className="flex flex-col mb-4">
              <label className="text-lg mb-2">End Date</label>
              <input
                type="date"
                className="p-2 border border-gray-400 rounded"
                value={endDate}
                onChange={handleEndDateChange}
                required
              />
            </div>
            <button
              type="submit"
              className="bg-indigo-500 text-white font-bold py-2 px-4 rounded hover:bg-indigo-600"
            >
                Submit  
            </button>
          </motion.form>
        </div>
      </div>
    </div>
    </div>
  );
};

export default Days;
