/*
notification on edit and create post needs to be fixed
*/
import HeaderLogo from "../components/HeaderLogo"
import "../assets/styles/posting-page.css"
import React, { useState, useRef,useEffect } from "react";
import {getCookie, fetchUserData} from "../utils/utils.js";
import Notification from "../components/Notification.jsx";
import {useLocation, useNavigate} from 'react-router-dom';


export default function PostingPage(){
   
    const previewMethodsRef = useRef();
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


    async function handleFile(e) {
        const selectedFile = e.target.files[0];

    
        if (!selectedFile) {
            console.error("No file selected!");
            return;
        }
        console.log('File being processed:', selectedFile);
    
        try {
            setFileName(selectedFile.name);
            const base64string = await convertToBase64(selectedFile);
            console.log('Base64 String before strip: ', base64string);
            const [contentTypeWithPrefix, base64DataString] = base64string.split(','); //splits string to data:datatype and the base64 string
            const base64ContentType = contentTypeWithPrefix.replace("data:", "");// strip data
            
            setBase64(base64DataString); 
            setBase64ContentType(base64ContentType); 
            
            console.log('Base64 Content Type:', base64ContentType);
            console.log('Base64 Data:', base64DataString);
            console.log('Base64 String: ', base64string);
    
        } catch (error) {
            console.error('Error converting file to Base64: ', error);
        }
    }

    function convertToBase64(selectedFile) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            console.log('File being processed:', selectedFile);
            console.log('Reader result at load:', reader.result);
    
            reader.onload = function() {
                console.log('called: ', reader);
                resolve(reader.result); 
            };
    
            reader.onerror = function(error) {
                reject(error); 
            };
    
            reader.readAsDataURL(selectedFile);
        });
    }

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
            alert("Please select a valid option!");
            return;
          }
        try {
            let content = "";
            let contentType = "";

            if (formData.contentType.includes("base64")) {
                content = base64Data; 
                contentType = base64ContentType;
            } else {
                content = formData.content;
                contentType = formData.contentType;
            }
            
              console.log(formData)
              console.log(base64Data)

            let resp = await fetchUserData();
            let AUTHOR_SERIAL = resp.user.author_id
            let csrfToken = getCookie('csrftoken');

            const response = await fetch(`http://localhost:8000/api/authors/${AUTHOR_SERIAL}/posts`,{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    title: formData.title,
                    description: formData.description,
                    contentType: contentType || null,
                    content: content || null,
                    visibility: formData.visibility,
                }),
                credentials: "include"
            })

            const data = await response.json()
            console.log(data)
            if (response.ok){
                showNotification(
                    "Success",
                    "Created Post!",
                    "Redirecting to your home feed..."
                    )
                setTimeout(() => {navigate(`/home`)}, 1500);
            }

        }
        catch (error){
            alert("Something went wrong. Please try again.");
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
                                <option value="PUBLIC">Public</option>
                                <option value="FRIENDS">Friends-Only</option>
                                <option value="UNLISTED">Unlisted</option>
                            </select>
                            <label className="form-label">Title</label>
                            <input type="text" name="title" placeholder="Enter a title for your post" required onChange={handleChange} value={formData.title}/>

                            <label className="form-label">Description</label>
                            <textarea name="description" placeholder="Enter the description of your post" required onChange={handleChange} value={formData.description}/>
                            
                            <label className="form-label">Content Type</label>
                            <select id="dropdown" name = "contentType" value={formData.contentType} required onChange={handleDropdownChange}>
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

                            {(formData.contentType === 'image/png;base64' ||
                                formData.contentType === 'image/jpeg;base64' ||
                                formData.contentType === 'application/base64') && (
                                <>
                                 <label className="form-label">Image</label>
                                    
                                 <input type="file" name="content" placeholder="An optional Image" onChange={handleFile} value={formData.content}/>
                                 {fileName && <p>Selected File: {fileName}</p>} 
                                </>
                            )}
                           
                            <button id= "post-button">Post</button>
                        </form>
                </div>
            </main>
    </div>

}
