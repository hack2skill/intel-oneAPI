import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import NavBar from './NavBar';
import Lottie from 'lottie-react';
import QuizAnimation from '../assets/92464-321-go.json';

const Quiz = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [score, setScore] = useState(0);
  const [quizCompleted, setQuizCompleted] = useState(false);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('https://api.npoint.io/93f3478daedcdf44a577');
        setQuestions(response.data.questions);
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    };

    fetchQuestions();
  }, []);

  const handleOptionSelect = (optionIndex) => {
    setSelectedOption(optionIndex);
  };

  const handleNextQuestion = () => {
    if (selectedOption !== null) {
      const currentQuestion = questions[currentQuestionIndex];
      const isCorrect = selectedOption === currentQuestion.correct_option;
      setScore((prevScore) => prevScore + (isCorrect ? 1 : -1));

      if (currentQuestionIndex + 1 === questions.length) {
        setQuizCompleted(true);
      } else {
        setSelectedOption(null);
        setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
      }
    }
  };

  const renderQuestion = () => {
    if (questions.length === 0) {
      return null; // Return null or a loading indicator while waiting for data
    }
    const currentQuestion = questions[currentQuestionIndex];

    return (
      <div className="bg-white rounded-lg shadow-md p-8 flex flex-col">

        <h2 className="text-xl font-semibold mb-4">{currentQuestion.question}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {currentQuestion.options.map((option, index) => (
            <motion.button
              key={index}
              className={`${
                selectedOption === index ? 'bg-green-400 text-white' : 'bg-gray-200 text-gray-700'
              } rounded-md py-2 px-4`}
              onClick={() => handleOptionSelect(index)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {option}
            </motion.button>
          ))}
        </div>
        <button
          className="bg-blue-500 text-white rounded-md py-2 px-4 mt-4"
          onClick={handleNextQuestion}
          disabled={selectedOption === null}
        >
          {currentQuestionIndex + 1 === questions.length ? 'Finish' : 'Next'}
        </button>
      </div>
    );
  };

  const renderQuizCompleted = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 flex flex-col">
        <h2 className="text-2xl font-semibold mb-4">Quiz Completed!</h2>
        <p className="text-lg">
          Your score is <span className="font-bold">{score}</span>.
        </p>
      </div>
    );
  };

  return (
    <div className="w-screen">
      <NavBar />
      <div className="flex flex-col items-center justify-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <Lottie animationData={QuizAnimation} className="w-24 h-32" />
        <h1 className="text-3xl text-white font-bold  mb-12">Quiz</h1>
          <div className='flex items-center justify-center'>
        {!quizCompleted ? renderQuestion() : renderQuizCompleted()}
        </div>
      </div>
    </div>
  );
};

export default Quiz;
