import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Navbar from "./NavBar";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";
import { useHistory } from "react-router-dom";



const Topiclist = () => {
  const [topics, setTopics] = useState([]);
 // const { currentUser } = useAuth();
  const history = useHistory();

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        // const response = await axios.post(
        //     `http://172.25.0.105:8000/cardData?email=${currentUser.email}`
        // );
        const response = await axios.get(
          "https://api.npoint.io/92bf600ec20a42b5fcc1"
      );
        setTopics(response.data);
      } catch (error) {
        console.error("Error fetching topics:", error);
      }
    };

    fetchTopics();
  }, []);
  const handleTopicClick = (topicName) => {
    history.push(`/learnnote?topic=${encodeURIComponent(topicName)}`);
  };

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <h1 className="text-3xl text-white font-bold mb-4 mt-4">Topic Wise Revision</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-24">
          {topics.map((topic, index) => (
            <motion.div
              key={index}
              className="bg-white rounded-lg shadow-md p-8 flex flex-col"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleTopicClick(topic.Topic_name)}
            >
              <motion.img
                src={topic.image_link}
                alt={topic.Topic_name}
                className="w-full h-40 object-cover mb-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              />
              <motion.p
                className="text-lg font-semibold mb-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.1 }}
              >
                {topic.Topic_name}
              </motion.p>
              <motion.p
                className="text-gray-500 text-sm md:text-base"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                {topic.description}
              </motion.p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Topiclist;
