import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';

const Sortedpyq = () => {
  const [pdfUrl, setPdfUrl] = useState('');

  useEffect(() => {
    fetchPdf();
  }, []);

  const fetchPdf = async () => {
    try {
      const response = await fetch('https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/generate_pdf');
      if (response.ok) {
        const pdfData = await response.blob();
        const pdfUrl = URL.createObjectURL(pdfData);

        // Download the PDF file
        const link = document.createElement('a');
        link.href = pdfUrl;
        link.download = 'combined_pdf.pdf';
        link.click();

        // Show the PDF in the iframe
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
          <h1 className="text-center text-3xl">Sorted PYQ</h1>
          {pdfUrl && (
            <iframe src={pdfUrl} title="Sorted PYQ" className="w-full h-full"></iframe>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sortedpyq;
