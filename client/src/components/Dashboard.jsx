import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Navbar from "./Navbar";
import { Link } from "react-router-dom";

const data = {
  coursesCompleted: 5,
  coursesInProgress: 3,
  coursesEnrolled: 8,
  performance: [
    { subject: "LD", score: 80 },
    { subject: "DSA", score: 75 },
    { subject: "OOPS", score: 90 },
    { subject: "CAO", score: 85 },
    { subject: "ALU", score: 70 },
  ],
  attentionRate: 85,
};

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
         <div className="grid grid-cols-4 gap-6 py-12 h-4">
        <Link to="/sortedpyq">
        <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6 w-72"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
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
            <h2 className="mb-4">Repetitive questions</h2>
            
          </motion.div>
          </Link>
          <Link to="/studyplanner">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <h2 className="mb-4">Study plan</h2>
            
          </motion.div>
          </Link>
          
          
        
        
          </div> 

        <div className="grid grid-cols-2 gap-16 py-16">
          <div className="grid grid-cols-2 gap-4">
          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6 h-88 w-60"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <h3 className="text-xl mb-4">Important Topics</h3>
            <pre>{impTopicContent}</pre>
            <p>NFA and DFA</p>
            <p>NFA to DFA conversion</p>
            <p>Minimisation</p>
            <p>Ardens Theorem</p>
          </motion.div>

          <motion.div
            className="bg-slate-100 rounded-lg shadow-lg py-6 w-60"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <h3 className="text-xl mb-4">Topic List</h3>
            <pre>{topicListContent}</pre>
            <p>Finite state systems</p>
            <p>Definitions</p>
            <p>Minimisation</p>
            <p>Moore and Mealy machinesm</p>
          </motion.div>
          </div>

          <motion.div
            className="bg-slate-50 rounded-lg shadow-lg py-6 w-120 h-96"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.4 }}
          >
            <h3 className="text-lg font-semibold mb-4">Cluster Questions</h3>
            <iframe
              src="http://www.gpcet.ac.in/wp-content/uploads/2017/04/flat-10.pdf"
              className="w-full h-full"
              title="PDF Viewer"
            />
          </motion.div>

         
        </div>
      </div>
    </div>
  );
};

export { Dashboard as default };
