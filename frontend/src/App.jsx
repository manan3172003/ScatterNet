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
import AdminProtectedRoute from "./components/AdminProtectedRoute.jsx";
import AdminPage from "./pages/AdminPage.jsx";
import ProfileRedirect from "./components/ProfileRedirect";

function App() {
  const { user } = useContext(AuthContext);
  console.log(user);
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={user ? <Navigate to="/home" replace /> : <LandingPage />}
        />

        <Route element={<LayoutWithNavbar />}>
          {/* Routes nested in here have the Navbar */}

          <Route path="/home" element={<ProtectedRoute element={<HomePage />} />}/>
          <Route
            path="/profile"
            element={<ProtectedRoute element={<ProfileRedirect />} />}
            user={user}
          />

          <Route path="/post" element={<ProtectedRoute element={<PostingPage />} />}/>

            {/* Admin Routes only accessible to admins */}
          <Route path="/admin" element={<AdminProtectedRoute element={<AdminPage />} />} />

          <Route path="/authors/:authorId" element={<UserProfile/>} />
        </Route>

        {/* Public Routes Go Here */}
        <Route path="/authors/:authorId/posts/:postId" element={<PublicPostPage />}/>

      </Routes>
    </Router>
  );
}

export default App;
