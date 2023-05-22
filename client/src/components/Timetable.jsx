import React, { useState } from 'react';

const Timetable = () => {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [numDays, setNumDays] = useState('');

  const API_KEY = 'api key';

  const handleMessage = async () => {
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${API_KEY}`,
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'system',
              content: `Create a study plan in a day by day according to module summary and pyq given. I want to complete it in ${numDays} days.`,
            },
            {
              role: 'user',
              content: input,
            },
          ],
        }),
      });

      const data = await response.json();
      const message = data.choices[0].message.content;

      setOutput(formatOutput(message));
    } catch (error) {
      console.error(error);
    }
  };

  const formatOutput = (message) => {
    // Split the message into paragraphs based on new lines
    const paragraphs = message.split('\n\n');

    // Map each paragraph and add appropriate formatting
    const formattedOutput = paragraphs.map((paragraph, index) => {
      // Check if the paragraph is a bullet point (starts with '-')
      if (paragraph.startsWith('-')) {
        const bulletPoints = paragraph.split('\n-'); // Split into individual bullet points
        return (
          <ul key={index} className="list-disc pl-8 mb-4">
            {bulletPoints.map((bulletPoint, bulletIndex) => (
              <li key={bulletIndex}>{bulletPoint}</li>
            ))}
          </ul>
        );
      } else {
        // Split the paragraph into days
        const days = paragraph.split('\n\nDay');

        // Map each day and create a card for it
        const dayCards = days.map((day, dayIndex) => {
          // Split the day into tasks
          const tasks = day.split('\n-');

          // Remove the 'Day X' label from the first task
          const firstTask = tasks[0].replace('Day', '').trim();

          return (
            <div key={dayIndex} className="mb-4">
              <h3 className="text-lg font-bold mb-2">Day {firstTask}</h3>
              <ul className="list-disc pl-8">
                {tasks.slice(1).map((task, taskIndex) => (
                  <li key={taskIndex}>{task}</li>
                ))}
              </ul>
            </div>
          );
        });

        return (
          <div key={index} className="mb-4">
            {dayCards}
          </div>
        );
      }
    });

    return formattedOutput;
  };

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleNumDaysChange = (event) => {
    setNumDays(event.target.value);
  };

  return (
    <div className="bg-gray-100 py-8 px-4 w-screen">
      <h1 className="text-3xl font-bold mb-6 text-center">Study Plan</h1>
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <textarea
          rows={4}
          value={input}
          onChange={handleInputChange}
          className="w-full resize-none border border-gray-300 rounded-lg p-2 mb-4"
          placeholder="Enter your study plan here..."
        />
        <input
          type="number"
          value={numDays}
          onChange={handleNumDaysChange}
          className="w-full border border-gray-300 rounded-lg p-2 mb-4"
          placeholder="Number of days"
        />
        <button
          onClick={handleMessage}
          className="bg-blue-500 hover:bg-blue-600 text-white rounded-lg px-4 py-2 text-center w-full"
        >
          Generate Plan
        </button>
      </div>
      <div className="bg-white rounded-lg shadow-md p-6">
        {output}
      </div>
    </div>
  );
};

export default Timetable;