import React, { useState } from 'react';
import { motion } from 'framer-motion';

function UploadNotes() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      return;
    }

    setUploading(true);

    // Generate a pre-signed URL for file upload
    const url = await getPresignedUrl(selectedFile.name, selectedFile.type);

    try {
      // Use the generated URL to upload the file directly to S3
      await uploadFile(url, selectedFile);
      setUploadSuccess(true);
    } catch (error) {
      console.error('Error uploading file:', error);
    }

    setUploading(false);
  };

  // Function to generate a pre-signed URL for file upload
  const getPresignedUrl = async (filename, filetype) => {
    const response = await fetch(`/api/get-upload-url?filename=${filename}&filetype=${filetype}`);
    const data = await response.json();
    return data.url;
  };

  // Function to upload the file to the generated URL
  const uploadFile = async (url, file) => {
    await fetch(url, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type,
      },
    });
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <motion.div
        className="bg-blue-500 text-white py-6 px-8 rounded-lg shadow-lg"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold mb-4">Upload Notes</h1>
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
          </>
        ) : (
          <motion.div
            className="text-xl"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            Upload successful!
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}

export default UploadNotes;