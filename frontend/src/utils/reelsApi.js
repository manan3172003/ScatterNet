import {getCookie } from './utils.js';

export async function uploadReel(videoFile, caption, visibility = "PUBLIC") {
 
  const formData = new FormData();
  formData.append('video', videoFile);
  formData.append('caption', caption);
  formData.append('visibility', visibility);
  // Creating formdata object to send the caption and video
  try {
    const response = await fetch('/api/reels/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: formData,
      credentials: 'include'
    });
    
    
    if (!response.ok) {
      try {
        const errorText = await response.text();
        console.error("Upload error response:", errorText);
      } catch (e) {
        console.error("Could not read error response:", e);
      }
    }
    
    return response;
  } catch (error) {
    console.error("Error during upload:", error);
    throw error;
  }
}

export async function getReelsFeed() {
  try {
    const response = await fetch('/api/reels/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include' 
    });
    
    if (!response.ok) {
      try {
        const errorText = await response.text();
        console.error("Feed error response:", errorText);
      } catch (e) {
        console.error("Could not read feed error response:", e);
      }
    }
    
    return response;
  } catch (error) {
    console.error("Error fetching feed:", error);
    throw error;
  }
}

export async function viewReel(reelId) {
  try {
    const response = await fetch(`/api/reels/${reelId}/view/`, {
      method: 'GET',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include'
    });
    return response;
  } catch (error) {
    return { ok: false, status: 500 };
  }
}
export async function likeReel(reelId) {
  try {
    const response = await fetch(`/api/reels/${reelId}/like/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include'
    });
    
    return response;
  }
  catch (err) {
    console.warn("Error liking reel:", err);
    return { ok: false, status: 500 };
  }
}

export async function unlikeReel(reelId) {
  try {
    const response = await fetch(`/api/reels/${reelId}/unlike/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include'
    });
    
    return response;
  } catch (err) {
    console.warn("Error unliking reel:", err);
    return { ok: false, status: 500 };
  }
}

export async function addReelComment(reelId, content, contentType = 'text/plain') {
  try {
   
    const response = await fetch(`/api/reels/${reelId}/add_comment/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ 
        content: content,
        contentType: contentType 
      }),
      credentials: 'include'
    });
    
    return response;
  } catch (error) {
    console.error(`Error commenting on reel ${reelId}:`, error);
    return { 
      ok: false, 
      status: 500,
      json: () => Promise.resolve({ error: 'Failed to add comment' })
    };
  }
}

export async function getReelComments(reelId) {
  try {
    const response = await fetch(`/api/reels/${reelId}/comments/`);
    if (!response || !response.ok) {
      console.warn("Failed to get comments, API returned:", response?.status);
      return { 
        ok: false, 
        results: [],
        json: () => Promise.resolve([])
      };
    }
    
    return response;
  } catch (err) {
    console.error("Error fetching comments:", err);
    return { 
      ok: false, 
      status: 500,
      results: [],
      json: () => Promise.resolve([])
    };
  }
}

export async function likeComment(reelId, commentId) {
  try {
    const response = await fetch(`/api/reels/${reelId}/comment_likes/${commentId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include'
    });
    
    return response;
  } catch (error) {
    console.error("Error liking comment:", error);
    return { ok: false, status: 500 };
  }
}

export async function unlikeComment(reelId, commentId) {
  try {
    const response = await fetch(`/api/reels/${reelId}/comment_likes/${commentId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include'
    });
    
    return response;
  } catch (error) {
    console.error("Error unliking comment:", error);
    return { ok: false, status: 500 };
  }
}