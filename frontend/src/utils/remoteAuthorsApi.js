import {apiCall, fetchUserData, getAuthorObject} from "./utils.js";

export async function fetchDiscoverAuthors() {
    try {
        const response = await apiCall(`authors`); // TODO: change this to authors/discover

        if (response.ok) {
            return await response.json();
        }
    }
    catch (error) {
        console.error("Error fetching remote authors:", error);
    }
}

// TODO: change this to remote authors
export async function getAuthorRelationship(otherAuthor){
    let {user: user} = await fetchUserData();
    user = await getAuthorObject(user);

    // First condition is when we pass the whole author object
    // second is when we have the otherAuthor's author id (e.g., ProfileHeader)
    if (user.id === otherAuthor.id) {
        return "Same Author";
    }

    try {
        // Check if other author is in following list of user
        const followerResponse = await apiCall(`authors/${user.serial}/following?isPending=false`);
        const followerData = await followerResponse.json();

        if (followerData.following.some(author => author.id === otherAuthor.id)) {
            return "Following";
        }

        // Check if there is a pending request to other author
        const followReqResponse = await apiCall(`authors/${user.serial}/following?isPending=true`);
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

export async function sendRemoteFollowRequest(currentAuthor, otherAuthor) {
    const requestBody = {
        "type": "follow",
        "summary": `${currentAuthor.displayName} -> ${otherAuthor.displayName}`,
        "actor": currentAuthor,
        "object": otherAuthor
    }
    try {
        const followResponse = await apiCall("authors/discover", "POST", requestBody);

        if (followResponse.ok) {
            return "Following";
        }
    }

    catch (error) {
        console.error("Error sending follow request to remote author:", error);
    }

}