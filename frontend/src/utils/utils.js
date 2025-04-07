export const validExtensions = ['png','jpeg']
export const validVideoExtensions  = ["mp4","webm","mov"]
function convertToBase64(selectedFile) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        console.log('File being processed:', selectedFile);
        console.log('Reader result at load:', reader.result);

        reader.onload = function() {
            console.log('called: ', reader);
            resolve(reader.result);
        };

        reader.onerror = function(error) {
            reject(error);
        };

        reader.readAsDataURL(selectedFile);
    });
}

const fetchUserData = async () => {
        try {
          const response = await apiCall("authors/current-user");

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
            const response = await apiCall(`authors/${user.author_id}`);

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
            const response = await apiCall(`authors/${author_serial}`);

            if (!response.ok) {
                throw new Error(`Error fetching author: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Failed to fetch author:", error);
            return null;
        }
}

async function handleFile(e, setFileName, setBase64,setBase64ContentType) {
        const selectedFile = e.target.files[0];

        if (!selectedFile) {
            console.error("No file selected!");
            return;
        }
        console.log('File being processed:', selectedFile);

        try {
            setFileName(selectedFile.name);
            const base64string = await convertToBase64(selectedFile);
            console.log('Base64 String before strip: ', base64string);
            const [contentTypeWithPrefix, base64DataString] = base64string.split(','); //splits string to data:datatype and the base64 string
            const base64ContentType = contentTypeWithPrefix.replace("data:", "");// strip data
            
            setBase64(base64DataString); 
            setBase64ContentType(base64ContentType); 
            
            console.log('Base64 Content Type:', base64ContentType);
            console.log('Base64 Data:', base64DataString);
            console.log('Base64 String: ', base64string);
    
        } catch (error) {
            console.error('Error converting file to Base64: ', error);
        }
}

async function apiCall(
    endpoint,
    httpmethod = "GET",
    body = null,
) {
    return await fetch(
        `/api/${endpoint}`,
        {
            method: httpmethod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: (body !== null) ? JSON.stringify(body) : body,
            credentials: "include"
        }
    );
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

function getPostHostname(post) {
  try {
    const url = new URL(post.id);
    return url.origin; // this pulls out the stuff like "http://localhost:8000"
  } catch (error) {
    // try using the fall back to the author's node instead id
    try {
      const authorUrl = new URL(post.author.id);
      return authorUrl.origin;
    } catch (e) {
      console.error("Could not figure out hostname");
      return "";
    }
  }
}
export async function handleVideoFile(e,setFileName,setBase64,setBase64ContentType,setVideoPreview,setUploadProgress,setIsUploading,showNotification) {
  const file = e.target.files[0]
  if (!file){
    return false
  }

  setFileName(file.name)
  const maxSize = 50 * 1024 * 1024
  if (file.size > maxSize) {
    showNotification(
      "error",
      "File Size Too Large",
      `Video must be less than 50MB`
    )
    return false
  }

  const extension = file.name.split(".").pop().toLowerCase()
  if (!validVideoExtensions.includes(extension)){
    showNotification(
      "error",
      "Invalid File Type",
      "Please upload a video with one of the following file types(mp4, mov, webm)."
    )
    return false
  }
  const videoURL = URL.createObjectURL(file)
  setVideoPreview(videoURL)
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onprogress = (event) => {

      if (event.lengthComputable){
        const progress = Math.round((event.loaded / event.total) * 100)
        setUploadProgress(progress)
        setIsUploading(true)
      }
    }

    reader.onload =() => {
      const base64String = reader.result.split(",")[1]
      setBase64(base64String)
      setBase64ContentType(`video/${extension};base64`)
      setIsUploading(false)
      setUploadProgress(100)
      
      showNotification(
          "success",
          "Video Ready",
          "Your video has been successfully loaded."
      )
      resolve(true)
    }
    reader.readAsDataURL(file)

  })

}   

export {getCookie, fetchUserData, getAuthorObject, apiCall, convertToBase64, handleFile, getAuthorObjectById,
    getPostHostname}
