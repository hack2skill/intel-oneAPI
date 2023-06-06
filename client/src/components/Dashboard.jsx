import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

import Navbar from "./Navbar";

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
      <div className="flex flex-col items-center justify-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <div className="flex flex-wrap justify-center gap-8 p-6">
          <motion.div
            className="w-full sm:w-1/2 bg-slate-50 rounded-lg shadow-lg p-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <h3 className="text-lg font-medium mb-4">Important Topics</h3>
            <pre>{impTopicContent}</pre>
          </motion.div>

          <motion.div
            className="w-full sm:w-1/2 bg-slate-50 rounded-lg shadow-lg p-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }}
          >
            <h3 className="text-lg font-medium mb-4">Topic List</h3>
            <pre>{topicListContent}</pre>
          </motion.div>

          <motion.div
            className="w-full sm:w-1/2 bg-slate-50 rounded-lg shadow-lg p-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.4 }}
          >
            <h3 className="text-lg font-medium mb-4">Cluster Questions</h3>
            <pre>{clusterQuestionsContent}</pre>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export { Dashboard as default };
