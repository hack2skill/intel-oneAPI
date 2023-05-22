

import {BrowserRouter, Routes, Route} from "react-router-dom"
import Home from "./components/Home"
import Login from "./components/Login"
import Dashboard from "./components/Dashboard"
function App() {
  return (
    <div className="container">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/home" element={<Home/>} />
          <Route path="/dashboard" element={<Dashboard/>} />
          
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;