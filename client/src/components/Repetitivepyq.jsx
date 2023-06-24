import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';

const Repetitivepyq = () => {
  const [pdfUrl, setPdfUrl] = useState('');

  useEffect(() => {
    fetchPdf();
  }, []);

  const fetchPdf = async () => {
    try {
      const response = await fetch('API_URL'); // Replace 'API_URL' with your actual API endpoint
      if (response.ok) {
        const pdfData = await response.blob();
        const pdfUrl = URL.createObjectURL(pdfData);
        setPdfUrl(pdfUrl);
      } else {
        throw new Error('Error fetching PDF');
      }
    } catch (error) {
      console.error('Error fetching PDF:', error);
    }
  };

  return (
    <div>
      <Navbar />

      <div className="flex justify-center">
        <div className="w-1/2 h-1/2 bg-gray-200 rounded-lg mt-4">
          <h1 className="text-center text-3xl">Repetitive PYQ</h1>
          {pdfUrl && (
            <iframe src={pdfUrl} title="Sorted PYQ" className="w-full h-full"></iframe>
          )}
        </div>
      </div>
    </div>
  );
};

export default Repetitivepyq;
