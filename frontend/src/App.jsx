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
import EditPostPage from "./pages/EditPostPage.jsx";
import ProfileRedirect from "./components/ProfileRedirect";
import AdminProtectedRoute from "./components/AdminProtectedRoute.jsx";
import AdminPage from "./pages/AdminPage.jsx";
import AuthorsList from "./components/AuthorsList.jsx";
import EditProfilePage from "./pages/EditProfilePage";
import DiscoverPage from "./pages/DiscoverPage.jsx";
import StreamPage from "./pages/StreamPage.jsx";
import ConnectNode from "./pages/ConnectNodes.jsx"

function App() {
  const { user } = useContext(AuthContext);
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
          <Route path="/editPost" element={<ProtectedRoute element={<EditPostPage />} />}/>
          <Route path="/profile" element={<ProtectedRoute element={<ProfileRedirect />} />}/>
          <Route path="/post" element={<ProtectedRoute element={<PostingPage />} />}/>
          <Route path="/editProfile" element={<ProtectedRoute element={<EditProfilePage />} />}/>
          <Route path="/requests" element={<ProtectedRoute element={<AuthorsList chosenMode="Requests" />} />}/>
          <Route path="/discover" element={<ProtectedRoute element={<DiscoverPage />} />}/>
          <Route path="/reels" element={<ProtectedRoute element={<StreamPage />} />}/>
          <Route path="/authors/:authorId" element={<UserProfile/>} />
          <Route path="/authors/:authorId/followers" element={<ProtectedRoute element={<AuthorsList chosenMode="Followers" />} />}/>
          <Route path="/authors/:authorId/following" element={<ProtectedRoute element={<AuthorsList chosenMode="Following" />} />}/>
          <Route path="/authors/:authorId/posts/:postId" element={<PublicPostPage />}/>
          
          {/* Admin Routes only accessible to admins */}
          <Route
            path="/admin"
            element={<AdminProtectedRoute element={<AdminPage />} />}
          />
          <Route
            path="/connectnodes"
            element={<AdminProtectedRoute element={<ConnectNode />} />}
          />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
