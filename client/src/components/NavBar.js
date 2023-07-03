import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import icon from '../assets/logof3.svg';

const NavBar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const menuVariants = {
    open: { opacity: 1, y: 0 },
    closed: { opacity: 0, y: -100 },
  };

  return (
    <nav className="bg-white pt-3">
      <div className="max-w-7xl mx-auto sm:px-4 lg:px-8">
        <div className="flex justify-between h-8">
          <div className="flex-shrink-0 flex items-center">
            <Link to='/'>
            <img src={icon} alt="Learnmate" className="h-14"/>
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="flex space-x-4 text-violet-900 font-medium">
              <Link
                to="/"
                className="hover:text-gray-900 px-3 py-2 rounded-md text-sm"
              > 
                Home
              </Link>
              {/* <Link
                to="/about"
                className="hover:text-gray-900 px-3 py-2 rounded-md text-sm"
              >
                About
              </Link> */}
              {/* <Link
                to="/aibot"
                className="hover:text-gray-900 px-3 py-2 rounded-md text-sm"
              >
                Tutor
              </Link> */}
              {/* <Link
                to="/team"
                className="hover:text-gray-900 px-3 py-2 rounded-md text-sm"
              >
                Quiz
              </Link> */}
              
              <Link
                to="/dashboard"
                className="hover:text-gray-900 px-3 py-2 rounded-md text-sm"
              >
                Dashboard
              </Link>
              <Link
                to="/show-profile"
                className="hover:text-gray-900 px-3 py-2 rounded-md text-sm"
              >
                Profile
              </Link>
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <motion.button
              type="button"
              className="bg-white inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              aria-expanded="false"
              onClick={toggleMenu}
              initial={false}
              animate={isMenuOpen ? 'open' : 'closed'}
            >
              <span className="sr-only">Open main menu</span>
              <motion.svg
                className="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
                variants={{
                  closed: { rotate: 0 },
                  open: { rotate: 180 },
                }}
                transition={{ duration: 0.3 }}
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </motion.svg>
              <motion.svg
                className="hidden h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
                variants={{
                  closed: { rotate: 0 },
                  open: { rotate: 180 },
                }}
                transition={{ duration: 0.3 }}
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12"/>
              </motion.svg>
            </motion.button>
          </div>
        </div>
      </div>

      <motion.div
        className={`${isMenuOpen ? 'block' : 'hidden'} md:hidden`}
        initial="closed"
        animate={isMenuOpen ? 'open' : 'closed'}
        variants={menuVariants}
        transition={{ duration: 0.3 }}
      >
        <div className="px-2 pt-4 pb-3 space-y-1 sm:px-3 shadow-sm">
          <Link to="/" className="hover:text-gray-900 block px-3 py-2 text-base">Home</Link>
          <Link to="/about" className="hover:text-gray-900 block px-3 py-2 text-base">About</Link>
          <Link to="/events" className="hover:text-gray-900 block px-3 py-2 text-base">Events</Link>
          <Link to="/execom" className="hover:text-gray-900 block px-3 py-2 text-base">Execom</Link>
          <Link to="/highlights" className="hover:text-gray-900 block px-3 py-2 text-base">Highlights</Link>
          <Link to="/contacts" className="hover:text-gray-900 block px-3 py-2 text-base">Contacts</Link>
        </div>
      </motion.div>
    </nav>
  );
};

export default NavBar;