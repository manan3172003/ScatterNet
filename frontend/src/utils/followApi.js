 import {getCookie, fetchUserData, getAuthorObject} from "./utils.js";

export async function getAuthorRelationship(otherAuthor){
    let {user: user} = await fetchUserData();

    // TODO: In the profile header, we are only passed the author id, so we need to get the author object
    if (typeof otherAuthor !== "object") {
        // Since getAuthorObject expects an object with a field of author_id, just make the author id into an object
        otherAuthor = {author_id: otherAuthor};
        otherAuthor = await getAuthorObject(otherAuthor);
    }

    // First condition is when we pass the whole author object
    // second is when we have the otherAuthor's author id (e.g., ProfileHeader)
    if (user.displayName === otherAuthor.displayName || user.author_id.toString() === otherAuthor.id) {
        return "Same Author";
    }

    try {
        // Check if other author is in following list of user
        const followerResponse = await fetch(`http://localhost:8000/api/authors/${user.author_id}/following?isPending=false`);
        const followerData = await followerResponse.json();

        if (followerData.following.some(author => author.id === otherAuthor.id)) {
            return "Following";
        }

        // Check if there is a pending request to other author
        const followReqResponse = await fetch(`http://localhost:8000/api/authors/${user.author_id}/following?isPending=true`);
        const followReqData = await followReqResponse.json();

        if (followReqData.following.some(author => author.id === otherAuthor.id)) {
            return "Requested";
        }

        return "Not Following";
    }
    catch (error) {
        console.error("Error checking follow status:", error);
        return false;
    }
}

// WE DONT HAVE A WAY TO CANCEL FOLLOW REQS, not in spec either
export async function handleFollowRequest(user, otherAuthor, authorsRelationship) {
    try {
        let newRelationship = authorsRelationship;
        let method = authorsRelationship === "Following" ? "DELETE" : "PUT";

        const response = await fetch(`http://localhost:8000/api/authors/${otherAuthor}/followers/${user.id}`, {
            method,
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });

        if (response.ok) {
            newRelationship = authorsRelationship === "Following" ? "Not Following" : "Requested";
        }
        else {
            console.error(`Error updating follow status (${method}):`, response.status);
        }

        return newRelationship; // Return the updated state

        }
        catch (error) {
            console.error("Error in handleFollow:", error);
            return null;
        }
}