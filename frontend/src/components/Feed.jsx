import { useState, useEffect } from "react";
import PostModal from "../components/PostModal";
import MobileCommentModal from "../components/MobileCommentModal";
import Post from "../components/Post";
import InfiniteScroll from "react-infinite-scroll-component";
export default function Feed() {
  const fakePosts = [
    {
      type: "post",

      title: "A post title about a post about web dev",

      id: "http://nodebbbb/api/authors/222/posts/249",

      page: "http://nodebbbb/authors/222/posts/293",
      // a brief description of the post
      description: "This post discusses stuff -- brief",

      contentType: "text/plain",
      content:
        "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
      // the author has an ID where by authors can be disambiguated
      author: {
        type: "author",

        id: "http://nodebbbb/api/authors/222",

        host: "http://nodebbbb/api/",

        displayName: "Lara Croft",

        page: "http://nodebbbb/authors/222",

        github: "http://github.com/laracroft",
        profileImage: "http://nodebbbb/api/authors/222/posts/217/image",
      },
      // comments about the post
      comments: {
        type: "comments",

        page: "http://nodebbbb/authors/222/posts/249",
        id: "http://nodebbbb/api/authors/222/posts/249/comments",

        page_number: 1,
        // size of comment pages
        size: 5,
        // total number of comments for this post
        count: 1023,
        // the first page of comments
        src: [
          {
            type: "comment",
            author: {
              type: "author",
              id: "http://nodeaaaa/api/authors/111",
              page: "http://nodeaaaa/authors/greg",
              host: "http://nodeaaaa/api/",
              displayName: "Greg Johnson",
              github: "http://github.com/gjohnson",
              profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
            },
            comment: "Sick Olde English",
            contentType: "text/markdown",
            // ISO 8601 TIMESTAMP
            published: "2015-03-09T13:07:04+00:00",
            // ID of the Comment
            id: "http://nodeaaaa/api/authors/111/commented/130",
            post: "http://nodebbbb/api/authors/222/posts/249",
            // this may or may not be the same as page for the post,
            // depending if there's a seperate URL to just see the one comment in html
            page: "http://nodebbbb/authors/222/posts/249",
            // it could also be something like
            // "page":"http://nodeaaaa/api/authors/greg/comments/130"
            // likes on the comment, not to be confused with likes on the post
            likes: {
              type: "likes",
              id: "http://nodeaaaa/api/authors/111/commented/130/likes",
              // in this example nodebbbb has a html page just for the likes
              page: "http://nodeaaaa/authors/greg/comments/130/likes",
              page_number: 1,
              size: 50,
              count: 0,
              src: [],
            },
          },
        ],
      },
      // likes on the post
      likes: {
        type: "likes",
        // this may or may not be the same as page for the post,
        // depending if there's a seperate URL to just see the comments
        page: "http://nodeaaaa/authors/222/posts/249",
        id: "http://nodeaaaa/api/authors/222/posts/249/likes",
        // likes.page, likes.size, likes.count,
        // likes.src should be sent for public and unlisted posts
        // in order to reduce API calls
        // You should return ~ 5 likes per post.
        // should be sorted newest(first) to oldest(last)
        // this is to reduce API call counts
        // number of the first page of likes
        page_number: 1,
        // size of a page of likes
        size: 50,
        // total number of likes
        count: 9001,
        // the first page of likes
        src: [
          {
            type: "like",
            author: {
              type: "author",
              id: "http://nodeaaaa/api/authors/111",
              page: "http://nodeaaaa/authors/greg",
              host: "http://nodeaaaa/api/",
              displayName: "Greg Johnson",
              github: "http://github.com/gjohnson",
              profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
            },
            // ISO 8601 TIMESTAMP
            published: "2015-03-09T13:07:04+00:00",
            // ID of the Comment (UUID)
            id: "http://nodeaaaa/api/authors/111/liked/166",
            // this should be the object they liked
            object: "http://nodebbbb/authors/222/posts/249",
          },
        ],
      },
      // ISO 8601 TIMESTAMP
      published: "2015-03-09T13:07:04+00:00",
      // visibility ["PUBLIC","FRIENDS","UNLISTED","DELETED"]
      visibility: "PUBLIC",
    },
    {
      type: "post",
      title: "DID YOU READ MY POST YET?",
      id: "http://nodebbbb/api/authors/222/posts/293",
      // The frontend URL of this post
      page: "http://nodebbbb/authors/222/posts/293",
      description: "Whatever",
      contentType: "text/plain",
      content: "Are you even reading my posts Arjun?",
      author: {
        type: "author",
        id: "http://nodebbbb/api/authors/222",
        host: "http://nodebbbb/api/",
        displayName: "Lara Croft",
        page: "http://nodebbbb/authors/222",
        github: "http://github.com/laracroft",
        profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
      },
      comments: {
        type: "comments",
        id: "http://nodebbbb/api/authors/222/posts/293/comments",
        // in this example nodebbbb has a html page just for the comments
        page: "http://nodebbbb/authors/222/posts/293/comments",
        page_number: 1,
        size: 5,
        count: 0,
        src: [],
      },
      likes: {
        type: "likes",
        id: "http://127.0.0.1:5454/api/authors/222/posts/293/likes",
        // in this example nodebbbb has a html page just for the likes
        page: "http://nodebbbb/authors/222/posts/293/likes",
        page_number: 1,
        size: 50,
        count: 0,
        src: [],
      },
      published: "2015-03-09T13:07:04+00:00",
      visibility: "FRIENDS",
    },
  ];

  const [selectedPost, setSelectedPost] = useState(null);
  const [showComments, setShowComments] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  function handlePostClick(post) {
    if (!isMobile) {
      selectedPost(post);
    }
  }
  function handleCommentClick(post, e) {
    console.log("This got called!");
    e.stopPropagation();
    if (isMobile) {
      setSelectedPost(post);
      setShowComments(true);
    }
  }
  async function fetchMorePosts() {
    try {
      const response = await fetch(`http://localhost:8000/api/posts?page=${1}`); // to be added
      const data = await response.json();
      console.log(data); // to be added
    } catch (error) {
      console.error("Error fetching posts:", error);
    }
  }
  return (
    <InfiniteScroll
      dataLength={fakePosts.length}
      next={fetchMorePosts}
      loader={<p>Loading more posts...</p>}
      endMessage={<p>No more posts to show.</p>}
    >
      <main className="feed-container">
        {fakePosts.map((post) => (
          <Post
            key={post.id}
            post={post}
            onPostClick={() => handlePostClick(post)}
            onCommentClick={(e) => handleCommentClick(post, e)}
          />
        ))}
      </main>
      {!isMobile && selectedPost && (
        <PostModal post={selectedPost} onClose={() => setSelectedPost(null)} />
      )}
      {isMobile && showComments && (
        <MobileCommentModal
          post={selectedPost}
          onClose={() => setShowComments(false)}
        />
      )}
    </InfiniteScroll>
  );
}
