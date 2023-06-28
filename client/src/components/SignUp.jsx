import React, { useState } from 'react';
import { motion } from 'framer-motion';

const SignUp = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSignUp = (event) => {
    event.preventDefault();

    if (password !== confirmPassword) {
      alert('Password and Confirm Password do not match');
      return;
    }

    const user = {
      email,
      password
    };

    saveUser(user);

    alert('Sign up successful');

    setEmail('');
    setPassword('');
    setConfirmPassword('');
  };

  const saveUser = (user) => {
    console.log('User data:', user);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <motion.h1
        className="text-3xl font-bold mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Sign Up
      </motion.h1>
      <form
        onSubmit={handleSignUp}
        className="flex flex-col items-center space-y-4"
      >
        <label htmlFor="email" className="text-lg">
          Email:
        </label>
        <input
          type="email"
          id="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border rounded-lg px-4 py-2 w-64"
        />

        <label htmlFor="password" className="text-lg">
          Password:
        </label>
        <input
          type="password"
          id="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border rounded-lg px-4 py-2 w-64"
        />

        <label htmlFor="confirm-password" className="text-lg">
          Confirm Password:
        </label>
        <input
          type="password"
          id="confirm-password"
          required
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className="border rounded-lg px-4 py-2 w-64"
        />

        <motion.button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Sign Up
        </motion.button>
      </form>
    </div>
  );
};

export default SignUp;
