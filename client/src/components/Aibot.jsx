import React, { useState, useRef } from 'react';
import Navbar from './Navbar';
import Lottie from 'lottie-react';
import animationData from '../assets/134013-student-with-laptop.json';
import animationData1 from '../assets/39701-robot-bot-3d.json';

const Tutor = () => {
  const [inputText, setInputText] = useState('');
  const inputImageRef = useRef(null);
  const inputVoiceRef = useRef(null);
  const recognitionRef = useRef(null);
  const [isListening, setIsListening] = useState(false);
  const [outputText, setOutputText] = useState('');
  const [outputSound, setOutputSound] = useState(null);
  const [outputImage, setOutputImage] = useState(null);

  const avatarNarration = 'Hello! I am Luna, your tutor. How can I assist you today?';

  const handleReply = () => {
    // Handle the reply button functionality here
    console.log('Input Text:', inputText);
    console.log('Input Image:', inputImageRef.current.files[0]);
    console.log('Input Voice:', inputVoiceRef.current.files[0]);
    // You can perform further actions based on the input and update the output state variables accordingly.
  };

  const handleTextChange = (event) => {
    setInputText(event.target.value);
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    inputImageRef.current.value = ''; // Reset the input file value for re-selecting the same file
    setOutputImage(URL.createObjectURL(file));
  };

  const handleVoiceChange = () => {
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      const recognition = new window.SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map((result) => result[0])
          .map((result) => result.transcript)
          .join('');

        setInputText(transcript);
      };

      recognition.onerror = (event) => {
        console.error('Recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
      setIsListening(true);
      recognitionRef.current = recognition;
    }
  };

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center justify-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <div className="h-3/4 flex flex-col justify-center">
          <div className="bg-slate-100 rounded-lg shadow-lg px-60 py-16 h-full mt-4 mb-28 w-auto">
            <div className="flex items-center py-8 px-16">
              <div className="w-24 h-24 rounded-full bg-orange-600 flex-shrink-0">
                <Lottie animationData={animationData1} loop autoplay />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-800">Luna</p>
                <p className="text-gray-500 text-sm">{avatarNarration}</p>
              </div>
            </div>
          </div>
        </div>
        <div className="h-1/4 flex items-center justify-center">
          <div className="max-w-xl bg-slate-100 rounded-lg shadow-lg p-4 fixed bottom-4">
            <div className="flex items-center">
              <div className="w-24 h-24 rounded-full bg-green-500 flex-shrink-0">
                <Lottie animationData={animationData} loop autoplay />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-800">Me</p>
                <div className="flex items-center justify-between mt-2">
                  <input
                    type="text"
                    className="w-full mr-4 bg-white rounded-lg py-2 px-3 focus:outline-none"
                    placeholder="Enter your message"
                    value={inputText}
                    onChange={handleTextChange}
                  />
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleImageChange}
                    ref={inputImageRef}
                  />
                  <button
                    className="bg-blue-500 text-white rounded-lg py-2 px-4 hover:bg-blue-600 transition-colors"
                    onClick={handleReply}
                  >
                    Reply
                  </button>
                  <button
                    className={`bg-blue-500 text-white rounded-lg py-2 px-4 hover:bg-blue-600 transition-colors ml-2 ${
                      isListening ? 'bg-red-500' : ''
                    }`}
                    onClick={handleVoiceChange}
                  >
                    {isListening ? 'Stop Listening' : 'Add Voice'}
                  </button>
                  <button
                    className="bg-blue-500 text-white rounded-lg py-2 px-4 hover:bg-blue-600 transition-colors ml-2"
                    onClick={() => inputImageRef.current.click()}
                  >
                    Add Image
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="fixed bottom-4 right-4">
          <div className="w-64 bg-white rounded-lg shadow-lg p-4">
            {outputText && <p className="mb-2">{outputText}</p>}
            {outputSound && (
              <audio controls>
                <source src={outputSound} type="audio/mpeg" />
              </audio>
            )}
            {outputImage && <img src={outputImage} alt="Output" className="w-full" />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tutor;
