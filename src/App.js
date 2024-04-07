import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';

import ImageUploader from "./views/WaterMark/WaterMark";

import ImageGenerator from './views/T2I/ImageGenerator';
import imageGenerator from "./views/T2I/ImageGenerator";
// import WaterMark from "./views/WaterMark/WaterMark";
function App() {
  return (
      <Router>
      <div>
          <Navbar />
        {/*<ImageGenerator />*/}
          <ImageUploader />

      </div>
      </Router>
  );
}

export default App;