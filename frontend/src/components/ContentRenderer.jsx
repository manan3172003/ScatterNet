/* This component is used to render the various content types of the Posts component*/
import { useState } from "react"
import ReactMarkdown from "react-markdown"


// eslint-disable-next-line react/prop-types
export default function ContentRenderer({contentType, content}) {
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
            return <p className="image-error">An error occured will loading the image.</p>
        }
        let imgMimeType;
        if (contentType === "application/base64"){
            // As specified by course website a image without a explicit type so we need to try and render it as a image.

            imgMimeType = "image"
        } else {
            imgMimeType = contentType
        }
        return (
            <img
                src={`data:${imgMimeType};base64,${content}`}
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