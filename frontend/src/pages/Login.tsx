import { useState } from "react";
import { postJSON } from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Login({ onLoginSuccess }: { onLoginSuccess: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await postJSON("/users/login", { username, password });
      if (res.ok) {
        onLoginSuccess();
        navigate("/posts");
      } else {
        setError("ユーザー名またはパスワードが正しくありません");
      }
    } catch (err) {
      setError("ネットワークエラーが発生しました。もう一度お試しください。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', paddingTop: '4rem' }}>
      <div className="card" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>ログイン</h2>
        
        {error && <div className="error-box">{error}</div>}

        <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>ユーザー名</label>
            <input 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>パスワード</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e)=>setPassword(e.target.value)} 
              required
            />
          </div>
          <button type="submit" className="primary" disabled={loading} style={{ marginTop: '0.5rem' }}>
            {loading ? "ログイン中..." : "ログイン"}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          アカウントをお持ちでないですか？ <Link to="/register">新規登録</Link>
        </p>
      </div>
    </div>
  );
}

