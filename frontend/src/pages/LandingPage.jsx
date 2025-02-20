
import HeaderLogo from "../components/HeaderLogo"
import {useContext, useState} from "react"
import { AuthContext } from "../context/AuthContext";
import "../assets/styles/landing-page.css"


export default function LandingPage(){
    const {login} = useContext(AuthContext)
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
    const [, setErrorMessage] = useState("");  
    const [, setSuccessMessage] = useState("");
    

    function handleChange(e){
      setFormData({
        ...formData,
        [e.target.name]:e.target.value
      })
      console.log(formData)

    }
    async function handleSignUp(e){
        e.preventDefault()
        
        if (formData.password !== formData.confirmPassword){
            alert("Passwords do not match!")
            // To Do: Will replace later on to be better looking
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/authors/api/signup",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                    github: formData.github || null,
                    displayname: formData.displayname,
                    profilePicture: formData.profilePicture || null,
                })
            })

            const data = await response.json()
            console.log(data)
            if (response.ok){
                alert("Your account has been created! Please wait for approval by the node admin.")
                setFormData({
                    github: "",
                    username: "",
                    email: "",
                    password: "",
                    confirmPassword: "",
                    profilePicture: null,
                    displayname: "",
                })
            }

        }
        catch (error){
            alert("Something went wrong. Please try again.");
            console.log(error)
        }


    }


    async function handleSubmit(e){
      e.preventDefault()
      if (activeTab == "login"){
        const response = await login(formData.username, formData.password);

        if (!response.success) {
            if (response.status === "401") {
                setErrorMessage("Incorrect username or password.");
            } else {
                setErrorMessage("An error occurred. Please try again.");
            }
        } else {
            setSuccessMessage("Login successful! Redirecting...");
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
                            <input type="text" name="displayname" placeholder="Enter a desired display name" required onChange={handleChange} value={formData.displayname}/>

                            <label className="form-label">Github Url</label>
                            <input type="url" name="github" placeholder="A link to your Github Profile" required onChange={handleChange} value={formData.github}/>

                            <label className="form-label">Profile Image Url</label>
                            <input type="url" name="profilePicture" placeholder="A link to your Profile picture" required onChange={handleChange} value={formData.profilePicture}/>
                            
                            <label className="form-label">Password</label>
                            <input type="password" name="password" required onChange={handleChange} value={formData.password}/>

                            <label className="form-label">Confirm Password</label>
                            <input type="password" name="password" required onChange={handleChange} value={formData.con}/>
                            
                            <button>Sign Up</button>
                        </form>
                    )}
                </div>
            </main>
    </div>

}
