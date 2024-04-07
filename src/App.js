import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';

import WaterMark from "./views/WaterMark/WaterMark";
import ImageGenerator from './views/T2I/ImageGenerator';
function App() {
  return (
      <Router>
      <div>
          <Navbar />
          <Routes>
              <Route path="/watermark" element={<WaterMark />} />
              <Route path="/image-generator" element={<ImageGenerator />} />
              //实体抽取待添加
                //default
              <Route path="/" element={<ImageGenerator />} />


          </Routes>



      </div>
      </Router>
  );
}

export default App;