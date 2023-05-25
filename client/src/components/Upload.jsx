import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function Upload() {
  const [numModules, setNumModules] = useState(0);
  const [numPYQs, setNumPYQs] = useState(0);

  const handleModuleUpload = (moduleNumber) => {
    // Handle module upload logic here
    console.log(`Upload module ${moduleNumber} PDF`);
  };

  const handlePYQUpload = (pyqNumber) => {
    // Handle PYQ upload logic here
    console.log(`Upload PYQ ${pyqNumber} PDF`);
  };

  const handleSyllabusUpload = () => {
    // Handle syllabus upload logic here
    console.log('Upload syllabus');
  };

  const handleNumModulesChange = (event) => {
    setNumModules(parseInt(event.target.value, 10));
  };

  const handleNumPYQsChange = (event) => {
    setNumPYQs(parseInt(event.target.value, 10));
  };

  const renderModuleUploadButtons = () => {
    const buttons = [];

    for (let i = 1; i <= numModules; i++) {
      buttons.push(
        <div key={`module-${i}`}>
          <label>Upload Module {i} PDF:</label>
          <Link to="/uploadnotes">
            <button onClick={() => handleModuleUpload(i)}>Upload</button>
          </Link>
        </div>
      );
    }

    return buttons;
  };

  const renderPYQUploadButtons = () => {
    const buttons = [];

    for (let i = 1; i <= numPYQs; i++) {
      buttons.push(
        <div key={`pyq-${i}`}>
          <label>Upload PYQ {i} PDF:</label>
          <Link to="/uploadsyllabus">
            <button onClick={() => handlePYQUpload(i)}>Upload</button>
          </Link>
        </div>
      );
    }

    return buttons;
  };

  return (
    <div>
      <h2>Upload Notes</h2>
      <label htmlFor="num-modules">Number of Modules:</label>
      <input
        type="number"
        id="num-modules"
        min={0}
        value={numModules}
        onChange={handleNumModulesChange}
      />
      {renderModuleUploadButtons()}

      <h2>Upload PYQs</h2>
      <label htmlFor="num-pyqs">Number of PYQs:</label>
      <input
        type="number"
        id="num-pyqs"
        min={0}
        value={numPYQs}
        onChange={handleNumPYQsChange}
      />
      {renderPYQUploadButtons()}

      <h2>Upload Syllabus</h2>
      <div>
        <label>Upload Syllabus PDF:</label>
        <Link to="/uploadsyllabus">
          <button onClick={handleSyllabusUpload}>Upload</button>
        </Link>
      </div>
    </div>
  );
}

export default Upload;
