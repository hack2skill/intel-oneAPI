import React from 'react';
import Navbar from './NavBar';

const Sortedpyq = () => {
  const modules = [
    {
      title: 'Module 1',
      color: 'bg-orange-400',
      questions: [
        'Differentiate between decimal numbers and binary numbers.',
        'Convert the binary number 101010 to octal and hexadecimal.',
        'Explain the concept of compliments in digital systems.',
        'Perform the operation of finding the 2\'s complement for the binary number 011001.',
        'Discuss the concept of signed binary numbers.',
'Define binary codes and provide some examples.',
'Differentiate between decimal numbers and binary numbers.',
    'Convert the binary number 101010 to octal and hexadecimal.',
    'Explain the concept of compliments in digital systems.',
    'Perform the operation of finding the 2\'s complement for the binary number 011001.',
    'Discuss the concept of signed binary numbers.',
    'Define binary codes and provide some examples.',
    'Compare and contrast binary storage and registers.',
    'Explain the use of binary logic in digital systems.',
    'Describe the axiomatic definition of Boolean algebra.',
    'State and prove the basic theorems and properties of Boolean algebra.',
    'Define Boolean functions and give some examples.',
    'Differentiate between canonical and standard forms of Boolean functions.',
    'Perform logic operations using Boolean algebra.',
    'Introduce the concept of digital logic gates.',
    'Use Karnaugh map to perform gate-level minimization.',
    'Simplify the Boolean expression using a two-variable Karnaugh map.',
    'Explore the methods of simplification using three, four, and five-variable Karnaugh maps.',
    'Explain the concept of Product of Sums and Sum of Products simplification.',
    'Discuss the implementation of NAND and NOR gates.',
    'Introduce the Exclusive OR function and its applications.',
    'Apply the Quine McCluskey technique for simplification.',
    'Define octal numbers and provide examples.',
    'Convert the decimal number 75 to binary, octal, and hexadecimal.',
    'Discuss the properties and advantages of hexadecimal numbers.',
    'Perform the operation of finding the 1\'s complement for the binary number 110110.',
    'Explain the concept of overflow in binary arithmetic.',
    'Define Gray code and its use in digital systems.',
    'Discuss the concept of arithmetic overflow and underflow in digital systems.',
    'Describe the concept of parity and its use in error detection.',
    'Explain the concept of logical shift and arithmetic shift operations.',
    'Discuss the representation of negative numbers using sign and magnitude method.',
    'Define one\'s complement and its representation of negative numbers.',
    'Describe the process of subtracting binary numbers using one\'s complement.',
    'Discuss the concept of two\'s complement and its representation of negative numbers.',
    'Perform the operation of adding binary numbers using two\'s complement.',
    'Explain the concept of excess-3 code and its use in BCD arithmetic.',
    'Discuss the representation of decimal numbers in BCD code.',
    'Describe the process of BCD addition and subtraction.',
    'Explain the concept of ASCII code and its use in character representation.',
    'Discuss the concept of digital memory and its organization.',
    'Describe the concept of random access memory (RAM) and its types.',
    'Explain the concept of read-only memory (ROM) and its types.',
    'Discuss the concept of memory address and data bus.',
    'Describe the concept of memory mapping and its use in addressing.',
    'Explain the concept of memory hierarchy and its levels.',
    'Discuss the concept of cache memory and its types.',
    'Describe the concept of virtual memory and its advantages.',
    'Explain the concept of memory management unit (MMU) and its functions.',
    'Discuss the concept of memory allocation and deallocation.',
    'Describe the concept of memory protection and its importance in operating systems.'
      ]
    },
    {
      title: 'Module 2',
      color: 'bg-blue-400',
      questions:  [
        'Define the concept of combinational circuits.',
        'Explain the difference between combinational and sequential circuits.',
        'Discuss the basic building blocks of combinational circuits.',
        'Describe the operation of logic gates.',
        'Define and compare different types of logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR).',
        'Explain the concept of truth tables and their use in combinational circuits.',
        'Discuss the concept of Boolean functions and their representation in combinational circuits.',
        'Describe the process of designing combinational circuits using Boolean algebra and truth tables.',
        'Explain the concept of multiplexers and their use in combinational circuits.',
        'Discuss the concept of decoders and their applications in combinational circuits.',
        'Define the concept of encoders and their use in combinational circuits.',
        'Describe the operation of adders and subtractors in combinational circuits.',
        'Explain the concept of half adders and full adders.',
        'Discuss the design and implementation of magnitude comparators in combinational circuits.',
        'Define the concept of multiplexed displays and their use in combinational circuits.',
        'Discuss the design and implementation of code converters in combinational circuits.',
        'Explain the concept of arithmetic logic units (ALUs) and their applications.',
        'Discuss the design and implementation of ALUs in combinational circuits.',
        'Define the concept of programmable logic devices (PLDs) and their types.',
        'Explain the process of designing combinational circuits using PLDs.',
        'Discuss the concept of field-programmable gate arrays (FPGAs) and their use in combinational circuits.',
        'Define the concept of carry look-ahead adders and their advantages over ripple carry adders.',
        'Explain the concept of multiplexer-based carry look-ahead adders.',
        'Discuss the design and implementation of parallel binary adders using carry look-ahead technique.',
        'Describe the operation of binary subtractors using complement methods.',
        'Explain the concept of serial binary adders and subtractors.',
        'Discuss the design and implementation of parallel binary subtractors using carry look-ahead technique.',
        'Define the concept of magnitude comparators and their applications in sequential circuits.',
        'Explain the design and implementation of sequential circuits using flip-flops.',
        'Discuss the concept of clock signals and their role in sequential circuits.',
        'Define the concept of latches and their types.',
        'Explain the operation of D flip-flops and their use in sequential circuits.',
        'Discuss the design and implementation of registers in sequential circuits.',
        'Define the concept of counters and their types.',
        'Explain the operation of synchronous and asynchronous counters.',
        'Discuss the design and implementation of modulo-n counters.',
        'Define the concept of shift registers and their types.',
        'Explain the operation of parallel-in parallel-out (PIPO) shift registers.',
        'Discuss the design and implementation of serial-in serial-out (SISO) shift registers.',
        'Define the concept of universal shift registers and their applications.',
        'Explain the operation of ring counters and Johnson counters.',
        'Discuss the design and implementation of synchronous and asynchronous sequential circuits.',
        'Define the concept of finite state machines (FSMs) and their types.',
        'Explain the design and implementation of Moore and Mealy state machines.',
        'Discuss the concept of state minimization and state assignment in sequential circuits.',
        'Define the concept of clock skew and its impact on sequential circuits.',
        'Explain the concept of metastability and its prevention techniques in sequential circuits.',
        'Discuss the concept of synchronous and asynchronous reset in sequential circuits.',
        'Define the concept of timing diagrams and their use in sequential circuits.',
        'Explain the concept of race conditions and their prevention in sequential circuits.',
       
        
    ]
    },
    {
      title: 'Module 3',
      color: 'bg-red-400',
      questions: [
        'What is a sequential circuit?',
    'Differentiate between combinational and sequential circuits.',
    'Explain the concept of flip-flops in sequential circuits.',
    'Discuss the different types of flip-flops.',
    'Describe the operation of SR flip-flop.',
    'Explain the operation of JK flip-flop.',
    'Discuss the functionality of D flip-flop.',
    'Describe the characteristics of T flip-flop.',
    'Explain the concept of clock signal in sequential circuits.',
    'Discuss the concept of setup time and hold time in flip-flops.',
    'What is the difference between synchronous and asynchronous sequential circuits?',
    'Explain the concept of state in sequential circuits.',
    'Describe the state table and state diagram representation of sequential circuits.',
    'Discuss the concept of Moore and Mealy machines.',
    'Explain the concept of race condition in sequential circuits.',
    'Discuss the concept of critical race and non-critical race in sequential circuits.',
    'Describe the concept of hazard in digital circuits.',
    'Explain the concept of static and dynamic hazards.',
    'Discuss the methods of hazard elimination in sequential circuits.',
    'Describe the concept of clock skew and its impact on sequential circuits.',
    'Explain the concept of metastability in sequential circuits.',
    'Discuss the techniques to mitigate metastability in digital systems.',
    'Describe the concept of synchronous counters.',
    'Explain the operation of binary ripple counter.',
    'Discuss the concept of synchronous counter design.',
    'Describe the concept of asynchronous counters.',
    'Explain the operation of Johnson counter.',
    'Discuss the concept of shift registers.',
    
      ]
    },
    {
      title: 'Module 4',
      color: 'bg-yellow-400',
      questions: [
        'Explain the concept of computer networks.',
    'Discuss the different types of network topologies.',
    'Explain the concept of network protocols.',
    'Discuss the layers of the OSI model.',
    'Explain the functions of each layer in the OSI model.',
    'Discuss the advantages and disadvantages of centralized and decentralized networks.',
    'Explain the concept of IP addressing and subnetting.',
    'Discuss the role of routers in computer networks.',
    'Explain the concept of TCP/IP protocol suite.',
    'Discuss the differences between TCP and UDP protocols.',
    'Explain the concept of network security and its importance.',
    'Discuss the different types of network attacks and countermeasures.',
    'Explain the concept of firewalls and their role in network security.',
    'Discuss the concept of virtual private networks (VPNs) and their benefits.',
    'Explain the concept of network address translation (NAT) and its use in IP addressing.',
    'Discuss the concept of network troubleshooting and common techniques used.',
    'Explain the concept of network monitoring and its importance.',
    'Discuss the different network management tools and their functions.',
    'Explain the concept of cloud computing and its benefits in network infrastructure.',
    'Discuss the concept of content delivery networks (CDNs) and their advantages.',
    'Explain the concept of network virtualization and its use in data centers.',
    'Discuss the concept of software-defined networking (SDN) and its advantages.',
    'Explain the concept of network congestion and methods to alleviate it.',
    'Discuss the concept of quality of service (QoS) and its role in network performance.',
    'Explain the concept of network load balancing and its benefits.',
    'Discuss the concept of network redundancy and its importance in fault tolerance.',
    'Explain the concept of network scalability and its challenges.',
    'Discuss the concept of network standards and their role in interoperability.',
    'Explain the concept of network protocols for wireless networks.',
    'Discuss the different wireless communication technologies.',
    'Explain the concept of mobile network architectures.',
    'Discuss the concept of Internet of Things (IoT) and its impact on network infrastructure.',
    'Explain the concept of network security protocols and encryption techniques.',
    'Discuss the challenges and solutions for securing wireless networks.',
    'Explain the concept of network performance optimization.',
    'Discuss the concept of network planning and design.',
    'Explain the concept of network documentation and its importance.',
    'Discuss the concept of network administration and its responsibilities.',
    'Explain the concept of network upgrades and migration strategies.',
    'Discuss the concept of network monitoring and troubleshooting tools.',
    'Explain the concept of network capacity planning and its importance.',
    'Discuss the concept of network disaster recovery and business continuity.',
    'Explain the concept of network audits and security assessments.',
    'Discuss the ethical and legal considerations in computer networks.',
    'Explain the concept of network governance and policies.',
    'Discuss the concept of network outsourcing and its benefits.',
    'Explain the concept of network virtualization technologies.',
    'Discuss the concept of network automation and its advantages.',
    'Explain the concept of network analytics and its applications.',
      ]
    },
    // Add more modules as needed
  ];

  return (
    <div className="w-screen">
      <Navbar />
      <div className="flex flex-col items-center w-screen bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-3">
        <h1 className="text-3xl text-white font-bold mb-4 mt-4">Sorted PYQ</h1>
        
        {modules.map((module, index) => (
          <div key={index}>
            <h2 className="text-2xl font-semibold text-white mb-2 mt-4">{module.title}</h2>
            <div className={`rounded-lg shadow-lg p-6 ${module.color}`}>
              {module.questions.map((question, questionIndex) => (
                <div key={questionIndex} className="mb-4">
                  <h3 className="text-lg font-semibold">{`${questionIndex + 1}. ${question}`}</h3>
                </div>
              ))}
            </div>
            <br />
          </div>
        ))}
        
      </div>
    </div>
  );
};

export default Sortedpyq;
