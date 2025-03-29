export type Author = {
    serial: number;
    type: "author";
    id: string;
    host: string;
    displayName: string;
    profileImage: string;
    page: string;
}

export type Like = {
    serial: number;
    type: "like";
    author: Author;
    published: string;
    id: string;
    object: string;
}

export type Likes = {
    count: number;
    next: string | null;
    previous: string | null;
    type: "likes";
    src: Array<Like>;
}

export type Comment = {
    serial: number;
    type: "comment";
    author: Author;
    comment: string;
    contentType: 'text/plain' | 'text/markdown';
    published: string;
    id: string;
    post: string;
    likes: Likes;
}

export type Comments = {
    count: number;
    next: string | null;
    previous: string | null;
    type: "comments";
    src: Array<Comment>;
}

export type Post = {
    serial: number;
    type: "post";
    title: string;
    id: string;
    page: string;
    description: string;
    contentType: 'text/plain' | 'text/markdown' | 'image/png;base64' | 'image/jpeg;base64' | 'application/base64';
    content: string;
    author: Author;
    comments: Comments;
    likes: Likes;
    published: string;
    visibility: 'PUBLIC' | 'FRIENDS' | 'UNLISTED' | 'DELETED';
}