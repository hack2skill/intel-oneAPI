import React, { useState } from 'react';
import UploadNotes from './UploadNotes';
import UploadPYQ from './Uploadpyq';
import UploadSyllabus from './Uploadsyllabus';

function Upload() {
  const [numModules, setNumModules] = useState(0);
  const [numPYQs, setNumPYQs] = useState(0);
  const [activeComponent, setActiveComponent] = useState(null);

  const handleModuleUpload = (moduleNumber) => {
    setActiveComponent(() => <UploadNotes moduleNumber={moduleNumber} />);
  };
  
  const handlePYQUpload = (pyqNumber) => {
    // Handle PYQ upload logic here
    setActiveComponent(<UploadPYQ pyqNumber={pyqNumber} />);
  };

  const handleSyllabusUpload = () => {
    // Handle syllabus upload logic here
    setActiveComponent(<UploadSyllabus />);
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
          <button onClick={() => handleModuleUpload(i)}>Upload</button>
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
          <button onClick={() => handlePYQUpload(i)}>Upload</button>
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
        <button onClick={handleSyllabusUpload}>Upload</button>
      </div>

      <div className="upload-container">
        <div className="left-side">
          {/* Display the active component on the left side */}
          {activeComponent}
        </div>
        <div className="right-side">
          {/* You can place any other content or components on the right side */}
        </div>
      </div>
    </div>
  );
}

export default Upload;
