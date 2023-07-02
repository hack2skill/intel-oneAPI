import React from 'react';
import Navbar from './NavBar';

const Repetitivepyq = () => {
  const questions = [
    {
      "question": "Differentiate between decimal numbers and binary numbers.",
      "frequency": 2
  },
  {
      "question": "Convert the binary number 101010 to octal and hexadecimal.",
      "frequency": 2
  },
  {
      "question": "Explain the concept of compliments in digital systems.",
      "frequency": 3
  },
  {
      "question": "Perform the operation of finding the 2's complement for the binary number 011001.",
      "frequency": 2
  },
  {
      "question": "Discuss the concept of signed binary numbers.",
      "frequency": 2
  },
  {
      "question": "Define binary codes and provide some examples.",
      "frequency": 2
  },
  {
      "question": "Compare and contrast binary storage and registers.",
      "frequency": 2
  },
  {
      "question": "Explain the use of binary logic in digital systems.",
      "frequency": 2
  },
  {
      "question": "Describe the axiomatic definition of boolean algebra.",
      "frequency": 2
  },
  {
      "question": "State and prove the basic theorems and properties of boolean algebra.",
      "frequency": 3
  },
  {
      "question": "Differentiate between canonical and standard forms of boolean functions.",
      "frequency": 2
  },
  {
      "question": "Perform logic operations using boolean algebra.",
      "frequency": 2
  },
  {
      "question": "Introduce the concept of digital logic gates.",
      "frequency": 2
  },
  {
      "question": "Use Karnaugh map to perform gate level minimisation.",
      "frequency": 5
  },
  {
      "question": "Simplify the boolean expression using two-variable Karnaugh map.",
      "frequency": 2
  },
  {
      "question": "Explore the methods of simplification using three, four, and five variable Karnaugh maps.",
      "frequency": 2
  },
  {
      "question": "Explain the concept of Product of Sums and Sum of Products simplification.",
      "frequency": 2
  },
  {
      "question": "Discuss the implementation of NAND and NOR gates.",
      "frequency": 2
  },
  {
      "question": "Introduce the Exclusive OR function and its applications.",
      "frequency": 2
  },
  {
      "question": "Apply the Quine McCluskey technique for simplification.",
      "frequency": 2
  }
  ];

  const importantTopics = [
    "Binary Numbers",
    "Base conversions",
    "Octal and Hexadecimal numbers",
    "Compliments",
    "Operations of compliments",
    "Signed binary numbers",
    "Binary codes",
    "Binary storage and Registers",
    "Binary Logic",
    "What is the purpose of compliments in binary numbers?",
    "Explain the process of base conversion.",
    "Compare and contrast octal and hexadecimal numbers.",
    "How are signed binary numbers represented?",
    "Discuss the different binary codes.",
    "Describe the storage and registers used in binary systems.",
    "Define binary logic and its relation to Boolean algebra.",
    "What are the axiomatic definitions of boolean algebra?",
    "List the basic theorems and properties of boolean algebra.",
    "Demonstrate the logic operations used in digital logic gates.",
    "Provide an introduction to gate level minimisation techniques.",
    "How can Karnaugh maps be used to minimise logic gates?",
    "Explain the concept of product of sums and sum of products simplification.",
    "Discuss the implementation of NAND and NOR gates.",
    "What is the purpose of an exclusive OR function?",
    "Describe the Quine McCluskey technique for simplification of boolean expressions."
  ];

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <h1 className="text-3xl text-white font-bold mb-4 mt-4">Repetitive PYQ</h1>
        <div className="text-xl">
         
          <ul className='text-left text-3xl'>
            {questions.map((q, index) => (
              <li key={index}>{`${index + 1}. ${q.question}`}</li>
            ))}
          </ul>
          <h2 className="text-left text-3xl font-bold mt-6">Important Topics:</h2>
          <ul className='text-left'>
            {importantTopics.map((topic, index) => (
              <li key={index}>{topic}</li>
            ))}
          </ul>
          <br />
          <br />
        </div>
      </div>
    </div>
  );
};

export default Repetitivepyq;
