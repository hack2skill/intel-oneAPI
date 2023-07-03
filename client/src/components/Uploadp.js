import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '../assets/101391-online-test.json';
import { Link } from 'react-router-dom';

function Uploadp({ moduleNumber }) {
  const [numNotes, setNumNotes] = useState(0);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [fadeOut, setFadeOut] = useState(false); // New state to control fading out

  const handleNumNotesChange = (event) => {
    const count = parseInt(event.target.value, 10);
    setNumNotes(count);
    setSelectedFiles(new Array(count).fill(null));
    setUploadSuccess(false);
  };

  const handleFileChange = async (index, event) => {
    const file = event.target.files[0];
    const updatedFiles = [...selectedFiles];
    updatedFiles[index] = file;
    setSelectedFiles(updatedFiles);
    setUploadSuccess(false);

    try {
      const formData = new FormData();
      formData.append('files', file);

      const response = await fetch('https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/notestotext_pyqs', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadSuccess(true);
        setShowSuccessMessage(true);
        setTimeout(() => {
          setShowSuccessMessage(false);
          setFadeOut(true);
        }, 10000);
      } else {
        throw new Error('Error uploading file');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleUpload = () => {
    if (selectedFiles.some((file) => file === null)) {
      return;
    }

    setUploading(true);

    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append('files', file);
    });

    fetch('http://192.168.137.193:8000/notestotext_modwise', {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          setUploadSuccess(true);
          setShowSuccessMessage(true);
          setTimeout(() => {
            setShowSuccessMessage(false);
            setFadeOut(true);
          }, 10000);
        } else {
          throw new Error('Error uploading files');
        }
      })
      .catch((error) => {
        console.error('Error uploading files:', error);
      })
      .finally(() => {
        setUploading(false);
      });
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

  const handleUploadAnother = () => {
    setSelectedFiles(new Array(numNotes).fill(null));
    setUploadSuccess(false);
    setShowSuccessMessage(false);
    setFadeOut(false);
  };

  const renderUploadInputs = () => {
    const inputs = [];

    for (let i = 0; i < numNotes; i++) {
      inputs.push(
        <div key={`upload-input-${i}`}>
          <label>PYQ {i + 1} PDF:</label>
          <input
            type="file"
            accept="application/pdf"
            className="mb-4 rounded-md px-3"
            onChange={(event) => handleFileChange(i, event)}
          />
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
          <h1 className="text-3xl font-bold mb-4">Upload PYQ</h1>
          {!uploadSuccess ? (
            <>
              <label htmlFor="num-notes" className="block font-medium mb-2">
                Number of PYQ:
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
                className={`bg-green-500 text-white py-2 px-6 rounded-lg ml-4 ${
                  uploading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
                disabled={uploading || selectedFiles.some((file) => file === null)}
                onClick={handleUpload}
                whileHover={!uploading ? { scale: 1.05 } : {}}
                whileTap={!uploading ? { scale: 0.95 } : {}}
              >
                {uploading ? 'Uploaded' : 'Upload'}
              </motion.button>
              <Link to="/uploads" className="bg-green-500 text-white py-2 ml-4 px-6 mt-4 rounded-lg">
                Next
              </Link>
            </>
          ) : (
            <>
              {showSuccessMessage && (
                <motion.div className="text-xl" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  Successfully Uploaded!
                </motion.div>
              )}
              <motion.button
                className="bg-green-500 text-white py-2 px-6 rounded-lg mt-4"
                onClick={handleUploadAnother}
              >
                Upload Another
              </motion.button>
              <Link to="/uploads" className="text-blue-500 mt-8">
                Next
              </Link>
            </>
          )}
        </motion.div>
      )}
    </div>
  );
}

export default Uploadp;
