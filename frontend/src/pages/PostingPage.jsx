/*
notification on edit and create post needs to be fixed
*/
import HeaderLogo from "../components/HeaderLogo"
import "../assets/styles/posting-page.css"
import React, { useState } from "react";
import Notification from "../components/Notification.jsx";
import {useNavigate} from 'react-router-dom';
import {fetchUserData, apiCall,handleFile,validExtensions} from "../utils/utils.js";

export default function PostingPage(){

    const [base64Data, setBase64] = useState(""); 
    const [base64ContentType, setBase64ContentType] = useState(""); 
    const [fileName, setFileName] = useState(""); 
    const navigate = useNavigate(); 

     const [notification, setNotification] = useState({
        show: false,
        type: "success",
        title: "",
        message: "",
      });

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        contentType: "text/markdown", //markdown, plain,img
        content: "", //deets
        visibility: "PUBLIC",
    })

    const showNotification = (type, title, message) => {
        setNotification({
          show: true,
          type,
          title,
          message,
        });
      };

      // Helper to hide notifications
  const hideNotification = () => {
    setNotification((prev) => ({ ...prev, show: false }));
  };

    function handleChange(e){
      setFormData({
        ...formData,
        [e.target.name]:e.target.value
        
      })
      console.log(formData)

    }

    function handleDropdownChange(e){
        setFormData({
          ...formData,
          [e.target.name]:e.target.value,
          content:""
          
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
            let content = "";
            let contentType = "";

            if (formData.contentType.includes("base64")) {//file input
                content = base64Data; 
                contentType = base64ContentType;
                //checks if extension is valid
                const extension = contentType.split("/")[1].split(";")[0];
                if (!validExtensions.includes(extension)) {  
                    contentType = 'application/base64';
                }
            } else {//text
                content = formData.content;
                contentType = formData.contentType;
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
                    contentType: contentType || null,
                    content: content || null,
                    visibility: formData.visibility,
                }
                );

            const data = await response.json()
            console.log(data)
            if (response.ok){
                showNotification(
                    "success",
                    "Created Post!",
                    "Redirecting to your home feed..."
                    )
                setTimeout(() => {navigate(`/home`)}, 1500);
            }else{
                console.error("Error creating post");
                showNotification("error", "Update Failed", data.message || "Something went wrong. Please try again.");
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
                 <header className="header">{<HeaderLogo />}</header>
            <main className="posting-main">
                <div className="form-content" >
                        <form className="post-form" onSubmit={handlePost}>
                            <label className="form-label">Create Post</label>
                            <label className="form-label">Visibility</label>
                            <select className="dropdown" name = "visibility" value={formData.visibility} required onChange={handleChange}>
                                <option value="PUBLIC">Public</option>
                                <option value="FRIENDS">Friends-Only</option>
                                <option value="UNLISTED">Unlisted</option>
                            </select>
                            <label className="form-label">Title</label>
                            <input type="text" name="title" placeholder="Enter a title for your post" required onChange={handleChange} value={formData.title}/>

                            <label className="form-label">Description</label>
                            <textarea name="description" placeholder="Enter the description of your post" required onChange={handleChange} value={formData.description}/>
                            
                            <label className="form-label">Content Type</label>
                            <select className="dropdown" name = "contentType" value={formData.contentType} required onChange={handleDropdownChange}>
                                {/* <option value="">Select...</option> */}
                                <option value="text/markdown">Markdown</option>
                                <option value="text/plain">Plain</option>
                                <option value="application/base64">Image </option> 

                            </select>
                              {(formData.contentType === 'text/plain'|| formData.contentType === 'text/markdown') && (
                                <>
                                <label className="form-label">Content</label>
                            <textarea name="content" placeholder="Enter the content of your post" required onChange={handleChange} value={formData.content}/>
                                </>
                            )}

                            {(formData.contentType === 'application/base64') && (
                                <>
                                 <label className="form-label">Image</label>
                                    
                                 <input type="file" name="content" placeholder="An optional Image" onChange={(e) => handleFile(e, setFileName, setBase64,setBase64ContentType)} value={formData.content} accept="image/*"/>
                                 {fileName && <p>Selected File: {fileName}</p>} 
                                </>
                            )}

                            <button id= "post-button">Post</button>
                        </form>
                </div>
            </main>
    </div>

}
