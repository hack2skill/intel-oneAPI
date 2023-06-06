import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '../assets/87967-task-completed.json';
import { Link } from 'react-router-dom';

function Uploadsyllabus() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadSuccess(false); // Reset upload success status when a new file is selected
  };

  const handleUpload = () => {
    if (!selectedFile) {
      return;
    }

    setUploading(true);

    const reader = new FileReader();

    reader.onload = () => {
      // Get the file contents
      const fileContents = reader.result;

      // Create a Blob from the file contents
      const blob = new Blob([fileContents], { type: selectedFile.type });

      // Call the API to process the syllabus
      uploadSyllabus(blob)
        .then(() => {
          setUploadSuccess(true);
        })
        .catch((error) => {
          console.error('Error uploading syllabus:', error);
        })
        .finally(() => {
          setUploading(false);
        });
    };

    reader.readAsArrayBuffer(selectedFile);
  };

  const uploadSyllabus = (file) => {
    return fetch('https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/notestotext_syllabus', {
      method: 'POST',
      body: file,
    });
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400">
      <motion.div
        className="bg-violet-900 text-white py-6 px-6 rounded-lg shadow-lg justify-center items-center flex flex-col"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Lottie animationData={animationData} style={{ width: 400, height: 300 }} />
        <h1 className="text-3xl font-bold mb-4">Upload Syllabus</h1>
        {!uploadSuccess ? (
          <>
            <input
              type="file"
              accept="application/pdf"
              className="mb-4"
              onChange={handleFileChange}
            />
            <motion.button
              className={`bg-green-500 text-white py-2 px-6 rounded-lg ${
                uploading ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={uploading || !selectedFile}
              onClick={handleUpload}
              whileHover={!uploading ? { scale: 1.05 } : {}}
              whileTap={!uploading ? { scale: 0.95 } : {}}
            >
              {uploading ? 'Uploading...' : 'Upload'}
            </motion.button>
            <Link to="/anythingmore" className="bg-green-500 text-white py-2 px-6 mt-4 rounded-lg">
              Next
            </Link>
          </>
        ) : (
          <motion.div className="text-xl" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            Upload successful!
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}

export default Uploadsyllabus;
