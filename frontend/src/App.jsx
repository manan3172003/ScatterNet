import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import UserProfile from "./pages/UserProfile";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/userProfile/" element={<UserProfile />} />
      </Routes>
    </Router>
  );
}

export default App;
