import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
// import T2I from './views/T2I/T2I';
// import T2I_left from './views/T2I/T2I_left';
import ImageGenerator from './views/T2I/ImageGenerator';
// import WaterMark from "./views/WaterMark/WaterMark";
function App() {
  return (
      <Router>
        <Navbar />
        <ImageGenerator/>
      </Router>
  );
}

export default App;