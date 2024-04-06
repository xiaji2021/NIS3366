import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
<<<<<<< HEAD
import NavigationBar from './components/Navbar/NavigationBar';
=======
import Navbar from './components/Navbar/Navbar';


>>>>>>> 6aaedb54e9b16c366e778a5bd8ade1ae09811bcf
import ImageGenerator from './views/T2I/ImageGenerator';
// import WaterMark from "./views/WaterMark/WaterMark";
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