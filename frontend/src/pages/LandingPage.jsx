
import HeaderLogo from "../components/HeaderLogo"
import {useState} from "react"

import "../assets/styles/landing-page.css"

export default function LandingPage(){
    const [activeTab,setActiveTab] = useState("login")
    const [formData, setFormData] = useState({
        github: "",
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        profilePicture: null, 
        displayname:""
    })
    function handleChange(e){
      setFormData({
        ...formData,
        [e.target.name]:e.target.value
      })
      console.log(formData)

    }
    function handleSubmit(e){
      e.preventDefault()
      if (activeTab == "login"){
        submitLogin()
      }



    }

    function submitLogin(){



    }

    return <div className="landing-container">
            <header className="landing-header">
                <HeaderLogo/>
            </header>
            <main className="landing-main">
                <div className="tab-switch">
                    <button className={activeTab === "login" ? "active" : ""}
                    onClick={() => setActiveTab("login")}>
                    Login
                    </button>
                    <button
                    className={activeTab === "signup" ? "active" : ""}
                    onClick={() => setActiveTab("signup")}
                    >
                        Sign Up
                    </button>
                </div>
                <div className="form-content">
                    {activeTab === "login" ? (
                        <form className="auth-form">
                          <label className="form-label">Username</label>
                          <input type="text" name="username" placeholder="Enter your username" required onChange={handleChange} value={formData.username}/>
                          <label className="form-label">Password</label>
                          <input type="password" name="password" placeholder="Enter your password" required onChange={handleChange} value={formData.password}/>
                         
                         <button type="submit" onSubmit={handleSubmit}>Log In</button>
                        </form>
                        ) : (
                        <form>

                        </form>
                    )}
                </div>
            </main>
    </div>

}
