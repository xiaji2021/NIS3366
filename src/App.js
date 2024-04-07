import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';

import WaterMark from "./views/WaterMark/WaterMark";
import ImageGenerator from './views/T2I/ImageGenerator';
import Entity from "./views/Entity/Entity";
function App() {
  return (
      <Router>
      <div>
          <Navbar />
          <Routes>
              <Route path="/watermark" element={<WaterMark />} />
              <Route path="/image-generator" element={<ImageGenerator />} />
              <Route path="/entity" element={<Entity />} />

              <Route path="/" element={<ImageGenerator />} />


          </Routes>



      </div>
      </Router>
  );
}

export default App;