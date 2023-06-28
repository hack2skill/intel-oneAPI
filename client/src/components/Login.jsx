import React, { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (event) => {
    event.preventDefault();

    // Perform login authentication here
    if (email && password) {
      alert(`Logging in with email: ${email}`);
      setEmail('');
      setPassword('');
    } else {
      alert('Please enter a valid email and password');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold mb-8">Login</h1>
      <form
        onSubmit={handleLogin}
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

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
