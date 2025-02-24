import './App.css';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom"

import LandingPage from './pages/LandingPage';
import ProtectedRoute from "./components/ProtectedRoute"
import HomePage from './pages/HomePage';
import LayoutWithNavbar from './components/LayoutWithNavbar';
import { AuthContext } from './context/AuthContext';
import { useContext } from 'react';
import {Navigate} from "react-router-dom"
import PublicPostPage from './pages/PublicPostPage';
function App() {
  
  const {user} = useContext(AuthContext)
  
  return (
   <Router>
      <Routes>
        <Route
            path="/"
            element={user ? <Navigate to="/home" replace /> : <LandingPage />}
        />

        <Route element={<LayoutWithNavbar/>}>
          <Route path="/home" element={<ProtectedRoute element={<HomePage />} />} />
        </Route>
        
        <Route
            path="/authors/:authorId/posts/:postId"
            element={<PublicPostPage />}
        />
      </Routes>

   </Router>
  );
}

export default App;
