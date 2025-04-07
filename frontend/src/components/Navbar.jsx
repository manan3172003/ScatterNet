
import { Home, User, SquarePlus, Shield, Video } from "lucide-react";
import { AiOutlineNotification, AiOutlineSearch } from "react-icons/ai";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router";
import "../assets/styles/navbar.css";
import {getCookie} from "../utils/utils.js";

export default function Navbar() {
  const [onMobile, setOnMobile] = useState(window.innerWidth < 768);

  const isAdminFromCookie = getCookie("isAdmin") === "true";
  const navItems = [
    { icon: Home, label: "Home", path: "/home" },
    { icon: SquarePlus, label: "Post", path: "/post" },
    { icon: User, label: "Profile", path: "/profile" },
    { icon: Video, label: "Reels", path: "/reels" },
    { icon: AiOutlineNotification, label: "Requests", path: "/requests "},
    { icon: AiOutlineSearch, label: "Discover", path: "/discover "},
    ...(isAdminFromCookie ? [{ icon: Shield, label: "Admin", path: "/admin" }] : []),
  ];
  // hook that runs when component is mounted
  useEffect(() => {
    const handleResize = () => setOnMobile(window.innerWidth < 768);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  // https://motion.dev/docs/react-motion-component
  return (
    /*initial defines state before animation starts 
        animate is the state and transition */
    <motion.nav
      className={`navbar ${onMobile ? "mobile" : "desktop"}`}
      initial={{ opacity: 0, x: onMobile ? 0 : -50, y: onMobile ? 50 : 0 }}
      animate={{ opacity: 1, x: 0, y: 0 }} // Layout position so 0
      transition={{ duration: 0.7 }}
    >
      <ul className={`nav-list ${onMobile ? "mobile" : "desktop"}`}>
        {navItems.map((item, index) => (
          <li key={index}>
            <Link to={item.path} className="nav-item">
              <item.icon size={24} />
              <span className="nav-label">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>
    </motion.nav>
  );
}
