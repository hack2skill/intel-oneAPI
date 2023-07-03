import React from "react";
import Navbar from "./NavBar";

const topics = [
  {
    "topic": "Theory_Notes",
    "date": "01/07/2023"
  },
  {
    "topic": "Introduction_to_Digital_System",
    "date": "02/07/2023"
  },
  {
    "topic": "Decimal_Number_System",
    "date": "03/07/2023"
  },
  {
    "topic": "Binary_Number_System",
    "date": "04/07/2023"
  },
  {
    "topic": "Octal_Number_System",
    "date": "05/07/2023"
  },
  {
    "topic": "Hexadecimal_Number_System",
    "date": "06/07/2023"
  },
  {
    "topic": "Number_Systems",
    "date": "07/07/2023"
  },
  {
    "topic": "Number_Base_Conversions",
    "date": "08/07/2023"
  },
  {
    "topic": "Conversion_of_Binary_to_Decimal",
    "date": "09/07/2023"
  },
  {
    "topic": "Conversion_of_Decimal_to_Binary",
    "date": "10/07/2023"
  },
  {
    "topic": "Conversion_of_Octal_to_Decimal",
    "date": "11/07/2023"
  },
  {
    "topic": "Conversion_of_Hexadecimal_to_Decimal",
    "date": "12/07/2023"
  },
  {
    "topic": "Decimal_to_Binary_Conversion",
    "date": "13/07/2023"
  },
  {
    "topic": "Decimal_to_Octal_Conversion",
    "date": "14/07/2023"
  },
  {
    "topic": "Decimal_to_Hexadecimal_Conversion",
    "date": "15/07/2023"
  },
  {
    "topic": "Positional_Weighted_Number_System",
    "date": "16/07/2023"
  },
  {
    "topic": "Comparison_of_Analog_and_Digital_Systems",
    "date": "17/07/2023"
  },
  {
    "topic": "Advantages_of_Boolean_Algebra",
    "date": "18/07/2023"
  },
  {
    "topic": "Axioms_of_Boolean_Algebra",
    "date": "19/07/2023"
  },
  {
    "topic": "Laws_of_Boolean_Algebra",
    "date": "20/07/2023"
  },
  {
    "topic": "Idempotence_Laws",
    "date": "21/07/2023"
  },
  {
    "topic": "Null_Law",
    "date": "22/07/2023"
  },
  {
    "topic": "Absorption_Law",
    "date": "23/07/2023"
  },
  {
    "topic": "Identity_Law",
    "date": "24/07/2023"
  },
  {
    "topic": "Double_Negation_Law",
    "date": "25/07/2023"
  },
  {
    "topic": "De_Morgan's_Theorem",
    "date": "26/07/2023"
  },
  {
    "topic": "Consensus_Theorem",
    "date": "27/07/2023"
  },
  {
    "topic": "Factoring_or_multiplying_out_of_expressions",
    "date": "28/07/2023"
  },
  {
    "topic": "Reduction_of_Boolean_Expressions",
    "date": "29/07/2023"
  },
  {
    "topic": "Boolean_Expressions_and_Karnaugh_Maps",
    "date": "30/07/2023"
  },
  {
    "topic": "K-Maps",
    "date": "31/07/2023"
  },
  {
    "topic": "Minterms_&_Maxterms_for_3_variables",
    "date": "01/08/2023"
  },
  // ... Rest of the topics and dates
];

const StudyPlanner = () => {
  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center w-screen text-center bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <h1 className="text-3xl text-white font-bold mb-4 mt-4">Study Planner</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-24">
          {topics.map((topic, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md p-8 flex flex-col">
              <p className="text-lg font-semibold mb-2">Day {index + 1}</p>
              <div>
                <h6 className="text-gray-500 text-sm md:text-base">{topic.date}</h6>
                <p className="text-gray-700 text-md md:text-base">{topic.topic}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StudyPlanner;
