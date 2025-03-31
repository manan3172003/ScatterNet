import {apiCall, fetchUserData, getAuthorObject} from "./utils.js";

export async function fetchDiscoverAuthors() {
    try {
        const response = await apiCall(`authors/discover`); // TODO: change this to authors/discover

        if (response.ok) {
            return await response.json();
        }
    }
    catch (error) {
        console.error("Error fetching remote authors:", error);
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
            return true;
        } else {
            return false;
        }
    }

    catch (error) {
        console.error("Error sending follow request to remote author:", error);
    }

}