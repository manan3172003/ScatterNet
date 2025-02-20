import './App.css';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom"

import LandingPage from './pages/LandingPage';
import ProtectedRoute from "./components/ProtectedRoute"
import HomePage from './pages/HomePage';
import LayoutWithNavbar from './components/LayoutWithNavbar';



function App() {
  return (
   <Router>
      <Routes>
        <Route path="/" element={<LandingPage/>}/>

        <Route element={<LayoutWithNavbar/>}>
          <Route path="/home" element={<ProtectedRoute element={<HomePage />} />} />
        </Route>
        
           
      </Routes>

   </Router>
  );
}

export default App;
