
import HeaderLogo from "../components/HeaderLogo"
import {useContext, useState} from "react"
import { AuthContext } from "../context/AuthContext"
import "../assets/styles/landing-page.css"
import {useNavigate } from "react-router-dom"
import Notification from "../components/Notification"
export default function LandingPage(){
    const {login} = useContext(AuthContext)
    const navigate = useNavigate()
    const [activeTab,setActiveTab] = useState("login")
    const [formData, setFormData] = useState({
        github: "",
        username: "",
        password: "",
        confirmPassword: "",
        profileImageURL: null, 
        displayName:""
    })    
    // State for keeping track of notifications
    const [notification, setNotification] = useState({
        show: false,
        type: "success",
        title: "",
        message: "",
    })

    // Helper function that is used to show notifications
    const showNotification = (type, title, message) => {
        setNotification({
        show: true,
        type,
        title,
        message,
        })
    }

    // Helper function that is used to hide notifications
    const hideNotification = () => {
        setNotification((prev) => ({ ...prev, show: false }))
    }

    function handleChange(e){
      setFormData({
        ...formData,
        [e.target.name]:e.target.value
      })
      

    }
    async function handleSignUp(e){
        e.preventDefault()
        
        if (formData.password !== formData.confirmPassword){
            
            showNotification(
                "error",
                "Password Error",
                "Passwords do not match!"
              )
            return
        }

        try {
            const response = await fetch("http://localhost:8000/api/authors/signup",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: formData.username,
                    password: formData.password,
                    github: formData.github || null,
                    displayName: formData.displayName,
                    profileImageURL: formData.profileImageURL || null,
                }),
                credentials: "include"
            })

            const data = await response.json()
            
            if (response.ok){
                showNotification("warning", "Account Created", "Your account has been created! Please wait to be approved by the node admin.")
                setFormData({
                    github: "",
                    username: "",
                    email: "",
                    password: "",
                    confirmPassword: "",
                    profileImageURL: null,
                    displayName: "",
                })
            } else if (response.status === 400 && data.username) {
                showNotification(
                  "error",
                  "Username Taken",
                  "An author with this username already exists. Please log in or pick a different username."
                )
            } else {
                showNotification("error", "Sign Up Failed", data.message || "Something went wrong. Please try again.")
            }

        }
        catch (error){
            showNotification("error", "Sign Up Failed", error || "Something went wrong. Please try again.")
            
        }


    }


    async function handleSubmit(e){
      e.preventDefault()
      if (activeTab == "login"){
        
        let response = await login(formData.username, formData.password)

        if (!response.success) {
            if (response.status === "401") {
                showNotification(
                    "error",
                    "Login Failed",
                    "Incorrect username or password."
                  )
            } else {
                showNotification(
                    "error",
                    "Login Error",
                    "An error occurred. Please try again."
                  )
            }
        } else {
            showNotification(
                "success",
                "Login Successful",
                "Redirecting to your dashboard..."
            )
            setTimeout(() => {navigate("/home")}, 1500) 
        }
      }
      else {
        handleSignUp(e)
      }



    }
    
    

    return <div className="landing-container">
            <header className="landing-header">
                <HeaderLogo/>
            </header>
            <Notification
                show={notification.show}
                type={notification.type}
                title={notification.title}
                message={notification.message}
                onClose={hideNotification}
            />
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
                <div className="form-content" >
                    {activeTab === "login" ? (
                        <form className="auth-form" onSubmit={handleSubmit}>
                          <label className="form-label">Username</label>
                          <input type="text" name="username" placeholder="Enter your username" required onChange={handleChange} value={formData.username}/>
                          <label className="form-label">Password</label>
                          <input type="password" name="password" placeholder="Enter your password" required onChange={handleChange} value={formData.password}/>
                         
                         <button>Log In</button>
                        </form>
                        ) : (
                        <form className="auth-form" onSubmit={handleSubmit}>
                            <label className="form-label">Username</label>
                            <input type="text" name="username" placeholder="Enter a desired username" required onChange={handleChange} value={formData.username}/>

                            <label className="form-label">Display Name</label>
                            <input type="text" name="displayName" placeholder="Enter a desired display name" required onChange={handleChange} value={formData.displayName}/>

                            <label className="form-label">Github Url</label>
                            <input type="url" name="github" placeholder="A link to your Github Profile" onChange={handleChange} value={formData.github}/>

                            <label className="form-label">Profile Image Url</label>
                            <input type="url" name="profileImageURL" placeholder="A link to your Profile picture" onChange={handleChange} value={formData.profileImageURL}/>
                            
                            <label className="form-label">Password</label>
                            <input type="password" name="password" required onChange={handleChange} value={formData.password}/>

                            <label className="form-label">Confirm Password</label>
                            <input type="password" name="confirmPassword" required onChange={handleChange} value={formData.confirmPassword}/>
                            
                            <button>Sign Up</button>
                        </form>
                    )}
                </div>
            </main>
    </div>

}
