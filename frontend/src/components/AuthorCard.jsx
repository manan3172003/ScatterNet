import "../assets/styles/author-card.css";

export default function AuthorCard({ author }) {

    return (
        <div className="author-card">
            <img
                className="author-image"
                src={author.profileImage}
                alt={`${author.displayName}'s profile`}
            />
            <h3 className="author-name">{author.displayName}</h3>
            <p className="author-host">{author.host}</p>
            <button className="follow-button">Follow</button>
        </div>
    )
}
