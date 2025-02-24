import HeaderLogo from "../components/HeaderLogo"
import "../assets/styles/posting-page.css"
import React, { useState, useRef,useEffect } from "react";
export default function PostingPage(){
    // const {login} = useContext(AuthContext)
    // const navigate = useNavigate()
    // const [activeTab,setActiveTab] = useState("login")
    const previewMethodsRef = useRef();

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        contentType: "", //markdown, plain,img
        content: "", //deets
        visibility: "",
    })
    // const [, setErrorMessage] = useState("");  
    // const [, setSuccessMessage] = useState("");
    

    function loadScript(src) {
        const script = document.createElement('script');
        script.src = src;
        script.async = true;
        document.body.appendChild(script);
      }

    function handleChange(e){
      setFormData({
        ...formData,
        [e.target.name]:e.target.value
        
      })
      console.log(formData)

    }
    
    async function handlePost(e){
        e.preventDefault()
        // forces visibiity to be choses
        if ((e.visibility === "")||(e.contentType==="")) {
            alert("Please select a valid option!");
            return;
          }
        
          console.log(formData)

        // TODO: add correct api link??
        try {
            const response = await fetch("http://localhost:8000/api/post",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    title: formData.title,
                    description: formData.description,
                    contentType: formData.contentType || null,
                    content: formData.content || null,
                    visibility: "",
                }),
                credentials: "include"
            })

            const data = await response.json()
            console.log(data)
            if (response.ok){
                alert("Uploaded Post!")
                setFormData({
                    title: "",
                    description: "",
                    contentType: "",
                    content: "",
                    visibility: "",
                })
            }

        }
        catch (error){
            alert("Something went wrong. Please try again.");
            console.log(error)
        }
    }
    useEffect(() => {
        loadScript('/markdown-editor.min.js'); // URL to the static JS file
      }, []);



    return <div className="posting-container">
        
            <header className="posting-header">
                {<HeaderLogo/> }
            </header>
            <main className="posting-main">
                <div className="form-content" >
                        <form className="post-form" onSubmit={handlePost}>
                            <label className="form-label">Create Post</label>
                            <label className="form-label">Visibility</label>
                            <select id="dropdown" name = "visibility" value={formData.visibility} required onChange={handleChange}>
                                <option value="">Select...</option>
                                <option value="PUBLIC">Public</option>
                                <option value="FRIENDS">Friends-Only</option>
                                <option value="UNLISTED">Unlisted</option>
                            </select>
                            <label className="form-label">Title</label>
                            <input type="text" name="title" placeholder="Enter a title for your post" required onChange={handleChange} value={formData.title}/>

                            <label className="form-label">Description</label>
                            <textarea name="description" placeholder="Enter the description of your post" required onChange={handleChange} value={formData.description}/>
                            
                            <label className="form-label">Content Type</label>
                            <select id="dropdown" name = "contentType" value={formData.contentType} required onChange={handleChange}>
                                <option value="">Select...</option>
                                <option value="text/markdown">Markdown</option>
                                <option value="text/plain">Plain</option>
                                {/* <option value="image/png;base64">Image (png)</option>
                                <option value="image/jpeg;base64">Image (jpeg)</option>
                                <option value="application/base64">Image </option> */}

                            </select>
                            {(formData.contentType === 'text/markdown') && (
                                <>
                                <label className="form-label">Content</label>
                            <textarea name="content" placeholder="Enter the content of your post" required onChange={handleChange} value={formData.content}/>
                            <button id= "markdown-button">Convert to Markdown</button>
                            <div id="markdown-output"></div>
                            <script src="{% static 'markdown-editor.min.js' %}"></script> 


                                </>
                            )}
                              {(formData.contentType === 'text/plain') && (
                                <>
                                <label className="form-label">Content</label>
                            <textarea name="content" placeholder="Enter the content of your post" required onChange={handleChange} value={formData.content}/>
                                </>
                            )}

                            {(formData.contentType === 'image/png;base64' ||
                                formData.contentType === 'image/jpeg;base64' ||
                                formData.contentType === 'application/base64') && (
                                <>
                                 <label className="form-label">Image</label>
                                    
                                 <input type="file" name="content" placeholder="An optional Image" onChange={handleChange} value={formData.content}/>
                            
                                </>
                            )}
                           
                            <button id= "post-button">Post</button>
                        </form>
                </div>
            </main>
    </div>

}
