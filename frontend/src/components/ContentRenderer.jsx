/* This component is used to render the various content types of the Posts component*/
import { useState } from "react"
import ReactMarkdown from "react-markdown"


// eslint-disable-next-line react/prop-types
export default function ContentRenderer({contentType, content, postHostname, postId}) {
    const [imageError,setImageError] = useState(false) // State that simply keeps track of whether or not we ran into a issue rendering the image.

    const handleImageError = () => {
        setImageError(true)
    }


    
    const isImageContent = (contentType) => {
        // eslint-disable-next-line react/prop-types
        return contentType.includes("image/") || contentType === "application/base64"
    }
    
    if (isImageContent(contentType)){
        if (imageError){
            return <p className="image-error">An error occurred while loading the image.</p>
        }
        const imageEndpoint = `${postId}/image`;
        return (
            <img
                src={imageEndpoint}
                className="post-image"
                onError={handleImageError}
            />
        )
    } else if (contentType === "text/plain") {
        return <p className="plain-text">{content}</p>
    } else if (contentType === "text/markdown"){
        return <ReactMarkdown className="markdown">{content}</ReactMarkdown>
    } else {
        return <p className="unsupported-content">Unsupported content type: {contentType}</p>
    }

}