import {Home, User, Bell, SquarePlus} from "lucide-react"
import { useState,useEffect } from "react"
import {motion} from "framer-motion"
import { Link } from "react-router";
const navItems = [
    {icon: Home, label: "Home", path:"/home"},
    {icon: User, label: "Profile", path:"/profile"},
    {icon: Bell, label: "Notifications",path:"/messages"},
    {icon: SquarePlus, label: "Post",path:"/post"}
]

export default function Navbar(){
    const [onMobile,setOnMobile] = useState(window.innerWidth < 768)
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
        className={`navbar ${onMobile ? "mobile": "desktop"}`}
        initial={{ opacity: 0, x: onMobile ? 0 : -50, y: onMobile ? 50 : 0 }}
        animate={{ opacity: 1, x: 0, y: 0 }} // Layout position so 0
        transition={{ duration: 0.4 }}
        >   
        
            <ul className={`nav-list ${onMobile ? "mobile" : "desktop"}`}>
                {navItems.map((item, index) => {
                    <li key={index}>
                        <Link to={item.path} className="nav-bar-item">
                            <item.icon size={24}/>
                            <span className="nav-label">{item.label}</span>
                        </Link>
                    </li>

                })}


            </ul>




        </motion.nav>
    )

}