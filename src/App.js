import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
<<<<<<< HEAD
import ImageGenerator from './views/T2I/ImageGenerator';
import WaterMark from "./views/WaterMark/WaterMark";
=======

import WaterMark from "./views/WaterMark/WaterMark";
import ImageGenerator from './views/T2I/ImageGenerator';
>>>>>>> 15f938e283bf9c2736c1b10510f9f3486d738d43
function App() {
  return (
      <Router>
      <div>
<<<<<<< HEAD
        <Navbar />
        {<ImageGenerator />}
        {<WaterMark/> }
=======
          <Navbar />
          <Routes>
              <Route path="/watermark" element={<WaterMark />} />
              <Route path="/image-generator" element={<ImageGenerator />} />
              //实体抽取待添加
                //default
              <Route path="/" element={<ImageGenerator />} />


          </Routes>



>>>>>>> 15f938e283bf9c2736c1b10510f9f3486d738d43
      </div>
      </Router>
  );
}
export default App;