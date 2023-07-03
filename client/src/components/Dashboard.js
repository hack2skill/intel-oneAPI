import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Navbar from "./NavBar";
import { Link } from "react-router-dom";
import Lottie from "lottie-react";
import studyplan from "../assets/121104-woman-discovering-business-statistics.json";
import repetition from "../assets/100679-wallp-repetitions-animation.json";
import generalp from "../assets/132573-marking-exam-questions.json";
import sorted from "../assets/96665-toggle-sort-menu-transition.json";
import learn from "../assets/54639-boy-studying-science.json";
import quiz from "../assets/133329-yellow-quiz.json";



const COLORS = ["#0088FE", "#FFBB28"];

const Dashboard = () => {
  const [impTopicContent, setImpTopicContent] = useState("");
  const [topicListContent, setTopicListContent] = useState("");
  const [clusterQuestionsContent, setClusterQuestionsContent] = useState("");
  const [module1Content, setModule1Content] = useState("");
  const [showModule1Content, setShowModule1Content] = useState(false);

  useEffect(() => {
    fetch("Files/generated_files/imp_topic_list.txt")
      .then((response) => response.text())
      .then((text) => setImpTopicContent(text))
      .catch((error) => console.log(error));

    fetch("Files/generated_files/topic_list.txt")
      .then((response) => response.text())
      .then((text) => setTopicListContent(text))
      .catch((error) => console.log(error));

    fetch("Files/generated_files/cluster_questions.txt")
      .then((response) => response.text())
      .then((text) => setClusterQuestionsContent(text))
      .catch((error) => console.log(error));
  }, []);

  const fetchModule1Content = () => {
    fetch("Files/generated_files/summarised_notes/module1_summarized.txt")
      .then((response) => response.text())
      .then((text) => {
        setModule1Content(text);
        setShowModule1Content(true);
      })
      .catch((error) => console.log(error));
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { duration: 0.5 } },
  };

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
         <div className="grid grid-cols-2 gap-6 py-12 h-4">
       
          <Link to="/days">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <Lottie animationData={studyplan} className="h-20" />
            <h2 className="mb-4">Study plan</h2>
            
          </motion.div>
          </Link>
          <Link to="/topiclist">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <Lottie animationData={learn} className="h-20" />
            <h2 className="mb-4">Topic Learn</h2>
            
          </motion.div>
          </Link>
          <Link to="/quiz">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <Lottie animationData={quiz} className="h-20" />
            <h2 className="mb-4">Quiz</h2>
            
          </motion.div>
          </Link>

          <Link to="/sortedpyq">
        <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6 w-72"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <Lottie animationData={sorted} className="h-20" />
            <h2 className="mb-4">Sorted PYQ</h2>
           
          </motion.div>
          </Link>
          <Link to="/generalpyq">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <Lottie animationData={generalp} className="h-20" />
            <h2 className="mb-4">General Question Paper</h2>
           
          </motion.div>
          </Link>
          <Link to="/repetitivepyq">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <Lottie animationData={repetition} className="h-20" />
            <h2 className="mb-4">Repetitive questions</h2>
            
          </motion.div>
          </Link>
               
          </div>        
        </div>
      </div>
    
  );
};

export { Dashboard as default };
