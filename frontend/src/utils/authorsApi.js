import {apiCall} from "./utils.js";

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