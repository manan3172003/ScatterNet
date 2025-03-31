import {useEffect, useState} from "react";
import {fetchDiscoverAuthors} from "../utils/authorsApi.js";
import AuthorCard from "../components/AuthorCard.jsx";
import "../assets/styles/discover-page.css";

export default function DiscoverPage() {
    const [authors, setAuthors] = useState([]);

    useEffect(() =>  {
        fetchAuthors();
    }, [])

    async function fetchAuthors() {
        const fetchedAuthors = await fetchDiscoverAuthors();
        setAuthors(fetchedAuthors.authors); // TODO: remove .authors since we're only doing that for local testing
    }

    return (
        <div className="discover-container">
            <h2 className="discover-header">Discover</h2>
            <div className="discover-author-grid">
                {authors.length > 0 && authors.map((author) => (
                    <AuthorCard key={author.id} author={author}></AuthorCard>
                ))}
            </div>
        </div>
    )
}