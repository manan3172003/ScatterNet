/* eslint-disable react/prop-types */
const MediaComponent = ({ media }) => {
  
    const isVideo = media.type === "video";

    return (
        <div className="media-container">
            {isVideo ? (
                <video 
                    src={media.url} 
                    className="post-media video"
                    controls 
                    muted 
                    loop 
                    playsInline
                />
            ) : (
                <img 
                    src={media.url} 
                    alt="Post" 
                    className="post-media image"
                    loading="lazy"
                />
            )}
        </div>
    );
};

export default MediaComponent;
