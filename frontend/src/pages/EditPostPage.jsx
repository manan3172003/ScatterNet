import HeaderLogo from "../components/HeaderLogo"
import "../assets/styles/posting-page.css"
import React, {useState, useEffect} from "react";
import {fetchUserData, handleFile, apiCall,validExtensions} from "../utils/utils.js";
import {useLocation, useNavigate} from 'react-router-dom';
import Notification from "../components/Notification.jsx";
export default function EditPostPage(){

    const [base64Data, setBase64] = useState(""); 
    const [base64ContentType, setBase64ContentType] = useState(""); 
    const [fileName, setFileName] = useState("");
    const [post, setPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const location = useLocation();
    const initialData = location.state?.formData || {
        title: "",
        description: "",
        contentType: "", 
        content: "", 
        visibility: "",
    };
    const [notification, setNotification] = useState({
    show: false,
    type: "success",
    title: "",
    message: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Helper to show notifications
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

    const postId = location.state?.postId
    const [formData, setFormData] = useState(initialData)

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
            showNotification("error", "Edit Post", "Please select a valid option!")
            return;
          }

          // Prevent multiple submissions
          if (isSubmitting) {
            return;
          }

          setIsSubmitting(true);

          try {
            let content = "";
            let contentType = "";


            if (formData.contentType.includes("base64")) {
                content = base64Data; 
                contentType = base64ContentType;
                 //checks if extension is valid
                 const extension = contentType.split("/")[1].split(";")[0];
                 if (!validExtensions.includes(extension)) {  
                     contentType = 'application/base64';
                 }
            } else {
                content = formData.content;
                contentType = formData.contentType;
            }
            
              console.log(formData)
              console.log(base64Data)

            let resp = await fetchUserData();
            let AUTHOR_SERIAL = resp.user.author_id;
            let POST_URL_ID = post.serial;

            const response = await apiCall(`authors/${AUTHOR_SERIAL}/posts/${POST_URL_ID}`,
                "PUT",
                {
                    title: formData.title,
                    description: formData.description,
                    contentType: contentType || null,
                    content: content || null,
                    visibility: formData.visibility,
                }
            )

            const data = await response.json()
            console.log(data)
            if (response.ok){
                showNotification(
                    "success",
                    "Edited Post!",
                    "Redirecting to your home feed..."
                    )
                setTimeout(() => {navigate(`/home`)}, 1500);
            } else {
                console.error("Error updating post");
                showNotification("error", "Update Failed", data.message || "Something went wrong. Please try again.");
                setIsSubmitting(false);
            }
        }
        catch (error){
            showNotification("error", "Update Failed", data.message || "Something went wrong. Please try again.");
            console.log(error)
            setIsSubmitting(false);
        }
    }

  useEffect(() => {
    fetchPost();
  }, []);

  const fetchPost = async () => {
    setLoading(true);
      await fetchUserData();
      try {
          const response = await apiCall(`posts/${postId}`);
      if (!response.ok) {
        throw new Error("Failed to fetch post");
      }
      const data = await response.json();
      setPost(data);
      setFormData({
        title: data.title,
        description: data.description,
        contentType: data.contentType,
        content: ['text/plain', 'text/markdown'].includes(data.contentType) ? data.content : null,
        visibility: data.visibility,
    })
    } catch (err) {
      console.error("Error fetching authors:", err);
      showNotification("error", "Load Error", "Failed to load author");
    }
    setLoading(false);
  };

  // set large at start
  document.addEventListener('DOMContentLoaded', () => {
    const textareas = document.querySelectorAll('.post-form textarea');

    textareas.forEach(textarea => {
        if (textarea) {
          textarea.style.height = `${Math.min(textarea.scrollHeight, parseInt(getComputedStyle(textarea).maxHeight))}px`; 
        }
    });
});
//dynamic resizing
  const textareas = document.querySelectorAll('.post-form textarea');

    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = "auto";
            this.style.height = `${Math.min(this.scrollHeight, parseInt(getComputedStyle(this).maxHeight))}px`; 
        });
    });

  

  if (loading) {
    return <div>Loading author...</div>
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
                        <form className="post-form" onSubmit={handleEdit}>
                            <label className="form-title">Edit Post</label>
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
                                    
                                 <input type="file" name="content" placeholder="An optional Image" onChange={(e) => handleFile(e, setFileName, setBase64, setBase64ContentType, showNotification)} value={formData.content}/>
                                 {fileName && <p>Selected File: {fileName}</p>} 

                                </>
                            )}
                           
                            <button id= "post-button" disabled={isSubmitting}>
                              {isSubmitting ? "Updating..." : "Edit"}
                            </button>
                        </form>
                </div>
            </main>
    </div>

}
