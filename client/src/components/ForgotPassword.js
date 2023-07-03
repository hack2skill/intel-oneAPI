import React, { useRef, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Link } from "react-router-dom";

export default function ForgotPassword() {
  const emailRef = useRef();
  const { resetPassword } = useAuth();
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      setMessage("");
      setError("");
      setLoading(true);
      await resetPassword(emailRef.current.value);
      setMessage("Check your inbox for further instructions");
    } catch {
      setError("Failed to reset password");
    }

    setLoading(false);
  }

  return (
    <>
      <div className="flex items-center justify-center h-screen w-screen">
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h2 className="text-center text-2xl font-bold mb-4">Password Reset</h2>
          {error && <div className="bg-red-500 text-white text-center py-2 mb-4">{error}</div>}
          {message && <div className="bg-green-500 text-white text-center py-2 mb-4">{message}</div>}
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
            <button
              disabled={loading}
              className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded"
              type="submit"
            >
              Reset Password
            </button>
          </form>
          <div className="text-center mt-3">
            <Link to="/login" className="text-blue-500 hover:underline">
              Login
            </Link>
          </div>
          <div className="w-full text-center mt-2">
          Need an account? <Link to="/signup" className="text-blue-500 hover:underline">Sign Up</Link>
        </div>
        </div>
        
      </div>
    </>
  );
}
