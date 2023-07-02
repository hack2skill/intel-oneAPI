import React, { useEffect, useState } from 'react';
import { Document, Page } from 'react-pdf';
import axios from 'axios';
import NavBar from './NavBar';
import { motion } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import Lottie from 'lottie-react';
import animation from '../assets/39701-robot-bot-3d.json';
import ChatBot from 'react-simple-chatbot'; 
import { MdClose } from 'react-icons/md';



const Learnnote = () => {
  const [pdfData, setPdfData] = useState(null);
  const [isToggleOn, setIsToggleOn] = useState(false);
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const topicName = searchParams.get('topic');
  const [isOpen, setIsOpen] = useState(false);

  const handleClose = () => {
    setIsOpen(false);
  };


  useEffect(() => {
    const fetchPdfData = async () => {
      try {
        const response = await axios.post(
          'http://172.25.0.105:8000/get_notes_pdf?email=angeloantu%40gmail.com',
          { responseType: 'arraybuffer' }
        );

        const arrayBuffer = response.data;
        const base64Data = btoa(
          new Uint8Array(arrayBuffer).reduce(
            (data, byte) => data + String.fromCharCode(byte),
            ''
          )
        );
        setPdfData(base64Data);
      } catch (error) {
        console.error('Error fetching PDF data:', error);
      }
    };

    fetchPdfData();
  }, []);

  const handleToggle = () => {
    setIsToggleOn(!isToggleOn);
  };

  return (
    <div>
      <div className="w-screen">
        <NavBar />
        <div className="flex flex-col items-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
          <h1 className="text-3xl text-white font-bold mb-4 mt-4">{topicName}</h1>
          <div className="h-screen flex w-screen justify-center align-center">
            <div className="flex-1 bg-violet-50 border-r-4 border-indigo-300 p-8 font-semibold text-2xl">
             
              <div className="grid grid-cols-1">
                <motion.div
                  className="bg-slate-100 rounded-lg shadow-lg h-80 mt-12"
                  initial="hidden"
                  animate="visible"
                  transition={{ delay: 0.2 }}
                >
                  <div className="flex flex-col items-center justify-center mt-8">
                    <iframe
                      width="600"
                      height="260"
                      src="https://www.youtube.com/embed/ss9FpyRgIjw" // Update the URL here
                      title="YouTube video player"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    ></iframe>
                    <h3 className="mt-4"></h3>
                  </div>
                </motion.div>
                <div className="chatbot-container fixed bottom-5 left-5 h-50">
                         {isOpen ? (
                            <>
                              <div className="close-icon" onClick={handleClose}>
                                <MdClose className="text-grey-800 text-2xl cursor-pointer" />
                              </div>
                          <ChatBot
                          steps={[
                            {
                              id: '1',
                              message: 'Hello, how can I assist you?',
                              trigger: '2',
                            },
                            {
                              id: '2',
                              user: true,
                              trigger: '3',
                            },
                            {
                              id: '3',
                              message: 'Sure, I can help you with your doubt. What is your question about the BCD adder concept?',
                              trigger: '4',
                            },
                            {
                              id: '4',
                              user: true,
                              trigger: '5',
                            },
                            {
                              id: '5',
                              message: 'I see. The BCD adder, also known as the Binary Coded Decimal adder, is a digital circuit that performs addition on Binary Coded Decimal numbers. BCD is a way to represent decimal numbers in binary form, where each decimal digit is represented by a four-bit binary code.',
                              trigger: '6',
                            },
                            {
                              id: '6',
                              message: 'The BCD adder works by adding each corresponding digit of the BCD numbers, similar to how we add decimal numbers. However, if the sum of a digit exceeds 9, which is the largest value in BCD representation, a correction process called "BCD correction" is performed to adjust the result.',
                              trigger: '7',
                            },
                            {
                              id: '7',
                              message: 'Do you have any specific doubts or questions about the BCD adder concept?',
                              trigger: '8',
                            },
                            {
                              id: '8',
                              user: true,
                              trigger: '9',
                            },
                            {
                              id: '9',
                              message: 'I apologize, but I am a simple chatbot and may not have all the answers. However, I can provide you with resources and references to learn more about BCD adders. You can try searching online tutorials, videos, or textbooks on the topic. They can provide in-depth explanations and examples to enhance your understanding.',
                              end: true,
                            },
                          ]}
                        />
                        </>
                        
                        
                        ) : (
                          <div className="chatbot-icon fixed bottom-5 left-5 bg-blue-500 rounded-full p-2 cursor-pointer" onClick={() => setIsOpen(true)}>
                            <Lottie animationData={animation} className='h-16'/>
                          </div>
                        )}
                      </div>
              </div>
            </div>
            <div className="flex-1 bg-violet-50 p-8 font-semibold text-2xl">
             
              <div className="grid grid-cols-1">
              <button
                className="bg-green-300 hover:bg-blue-400 text-gray-800 py-2 px-4 rounded mt-4"
                onClick={handleToggle}
              >
                Change
              </button>
              </div>
              <motion.div
                className="bg-slate-100 rounded-lg shadow-lg h-96 mt-12"
                initial="hidden"
                animate="visible"
                transition={{ delay: 0.2 }}
              >
                <div className="flex flex-col items-center justify-center mt-4 h-108">
                  
                  {isToggleOn ? (
                    <div>
                      {/* {pdfData ? (
                        <Document
                          file={`data:application/pdf;base64,${pdfData}`}
                          options={{ workerSrc: '/pdf.worker.js' }} // Provide the path to pdf.worker.js
                        >
                          <Page pageNumber={1} />
                        </Document>
                      ) : (
                        <div>Loading my PDF...</div>
                      )} */}
                      <iframe
                        src="https://siiet.ac.in/wp-content/uploads/2019/05/CSE-II-I-DLD.pdf"
                        title="PDF Viewer"
                        height="380px"
                        width="720px">
                      </iframe>
                    </div>
                  ) : (
                    <div className='p-4'>
                    
                      <p>
                      - BCD is a numeric code used to represent decimals using binary bits.</p>
<p>- Each decimal digit is represented by a group of four bits in BCD, also known as the 8421 code.</p>
<p>- BCD code for each digit ranges from 0000 to 1001.</p>

<ul>
- Example: Convert (58)10 to BCD
<li>  - Decimal: 58</li>
<li>  - BCD: 0101 1000</li>
<li>  - BCD: 0101 1000</li>
<li>  - Therefore, (58)10 = (01011000)BCD</li>
  </ul>

                    </div>
                  )}
                </div>
              </motion.div>
              
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Learnnote;
