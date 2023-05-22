import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import 

function Home() {
  const buttonVariants = {
    hover: {
      scale: 1.1,
      transition: {
        duration: 0.3,
        yoyo: Infinity,
      },
    },
  };

  const quotes = [
    "Personalized AI tutor adapts to your learning style.",
    "Get instant feedback and guidance on your progress.",
    "Study at your own pace with customized lesson plans.",
    "Unlock your full potential with AI-powered tutoring.",
  ];

  return (
    <div className="flex h-screen w-screen">
      
      {/* Left Half */}
      <div className="w-1/2 bg-gray-200 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-6">Choose an option:</h1>
          <div className="space-y-4">
            <Link to="/uploadnotes">
            <motion.button
              className="bg-blue-500 text-white px-8 py-4 rounded-lg shadow-lg"
              variants={buttonVariants}
              whileHover="hover"
            >
              Upload notes
            </motion.button>
            </Link>
            <Link to="/recordnotes">
            <motion.button
              className="bg-green-500 text-white px-8 py-4 rounded-lg shadow-lg mx-8"
              variants={buttonVariants}
              whileHover="hover"
            >
              Record notes
            </motion.button>
            </Link>
          </div>
        </div>
      </div>

      {/* Right Half */}
      <div className="w-1/2 relative">
        <motion.div
          className="absolute top-0 left-0 right-0 bottom-0"
          initial={{ rotateY: 180, opacity: 0 }}
          animate={{ rotateY: 0, opacity: 1 }}
          transition={{ duration: 1 }}
        >
          <div className="bg-blue-500 w-full h-full"></div>
        </motion.div>

        <div className="absolute top-0 left-0 right-0 bottom-0 flex flex-col justify-center items-center p-10">
          <motion.div
            className="text-white text-2xl mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 1 }}
          >
            {quotes.map((quote, index) => (
              <motion.div
                key={index}
                className="mb-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: index * 4, duration: 2 }}
              >
                {quote}
              </motion.div>
            ))}
          </motion.div>
        </div>
        
      </div>
   
    </div>
  );
}

export default Home;