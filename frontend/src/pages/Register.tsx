import { useState } from "react";
import { postJSON } from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await postJSON("/users/register", { username, email, password });
      if (res.ok) {
        navigate("/login");
      } else {
        const data = await res.json();
        setError(data.error || "登録に失敗しました。入力内容を確認してください。");
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
        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>新規登録</h2>
        
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
            <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>メールアドレス</label>
            <input 
              type="email"
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
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
            {loading ? "登録中..." : "登録"}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          すでにアカウントをお持ちですか？ <Link to="/login">ログイン</Link>
        </p>
      </div>
    </div>
  );
}

