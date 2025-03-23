import {apiCall} from "./utils.js";

async function fetchAllComments(post) {
    try {
        let currUrl = `authors/${post.author.serial}/posts/${post.serial}/comments`;
        let allComments = [];
        while (currUrl) {
            const response = await apiCall(currUrl);
            if (!response.ok) break;

            const data = await response.json();
            allComments = allComments.concat(data.src || []);

            let newUrl = null;

            if (data.next) {
                const fetchedNextUrl = new URL(data.next);

                // pathname = `/api/authors/{}/posts/{}/comments`, search = `?page=2`
                newUrl = fetchedNextUrl.pathname + fetchedNextUrl.search;

                // Strip /api/ from the URL
                newUrl = newUrl.slice(5);
            }
            currUrl = newUrl;
        }
        return allComments;
    } catch (error) {
        console.error("Error fetching comments:", error);
    }
}

export {fetchAllComments};