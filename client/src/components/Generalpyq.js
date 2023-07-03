import React, { useEffect, useState } from 'react';
import Navbar from './NavBar';

const Generalpyq = () => {
  const questionPaper1 = [
    "1. Convert the decimal number (124)10 to binary and hexadecimal.",
    "2. Explain the concept of De-Morgan's theorem and provide an example.",
    "3. Express the Boolean function F = A · (B + C') as a product of maxterms.",
    "4. Discuss the differences between combinational and sequential circuits.",
    "5. Design a 3 x 8 decoder using two 2 x 4 decoders.",
    "6. Implement a full subtractor using a 3-input decoder and gates.",
    "7. Describe the triggering modes of flip-flops.",
    "8. What are excitation tables and how are they used?",
    "9. Draw the block diagram of a PAL and explain its features.",
    "10. Compare the features of CMOS and TTL logic devices."
  ];

  const questionPaper2 = [
    "1. Convert the octal number (457)8 to hexadecimal.",
    "2. Explain the process of converting a decimal number to binary.",
    "3. Differentiate between canonical and standard forms of Boolean functions with examples.",
    "4. What are universal gates? Why are they given that name?",
    "5. Discuss the concept of carry look-ahead addition and why it is necessary.",
    "6. Outline the design procedure for a combinational circuit.",
    "7. Compare synchronous and asynchronous circuits, highlighting their differences.",
    "8. Describe the operation of a master-slave flip-flop.",
    "9. Explain the differences between PLA and PAL.",
    "10. Define the terms fan out, propagation delay, and noise margin."
  ];

  return (
    <div>
      <div className="w-screen">
        <Navbar />
        <div className="flex flex-col items-center w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
          <h1 className="text-3xl text-white font-bold mb-4 mt-4">General PYQ</h1>
          <div className="text-left mt-4">
          <div className="text-left mt-4">
            <h2 className="text-2xl font-bold mb-2">Question paper 1:</h2>
            <ul className="pl-6 text-xl">
              {questionPaper1.map((question, index) => (
                <li key={index}>{question}</li>
              ))}
            </ul>
          </div>

          <div className="text-left mt-4">
            <h2 className="text-2xl font-bold mb-2">Question paper 2:</h2>
            <ul className="pl-6 text-xl">
              {questionPaper2.map((question, index) => (
                <li key={index}>{question}</li>
              ))}
            </ul>
          </div>
        </div>
        </div>
      </div>
    </div>
  );
};

export default Generalpyq;
