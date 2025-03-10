import HeaderLogo from "../components/HeaderLogo"
import "../assets/styles/posting-page.css"
import React, { useState, useRef } from "react";
import {getCookie, fetchUserData} from "../utils/utils.js";
import { useLocation } from 'react-router-dom';
export default function EditPostPage(){

    const [base64Data, setBase64] = useState(""); 
    const [fileName, setFileName] = useState(""); 

   
    const previewMethodsRef = useRef();

    const location = useLocation();
    const initialData = location.state?.formData || {
        title: "",
        description: "",
        contentType: "", 
        content: "", 
        visibility: "",
    };

    ;
    const postId = location.state?.postId

    const [formData, setFormData] = useState(initialData)

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
            setBase64(base64string .split(",")[1]);
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
    
    async function handleEdit(e){
        e.preventDefault()
        // forces visibiity to be choses
        if ((e.visibility === "")||(e.contentType==="")) {
            alert("Please select a valid option!");
            return;
          }

          try {
            let content = "";

            if (formData.contentType.includes("base64")) {
                content = base64Data; 
            } else {
                content = formData.content;
            }
            
              console.log(formData)
              console.log(base64Data)

            let resp = await fetchUserData();
            let AUTHOR_SERIAL = resp.user.author_id
            let csrfToken = getCookie('csrftoken');
            let POST_URL_ID = postId

            const response = await fetch(`http://localhost:8000/api/authors/${AUTHOR_SERIAL}/posts/${POST_URL_ID}`,{
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    title: formData.title,
                    description: formData.description,
                    contentType: formData.contentType || null,
                    content: content || null,
                    visibility: formData.visibility,
                }),
                credentials: "include"
            })

            const data = await response.json()
            console.log(data)
            if (response.ok){
                alert("Edited Post!")
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


    return <div className="posting-container">
        
            <header className="posting-header">
                {<HeaderLogo/> }
            </header>
            <main className="posting-main">
                <div className="form-content" >
                        <form className="post-form" onSubmit={handleEdit}>
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
                            <select id="dropdown" name = "contentType" value={formData.contentType} required onChange={handleDropdownChange}>
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
                                    
                                 <input type="file" name="content" placeholder="An optional Image" onChange={handleFile} value={formData.content}/>
                                 {fileName && <p>Selected File: {fileName}</p>} 

                                </>
                            )}
                           
                            <button id= "post-button">Edit</button>
                        </form>
                </div>
            </main>
    </div>

}
