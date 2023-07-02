import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '../assets/101391-online-test.json';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

function Uploadp1({ moduleNumber }) {
  const [numNotes, setNumNotes] = useState(0);
  const [fadeOut, setFadeOut] = useState(false); // New state to control fading out
  const {currentUser}=useAuth();

  const handleNumNotesChange = (event) => {
    const count = parseInt(event.target.value, 10);
    setNumNotes(count);
  };

  const handleUpload = async () => {
    const files = document.querySelectorAll('input[type="file"]');
    const formData = new FormData();

    files.forEach((file) => {
      formData.append('files', file.files[0]);
    });

    formData.append('user', currentUser.email);

    try {
      const response = await axios.post(
        'https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/notestotext_pyqs',
        formData
      );

      console.log(response.data); // Handle the response data
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  const renderUploadInputs = () => {
    const inputs = [];

    for (let i = 0; i < numNotes; i++) {
      inputs.push(
        <div key={`upload-input-${i}`}>
          <label>Module {i + 1} PDF:</label>
          <input type="file" accept="application/pdf" className="mb-4 rounded-md px-3" />
        </div>
      );
    }

    return inputs;
  };

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
          <h1 className="text-3xl font-bold mb-4">Upload PYQ - Module Wise {moduleNumber}</h1>
          <label htmlFor="num-notes" className="block font-medium mb-2">
            Number of PYQs:
          </label>
          <input
            type="number"
            id="num-notes"
            min={0}
            value={numNotes}
            onChange={handleNumNotesChange}
            className="border border-gray-300 rounded-md px-3 py-2 mb-4"
          />
          {renderUploadInputs()}
          <motion.button
            className="bg-green-500 text-white py-2 px-6 rounded-lg ml-4"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleUpload}
          >
            Upload
          </motion.button>
          <Link to="/uploads1" className="bg-green-500 text-white py-2 ml-4 px-6 mt-4 rounded-lg">
            Next
          </Link>
        </motion.div>
      )}
    </div>
  );
}

export default Uploadp1;
