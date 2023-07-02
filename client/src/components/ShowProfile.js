import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useHistory } from 'react-router-dom';
import NavBar from './NavBar';
import Lottie from 'lottie-react';
import animation from '../assets/63004-profile-password-unlock.json';




const Landing = () => {
  const [error, setError] = useState('');
  const { currentUser, logout } = useAuth();
  const history = useHistory();

  async function handleLogout() {
    setError('');

    try {
      await logout();
      history.push('/login');
    } catch {
      setError('Failed to log out');
    }
  }

  return (
    <>
    <div className='w-screen'>
  <NavBar />
  <div className="flex items-center justify-center h-screen w-screen bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-2">  
        
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <Lottie animationData={animation} className="h-20"/>
          <h2 className="text-center text-2xl font-bold mb-6">Profile</h2>
          {error && <div className="text-red-500 text-center mb-4">{error}</div>}
          <strong>Email:</strong> {currentUser.email}
          <br />
          <Link to="/update-profile" className="bg-blue-500 text-white text-center font-bold py-2 px-4 block w-full mt-3 rounded">
            Update Profile
          </Link>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white font-bold py-2 px-4 block w-full mt-3 rounded"
          >
            Log Out
          </button>
          

        </div>
        </div>
      </div>
    </>
  );
};

export default Landing;
