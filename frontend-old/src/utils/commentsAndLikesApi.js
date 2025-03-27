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

async function fetchAllLikes(post) {
    try {
        let currUrl = `authors/${post.author.serial}/posts/${post.serial}/likes`;
        let allLikes = [];
        while (currUrl) {
            const response = await apiCall(currUrl);
            if (!response.ok) break;

            const data = await response.json();
            allLikes = allLikes.concat(data.src || []);

            let newUrl = null;

            if (data.next) {
                const fetchedNextUrl = new URL(data.next);

                // pathname = `/api/authors/{}/posts/{}/likes`, search = `?page=2`
                newUrl = fetchedNextUrl.pathname + fetchedNextUrl.search;

                // Strip /api/ from the URL
                newUrl = newUrl.slice(5);
            }
            currUrl = newUrl;
        }
        return allLikes;
    } catch (error) {
        console.error("Error fetching likes:", error);
    }
}

export {fetchAllComments, fetchAllLikes};