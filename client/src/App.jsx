

import {BrowserRouter, Routes, Route} from "react-router-dom"
import Home from "./components/Home"
import Login from "./components/Login"
import Dashboard from "./components/Dashboard"
import UploadNotes from "./components/UploadNotes";
import Navbar from "./components/Navbar";
function App() {
  return (
    <div className="container">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/home" element={<Home/>} />
          <Route path="/dashboard" element={<Dashboard/>} />
          <Route path="/uploadnotes" element={<UploadNotes/>} />
          <Route path="/Navbar" element={<Navbar/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;