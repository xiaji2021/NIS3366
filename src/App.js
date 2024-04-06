import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavigationBar from './components/Navbar/NavigationBar';
import ImageGenerator from './views/T2I/ImageGenerator';
import WaterMark from "./views/WaterMark/WaterMark";
function App() {
  return (
      <Router>
      <div>
        <ImageGenerator />
      </div>
      </Router>
  );
}

export default App;