import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '../assets/87967-task-completed.json';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

function Uploads1({ moduleNumber }) {
  const [file, setFile] = useState(null);
  const [fadeOut, setFadeOut] = useState(false); // New state to control fading out
  const { currentUser } = useAuth();

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('files', file, 'syllabus.txt');
      formData.append('user', currentUser.email);

      try {
        const response = await axios.post(
          'https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/notestotext_syllabus',
          formData
        );

        console.log(response.data); // Handle the response data
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };
  const handleFinish = async () => {

    const formData = new FormData();
      formData.append('user', currentUser.email);
  
      try {
        const response = await axios.post(
          'https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/filestotext2',
          formData
        );
  
        console.log(response.data); // Handle the response data
      } catch (error) {
        console.error('Error calling API:', error);
      }
    }
  
  


  return (
    <div className="flex flex-col items-center justify-center w-screen text-center h-screen bg-gradient-to-tr from-violet-700 via-green-600 to-green-400">
      {!fadeOut && (
        <motion.div
          className="bg-violet-900 text-white py-6 px-6 rounded-lg shadow-lg text-center justify-center items-center flex flex-col"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Lottie animationData={animationData} style={{ width: 400, height: 300 }} />
          <h1 className="text-3xl font-bold mb-4">Upload Syllabus {moduleNumber}</h1>
          <label htmlFor="file-upload" className="block font-medium mb-2">
            Select a text file:
          </label>
          <input
            type="file"
            id="file-upload"
            accept=".txt"
            onChange={handleFileChange}
            className="border border-gray-300 rounded-md px-3 py-2 mb-4"
          />
          <motion.button
            className="bg-green-500 text-white py-2 px-6 rounded-lg ml-4"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleUpload}
          >
            Upload
          </motion.button>
          <Link to="/wait">
          <button
            className="bg-green-500 text-white py-2 ml-4 px-6 mt-4 rounded-lg"
            onClick={handleFinish}
          >
            Finish
          </button>
          </Link>
        </motion.div>
      )}
    </div>
  );
};



export default Uploads1;
