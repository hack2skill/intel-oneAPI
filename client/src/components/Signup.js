import React, { useRef, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useHistory } from 'react-router-dom';

const Signup = () => {
  const emailRef = useRef();
  const passwordRef = useRef();
  const passwordConfirmRef = useRef();
  const { signup } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  async function handleSubmit(e) {
    e.preventDefault();
    if (passwordRef.current.value !== passwordConfirmRef.current.value) {
      return setError('Passwords do not match');
    }
    try {
      setError('');
      setLoading(true);
      await signup(emailRef.current.value, passwordRef.current.value);
      history.push('/');
    } catch (error) {
      console.log(error);
      setError('Failed to create an account');
    }
    setLoading(false);
  }

  return (
    <>
      <div className="flex items-center justify-center h-screen w-screen bg-gradient-to-tr from-violet-700 via-green-600 to-green-400">
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h2 className="text-center text-2xl font-bold mb-4">Sign Up</h2>
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
                className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none"
                required
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
                className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none"
                required
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
                className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none"
                required
              />
            </div>
            <button
              disabled={loading}
              className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded"
              type="submit"
            >
              Sign Up
            </button>
          </form>
          <div className="w-full text-center mt-2">
          Already have an account? <Link to="/login" className="text-blue-500 hover:underline">Log In</Link>
        </div>
        </div>
        
      </div>
    </>
  );
};

export default Signup;
