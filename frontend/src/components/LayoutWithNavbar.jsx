import Navbar from "./Navbar"; 
import { Outlet } from "react-router-dom";
import "../assets/styles/LayoutWithNavbar.css"

export default function LayoutWithNavbar() {
    return (
        <div className="layout">
            <Navbar />
            <main className="content-area">
                <Outlet />
            </main>
        </div>
    );
}
