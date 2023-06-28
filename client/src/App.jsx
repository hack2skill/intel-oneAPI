import {BrowserRouter, Routes, Route} from "react-router-dom"
import Home from "./components/Home"
import Dashboard from "./components/Dashboard"
import Navbar from "./components/Navbar";
import Landingpage from "./components/Landingpage";
import About from "./components/About";
import Team from "./components/Team";
import Studyplanner from "./components/Studyplanner";
import Features from "./components/Features";
import Uploadnote from "./components/Uploadnote";
import Anythingmore from "./components/Anythingmore";
import Uploadn from "./components/Uploadn";
import Aibot from "./components/Aibot";
import Uploadp from "./components/Uploadp";
import Uploads from "./components/Uploads";
import Sortedpyq from "./components/Sortedpyq";
import Generalpyq from "./components/Generalpyq";
import Repetitivepyq from "./components/Repetitivepyq";
import Auth from "./components/Auth";
import Wait from "./components/Wait";

function App() {
  return (
    <div className="container">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landingpage/>} />
          <Route path="/home" element={<Home/>} />
          <Route path="/dashboard" element={<Dashboard/>} />         
          <Route path="/Navbar" element={<Navbar/>} />
           
          <Route path="/landing" element={<Landingpage/>} />
          <Route path="/about" element={<About/>} />
          <Route path="/team" element={<Team/>} />
          <Route path="/studyplanner" element={<Studyplanner/>} />
          <Route path="/features" element={<Features/>} />
          <Route path="/login" element={<Auth />} />
        
          <Route path="/uploadnote" element={<Uploadnote/>} />         
          <Route path="/anythingmore" element={<Anythingmore/>} />
          <Route path="/uploadn" element={<Uploadn/>} />
          <Route path="/uploadp" element={<Uploadp/>} />
          <Route path="/uploads" element={<Uploads/>} />

          <Route path="/aibot" element={<Aibot/>} />
          <Route path="/sortedpyq" element={<Sortedpyq/>} />
          <Route path="/generalpyq" element={<Generalpyq/>} />
          <Route path="/repetitivepyq" element={<Repetitivepyq/>} />
          <Route path="/signup" element={<Auth />} />
          <Route path="/wait" element={<Wait />} />

        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;