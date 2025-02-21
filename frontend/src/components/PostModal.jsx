/* eslint-disable react/prop-types */
import Post from "./Post";

export default function PostModal({ post, onClose }) {
    return (
      <div
        className="modal-overlay"
        onClick={onClose}>
        <div
         
          className="modal-content"
          onClick={(e) => e.stopPropagation()}
        >
          <Post post={post} onPostClick={() => {}} />
        </div>
      </div>
    );
  }