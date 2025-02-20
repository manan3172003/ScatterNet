import Navbar from "./Navbar"; 
import { Outlet } from "react-router-dom";

export default function LayoutWithNavbar() {
    return (
        <div>
            <Navbar />  
            <Outlet />   
        </div>
    );
}
