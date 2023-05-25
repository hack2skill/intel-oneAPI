import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '../assets/95241-uploading.json';

function Uploadmn1({ moduleNumber }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadSuccess(false);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      return;
    }

    setUploading(true);

    const reader = new FileReader();

    reader.onload = () => {
      const fileContents = reader.result;
      const blob = new Blob([fileContents], { type: selectedFile.type });
      const filePath = `Local_Storage/notes_pdf/module_${moduleNumber}/${selectedFile.name}`;

      saveFileLocally(filePath, blob)
        .then(() => {
          setUploadSuccess(true);
          setUploading(false);
          setShowSuccessMessage(true);
          setTimeout(() => {
            setShowSuccessMessage(false);
          }, 10000); // Set timeout for 10 seconds
        })
        .catch((error) => {
          console.error('Error saving file:', error);
          setUploading(false);
        });
    };

    reader.readAsArrayBuffer(selectedFile);
  };

  const saveFileLocally = (filePath, file) => {
    return new Promise((resolve, reject) => {
      const virtualLink = document.createElement('a');
      virtualLink.href = URL.createObjectURL(file);
      virtualLink.download = filePath;
      virtualLink.addEventListener('load', () => {
        URL.revokeObjectURL(virtualLink.href);
        resolve();
      });
      virtualLink.addEventListener('error', (error) => {
        reject(error);
      });
      document.body.appendChild(virtualLink);
      virtualLink.click();
      document.body.removeChild(virtualLink);
    });
  };

  return (
    <div className="flex flex-col items-center justify-center text-center">
      <motion.div
        className="bg-blue-500 text-white py-6 px-6 rounded-lg shadow-lg"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Lottie animationData={animationData} style={{ width: 400, height: 300 }} />
        <h1 className="text-3xl font-bold mb-4">Upload Notes - Module {moduleNumber}</h1>
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
              {uploading ? 'Uploaded' : 'Upload'}
            </motion.button>
          </>
        ) : (
          <>
            {showSuccessMessage ? (
              <motion.div
                className="text-xl"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                Successfully Uploaded!
              </motion.div>
            ) : null}
            <motion.button
              className="bg-green-500 text-white py-2 px-6 rounded-lg mt-4"
              onClick={() => setUploadSuccess(false)}
            >
              Upload Again
            </motion.button>
          </>
        )}
      </motion.div>
    </div>
  );
}

export default Uploadmn1;