import { useEffect, useState } from "react";
import { getJSON, postJSON, deleteJSON } from "../api";

type Post = { id: number; content: string; user_id?: number; created_at?: string };

export default function Posts() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [content, setContent] = useState("");

  async function load() {
    const res = await getJSON("/posts/");
    if (res.ok) {
      const body = await res.json();
      setPosts(body);
    } else {
      console.error("Failed to load posts");
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function create(e: React.FormEvent) {
    e.preventDefault();
    const res = await postJSON("/posts/", { content });
    if (res.ok) {
      setContent("");
      load();
    } else {
      alert("Failed to create post");
    }
  }

  async function remove(id: number) {
    if (!confirm("Delete this post?")) return;
    const res = await deleteJSON(`/posts/${id}`);
    if (res.ok) load();
    else alert("Failed to delete");
  }

  return (
    <div>
      <h2>Posts</h2>
      <form onSubmit={create}>
        <textarea value={content} onChange={(e) => setContent(e.target.value)} />
        <button type="submit">Create</button>
      </form>
      <ul>
        {posts.map((p) => (
          <li key={p.id}>
            {p.content} <button onClick={() => remove(p.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
