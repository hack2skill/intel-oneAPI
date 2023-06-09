import React from "react";
import Driver from "./components/Driver/Driver";
import Find from "./components/Find/Find";
import Footer from "./components/Footer/Footer";
import Hero from "./components/Hero/Hero";
import Luxury from "./components/Luxury/Luxury";
import NavBar from "./components/NavBar/NavBar";

function App() {
  return (
    <div>
      <NavBar/>
      <Hero/>
      <Find/>
      <Driver/>
      <Luxury/>
      <Footer/>
    </div>
  );
}

export default App;
