import { SidebarLayout } from "@/components/sidebar-layout.tsx";
import ContentCard from "@/components/post.tsx"
import {apiCall} from "@/utils/ApiCall.tsx";
import {useEffect, useState} from "react";

export function Homepage() {
  // const data = {
  //   type: "post",
  //   title: "A post title about a post about web dev",
  //   id: "http://nodebbbb/api/authors/222/posts/249",
  //   page: "http://nodebbbb/authors/222/posts/293",
  //   description: "This post discusses stuff -- brief",
  //   contentType: "text/plain",
  //   content: "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
  //   author: {
  //       type: "author",
  //       id: "http://nodebbbb/api/authors/222",
  //       host: "http://nodebbbb/api/",
  //       displayName: "Lara Croft",
  //       page: "http://nodebbbb/authors/222",
  //       github: "http://github.com/laracroft",
  //       profileImage: "http://nodebbbb/api/authors/222/posts/217/image"
  //   },
  //   comments: {
  //       type: "comments",
  //       page: "http://nodebbbb/authors/222/posts/249",
  //       id: "http://nodebbbb/api/authors/222/posts/249/comments",
  //       page_number: 1,
  //       size: 5,
  //       count: 1023,
  //       src: [
  //           {
  //               type: "comment",
  //               author: {
  //                   type: "author",
  //                   id: "http://nodeaaaa/api/authors/111",
  //                   page: "http://nodeaaaa/authors/greg",
  //                   host: "http://nodeaaaa/api/",
  //                   displayName: "Greg Johnson",
  //                   github: "http://github.com/gjohnson",
  //                   profileImage: "https://i.imgur.com/k7XVwpB.jpeg"
  //               },
  //               comment: "Sick Olde English",
  //               contentType: "text/markdown",
  //               published: "2015-03-09T13:07:04+00:00",
  //               id: "http://nodeaaaa/api/authors/111/commented/130",
  //               post: "http://nodebbbb/api/authors/222/posts/249",
  //               page: "http://nodebbbb/authors/222/posts/249",
  //               likes: {
  //                   type: "likes",
  //                   id: "http://nodeaaaa/api/authors/111/commented/130/likes",
  //                   page: "http://nodeaaaa/authors/greg/comments/130/likes",
  //                   page_number: 1,
  //                   size: 50,
  //                   count: 0,
  //                   src: [],
  //               },
  //           }
  //       ]
  //   },
  //   likes: {
  //       type: "likes",
  //       page: "http://nodeaaaa/authors/222/posts/249",
  //       id: "http://nodeaaaa/api/authors/222/posts/249/likes",
  //       page_number: 1,
  //       size: 50,
  //       count: 9001,
  //       src: [
  //           {
  //               type: "like",
  //               author: {
  //                   type: "author",
  //                   id: "http://nodeaaaa/api/authors/111",
  //                   page: "http://nodeaaaa/authors/greg",
  //                   host: "http://nodeaaaa/api/",
  //                   displayName: "Greg Johnson",
  //                   github: "http://github.com/gjohnson",
  //                   profileImage: "https://i.imgur.com/k7XVwpB.jpeg"
  //               },
  //               published: "2015-03-09T13:07:04+00:00",
  //               id: "http://nodeaaaa/api/authors/111/liked/166",
  //               object: "http://nodebbbb/authors/222/posts/249"
  //           }
  //       ]
  //   },
  //   published: "2015-03-09T13:07:04+00:00",
  //   visibility: "PUBLIC"
  // };
  interface PostData {
    id: string;
    title: string;
    description: string;
    contentType: 'text/plain' | 'text/markdown' | 'image/png;base64' | 'image/jpeg;base64' | 'application/base64';
    content:string;
    author: {
      id: string,
      displayName: string,
      profileImage: string,
    };
    visibility: 'PUBLIC' | 'FRIENDS' | 'UNLISTED' | 'DELETED';

  }

  // Use state to manage the data and loading state
  const [data, setData] = useState<PostData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Create an async function inside useEffect
    const fetchData = async () => {
      try {
        // Reset loading and error states
        setIsLoading(true);
        setError(null);

        // Make the API call
        const response = await apiCall('authors/2/posts/2');
        const responseData = await response.json();

        // Update state with fetched data
        setData(responseData);
        setIsLoading(false);
      } catch (err) {
        // Handle any errors during fetching
        setError('Failed to load post data');
        setIsLoading(false);
        console.error('Error fetching data:', err);
      }
    };

    // Call the async function
    fetchData();
  }, []); // Empty dependency array means this runs once on component mount

  // Handle loading and error states
  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }


  return (
      <SidebarLayout>
        <div className="p-6">
          <ContentCard
              id ={data!.id}
              type ={data!.contentType}
              title ={data!.title}
              content ={data!.content}
              description = {data!.description}
              user = {{
                id: data!.author.id,
                username: data!.author.displayName,
                profilePicture: data!.author.profileImage,
                isCurrentUser: true
              }}
              visibility = {data!.visibility}
          />
        </div>
      </SidebarLayout>
  )
}