async function apiCall(
    endpoint: string,
    httpmethod: string = "GET",
    body: Record<string, any> | null = null
): Promise<Response> {
    return await fetch(
        `/api/${endpoint}`,
        {
            method: httpmethod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken') || ''
            },
            body: (body !== null) ? JSON.stringify(body) : undefined,
            credentials: "include"
        }
    );
}

function getCookie(name: string): string | null {
  let cookieValue: string | null = null;
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

export { apiCall, getCookie };