import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function Anythingmore() {
  const [details, setDetails] = useState('');

  const handleInputChange = (event) => {
    setDetails(event.target.value);
  };

  const handleSubmit = () => {
    // Perform any necessary actions with the submitted details
    console.log('Submitted details:', details);
    // You can add additional logic here, such as making an API call to save the details

    // Create a text file from the input content
    const textFile = new Blob([details], { type: 'text/plain' });

    // Create a file URL for downloading
    const fileURL = URL.createObjectURL(textFile);

    // Create a temporary link element
    const downloadLink = document.createElement('a');
    downloadLink.href = fileURL;
    downloadLink.download = 'anything.txt';

    // Append the link to the document body and trigger the download
    document.body.appendChild(downloadLink);
    downloadLink.click();

    // Remove the link from the document body
    document.body.removeChild(downloadLink);

    // Call the API to push the text file
    callAPI(textFile)
      .then(() => {
        console.log('API call successful');
      })
      .catch((error) => {
        console.error('Error calling API:', error);
      });

    // Clear the input field after submission
    setDetails('');
  };

  const callAPI = (file) => {
    const formData = new FormData();
    formData.append('file', file);

    return fetch(
      'https://3f2ssd7loqowjtj7hnzhni7trq0blutk.lambda-url.us-east-1.on.aws/notestotext_anythingelse',
      {
        method: 'POST',
        body: formData,
      }
    );
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen text-center w-screen bg-gradient-to-tr from-violet-700 via-green-600 to-green-400">
      <h1 className="text-3xl font-bold mb-4 text-white">Anything more to add!</h1>
      <textarea
        className="w-96 h-40 p-4 mb-4 rounded-md"
        value={details}
        onChange={handleInputChange}
        placeholder="Enter details..."
      ></textarea>
      <button className="bg-violet-900 text-white py-2 px-6 rounded-lg mb-4" onClick={handleSubmit}>
        Submit
      </button>
      <Link to="/dashboard">
        <button className="bg-violet-900 text-white py-2 px-6 rounded-lg">Finish</button>
      </Link>
    </div>
  );
}

export default Anythingmore;
