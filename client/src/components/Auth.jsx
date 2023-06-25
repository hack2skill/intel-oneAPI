import React, { useState } from 'react';
import Login from './Login';
import SignUp from './SignUp';

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);

  const toggleAuthMode = () => {
    setIsLogin((prevMode) => !prevMode);
  };

  return (
    <div>
      {isLogin ? (
        <Login toggleAuthMode={toggleAuthMode} />
      ) : (
        <SignUp toggleAuthMode={toggleAuthMode} />
      )}
    </div>
  );
};

export default Auth;
