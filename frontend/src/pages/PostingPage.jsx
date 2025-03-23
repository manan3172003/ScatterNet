import HeaderLogo from "../components/HeaderLogo"
import "../assets/styles/posting-page.css"
import React, { useState } from "react";
import {fetchUserData, apiCall, handleFile} from "../utils/utils.js";
import Notification from "../components/Notification";
import {useNavigate} from "react-router-dom";
export default function PostingPage(){
    const navigate = useNavigate();
    const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
    });

    const showNotification = (type, title, message) => {
    setNotification({
      show: true,
      type,
      title,
      message,
        });
    };

    const hideNotification = () => {
        setNotification((prev) => ({ ...prev, show: false }));
    };

    const [base64Data, setBase64] = useState(""); 
    const [fileName, setFileName] = useState(""); 

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        contentType: "", //markdown, plain,img
        content: "", //deets
        visibility: "",
    })

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
            showNotification("error", "Incorrect Option Selected",
                "Please select a valid option!");
            return;
          }
        try {
            let content;

            if (formData.contentType.includes("base64")) {
                content = base64Data; 
            } else {
                content = formData.content;
            }
            
              console.log(formData)
              console.log(base64Data)

            let resp = await fetchUserData();
            let AUTHOR_SERIAL = resp.user.author_id;

            const response = await apiCall(`authors/${AUTHOR_SERIAL}/posts`,
                "POST",
                {
                    title: formData.title,
                    description: formData.description,
                    contentType: formData.contentType || null,
                    content: content || null,
                    visibility: formData.visibility,
                }
                );

            const data = await response.json()
            console.log(data)
            if (response.ok){
                showNotification("success", "Create Successful!", "Uploaded Post!");
                setFormData({
                    title: "",
                    description: "",
                    contentType: "",
                    content: "",
                    visibility: "",
                })
                setTimeout(() => {navigate(`/home`)}, 1500);
            }

        }
        catch (error){
            showNotification("error", "Post Creation Failed", "Something went wrong. Please try again.");
            console.log(error)
        }
    }

    return <div className="posting-container">
            <Notification
            show={notification.show}
            type={notification.type}
            title={notification.title}
            message={notification.message}
            onClose={hideNotification}
            />
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
                                {/* <option value="">Select...</option> */}
                                <option value="text/markdown">Markdown</option>
                                <option value="text/plain">Plain</option>
                                 <option value="image/png;base64">Image (png)</option>
                                <option value="image/jpeg;base64">Image (jpeg)</option>
                                <option value="application/base64">Image </option>

                            </select>
                              {(formData.contentType === 'text/plain'|| formData.contentType === 'text/markdown') && (
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
                                    
                                 <input type="file" name="content" placeholder="An optional Image" onChange={(e) => handleFile(e, setFileName, setBase64)} value={formData.content}/>
                                 {fileName && <p>Selected File: {fileName}</p>} 
                                </>
                            )}

                            <button id= "post-button">Post</button>
                        </form>
                </div>
            </main>
    </div>

}
