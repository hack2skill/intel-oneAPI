import React, { useRef, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useHistory } from 'react-router-dom';
import NavBar from './NavBar';

export default function UpdateProfile() {
  const emailRef = useRef();
  const passwordRef = useRef();
  const passwordConfirmRef = useRef();
  const { currentUser, updatePassword, updateEmail } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  function handleSubmit(e) {
    e.preventDefault();
    if (passwordRef.current.value !== passwordConfirmRef.current.value) {
      return setError('Passwords do not match');
    }

    const promises = [];
    setLoading(true);
    setError('');

    if (emailRef.current.value !== currentUser.email) {
      promises.push(updateEmail(emailRef.current.value));
    }
    if (passwordRef.current.value) {
      promises.push(updatePassword(passwordRef.current.value));
    }

    Promise.all(promises)
      .then(() => {
        history.push('/');
      })
      .catch(() => {
        setError('Failed to update account');
      })
      .finally(() => {
        setLoading(false);
      });
  }

  return (
    <>
        <div className='w-screen'>
  <NavBar />
  <div className="bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-2">  
      <div className=' flex items-center justify-center h-screen w-screen'>
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h2 className="text-center text-2xl font-bold mb-4">Update Profile</h2>
          {error && <div className="bg-red-500 text-white text-center py-2 mb-4">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="block text-gray-700 font-semibold mb-2">
                Email
              </label>
              <input
                type="email"
                id="email"
                ref={emailRef}
                required
                defaultValue={currentUser.email}
                className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="password" className="block text-gray-700 font-semibold mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                ref={passwordRef}
                placeholder="Leave blank to keep the same"
                className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="password-confirm" className="block text-gray-700 font-semibold mb-2">
                Password Confirmation
              </label>
              <input
                type="password"
                id="password-confirm"
                ref={passwordConfirmRef}
                placeholder="Leave blank to keep the same"
                className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none"
              />
            </div>
            <button
              disabled={loading}
              className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded"
              type="submit"
            >
              Update
            </button>
          </form>
        </div>
        <div className="w-full text-center mt-2">
          <Link to="/" className="text-blue-500 hover:underline">
            Cancel
          </Link>
        </div>
      </div>
      </div>
      </div>
    </>
  );
}
