import React, { useState } from 'react';

function Anythingmore() {
  const [details, setDetails] = useState('');

  const handleInputChange = (event) => {
    setDetails(event.target.value);
  };

  const handleSubmit = () => {
    // Perform any necessary actions with the submitted details
    console.log('Submitted details:', details);
    // You can add additional logic here, such as making an API call to save the details

    // Clear the input field after submission
    setDetails('');
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
      <button
        className="bg-violet-900 text-white py-2 px-6 rounded-lg"
        onClick={handleSubmit}
      >
        Finish
      </button>
    </div>
  );
}

export default Anythingmore;
