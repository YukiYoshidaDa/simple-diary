import { useEffect, useState } from "react";
import { getJSON, postJSON, deleteJSON } from "../api";

type Post = { id: number; content: string; user_id: number; created_at?: string };

export default function Posts({ currentUser }: { currentUser: any }) {
  const [posts, setPosts] = useState<Post[]>([]);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    try {
      const res = await getJSON("/posts/");
      if (res.ok) {
        const body = await res.json();
        setPosts(body);
      } else if (res.status === 401) {
        setError("ログインが必要です。");
      }
    } catch (err) {
      setError("サーバーへの接続に失敗しました。");
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function create(e: React.FormEvent) {
    e.preventDefault();
    if (!content.trim() || !currentUser) return;
    
    setLoading(true);
    try {
      const res = await postJSON("/posts/", { content });
      if (res.ok) {
        setContent("");
        await load();
      } else {
        alert("投稿に失敗しました。ログイン状態を確認してください。");
      }
    } finally {
      setLoading(false);
    }
  }

  async function remove(id: number, e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    
    if (!window.confirm("この日記を削除してもよろしいですか？")) return;
    
    try {
      const res = await deleteJSON(`/posts/${id}`);
      if (res.ok) {
        await load();
      } else {
        const data = await res.json().catch(() => ({}));
        alert(data.error || "権限がありません。自分の投稿のみ削除できます。");
      }
    } catch (err) {
      alert("通信エラーが発生しました。");
    }
  }

  return (
    <div>
      {currentUser && (
        <section className="card">
          <h3 style={{ marginBottom: '1rem' }}>今日の日記</h3>
          <form onSubmit={create}>
            <textarea 
              style={{ minHeight: '100px', marginBottom: '1rem' }}
              placeholder="今の気持ちを記録しましょう..."
              value={content} 
              onChange={(e) => setContent(e.target.value)} 
              disabled={loading}
            />
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button type="submit" className="primary" disabled={loading || !content.trim()}>
                {loading ? "保存中..." : "保存"}
              </button>
            </div>
          </form>
        </section>
      )}

      <div>
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: 700 }}>タイムライン</h2>
        
        {error && <div className="error-box" style={{ textAlign: 'center' }}>{error}</div>}

        {posts.length === 0 && !error && (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
            投稿がありません。最初の一歩を書き出してみましょう！
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {posts.map((p) => (
            <article key={p.id} className="card" style={{ padding: '1rem' }}>
              <div style={{ whiteSpace: 'pre-wrap', marginBottom: '1rem' }}>
                {p.content}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border)', paddingTop: '0.75rem' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  {p.created_at ? new Date(p.created_at).toLocaleDateString("ja-JP") : '今日'}
                </span>
                
                {currentUser && currentUser.id === p.user_id && (
                  <button 
                    type="button"
                    onClick={(e) => remove(p.id, e)} 
                    className="danger" 
                    style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
                  >
                    削除
                  </button>
                )}
              </div>
            </article>
          ))}
        </div>
      </div>
    </div>
  );
}

