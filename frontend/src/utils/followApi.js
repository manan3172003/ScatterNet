import {getCookie, fetchUserData, getAuthorObject} from "./utils.js";

export async function getAuthorRelationship(otherAuthor){
    let {user: user} = await fetchUserData();
    user = await getAuthorObject(user);

    // First condition is when we pass the whole author object
    // second is when we have the otherAuthor's author id (e.g., ProfileHeader)
    if (user.displayName === otherAuthor.displayName) {
        return "Same Author";
    }

    try {
        // Check if other author is in following list of user
        const followerResponse = await fetch(`http://localhost:8000/api/authors/${user.serial}/following?isPending=false`);
        const followerData = await followerResponse.json();

        if (followerData.following.some(author => author.id === otherAuthor.id)) {
            return "Following";
        }

        // Check if there is a pending request to other author
        const followReqResponse = await fetch(`http://localhost:8000/api/authors/${user.serial}/following?isPending=true`);
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

        const response = await fetch(`http://localhost:8000/api/authors/${otherAuthor.serial}/followers/${user.id}`, {
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

export async function getFollowRequests(user) {
    try {
        const response = await fetch(`http://localhost:8000/api/authors/${user.serial}/followers?isPending=true`)
        if (response.ok) {
            return await response.json()
        }
    }
    catch (error) {
        console.error("Error fetching follow requests", error);
        return null;
    }
}

export async function getFollowing(user) {
    try {
        const response = await fetch(`http://localhost:8000/api/authors/${user.serial}/following`)
        if (response.ok) {
            return await response.json()
        }
    }
    catch (error) {
        console.error("Error fetching following list", error);
        return null;
    }
}

export async function getFollowers(user) {
    try {
        const response = await fetch(`http://localhost:8000/api/authors/${user.serial}/followers`)
        if (response.ok) {
            return await response.json()
        }
    }
    catch (error) {
        console.error("Error fetching followers list", error);
        return null;
    }
}

export async function handleRespondingToFollowRequest(user, otherAuthor, authorResponse) {
    try {
        let method = authorResponse === "Accept" ? "PUT" : "DELETE";

        const response = await fetch(`http://localhost:8000/api/authors/${user.serial}/followers/${otherAuthor.id}`, {
            method,
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });
        if (!response.ok) {
            console.error(`Error responding to follow request (${method}):`, response.status);
        }
    }
    catch (error) {
            console.error("Error in handling follow request:", error);
            return null;
        }

}