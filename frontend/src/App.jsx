import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


import LandingPage from "./pages/LandingPage";
import UserProfile from "./pages/UserProfile";
import ProtectedRoute from "./components/ProtectedRoute";
import HomePage from "./pages/HomePage";
import LayoutWithNavbar from "./components/LayoutWithNavbar";
import { AuthContext } from "./context/AuthContext";
import { useContext } from "react";
import { Navigate } from "react-router-dom";
import PublicPostPage from "./pages/PublicPostPage";
import PostingPage from "./pages/PostingPage";

function App() {
  const { user } = useContext(AuthContext);
  console.log(user)
  return (
    <Router>
      <Routes>

        <Route path="/"element={user ? <Navigate to="/home" replace /> : <LandingPage />}/>

        <Route element={<LayoutWithNavbar />}>
          {/* Routes nested in here have the Navbar */}

          <Route path="/home" element={<ProtectedRoute element={<HomePage />} />}/>
          <Route path="/profile" element={<ProtectedRoute element={<UserProfile />} />}/>

          <Route path="/post" element={<ProtectedRoute element={<PostingPage />} />}/>

          <Route path="/authors/:authorId" element={<ProtectedRoute element={<UserProfile />} />}/> # 
        </Route>

        {/* Public Routes Go Here */}
        <Route path="/authors/:authorId/posts/:postId" element={<PublicPostPage />}/>
        
        <Route path="/authors/:authorId" element={<UserProfile/>} />

      </Routes>
   </Router>

  );
}

export default App;
