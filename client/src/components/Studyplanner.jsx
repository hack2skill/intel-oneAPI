import React from "react";
import Navbar from "./Navbar";

const StudyPlanner = () => {
  const studySchedule = [
    {
      day: 1,
      subjects: [
        { time: "10:00 AM", subject: "Math" },
        { time: "11:00 AM", subject: "Physics" },
      ],
    },
    {
      day: 2,
      subjects: [
        { time: "12:00 PM", subject: "English" },
        { time: "1:00 PM", subject: "Chemistry" },
      ],
    },
    {
      day: 3,
      subjects: [
        { time: "3:00 PM", subject: "History" },
        { time: "4:00 PM", subject: "Geography" },
      ],
    },
    {
      day: 4,
      subjects: [
        { time: "5:00 PM", subject: "Biology" },
        { time: "6:00 PM", subject: "Computer Science" },
      ],
    },
    {
      day: 5,
      subjects: [
        { time: "7:00 PM", subject: "Economics" },
        { time: "8:00 PM", subject: "Business Studies" },
      ],
    },
    {
      day: 6,
      subjects: [
        { time: "9:00 PM", subject: "Accountancy" },
        { time: "10:00 PM", subject: "Political Science" },
      ],
    },
  ];

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center h-screen w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <h1 className="text-3xl text-white font-bold mb-4 mt-4">Study Planner</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-6">
          {studySchedule.map((slot) => (
            <div
              key={slot.day}
              className="bg-white rounded-lg shadow-md p-4 flex flex-col"
            >
              <p className="text-lg font-semibold mb-2">Day {slot.day}</p>
              {slot.subjects.map((subject, index) => (
                <div key={index} className="flex items-center justify-between mb-2">
                  <p className="text-base md:text-lg font-semibold">{subject.time}</p>
                  <p className="text-gray-500 text-sm md:text-base">{subject.subject}</p>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StudyPlanner;
