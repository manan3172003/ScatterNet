const fetchUserData = async () => {
        try {
          const response = await fetch(
            "http://localhost:8000/api/authors/current-user",
            {
              method: "GET",
              credentials: "include",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": getCookie("csrftoken")
              },
            }
          );

          if (response.ok) {
            const data = await response.json();
            return data;
          }
            }
        catch (error) {
          console.error("Error fetching user data:", error);
        }
};

async function getAuthorObject(user) {
        try {
            const response = await fetch(`http://localhost:8000/api/authors/${user.author_id}`);

            if (!response.ok) {
                throw new Error(`Error fetching author: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Failed to fetch author:", error);
            return null;
        }
}

async function getAuthorObjectById(author_serial) {
        try {
            const response = await fetch(`http://localhost:8000/api/authors/${author_serial}`);

            if (!response.ok) {
                throw new Error(`Error fetching author: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Failed to fetch author:", error);
            return null;
        }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export {getCookie, fetchUserData, getAuthorObject, getAuthorObjectById}