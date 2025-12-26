import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Posts from "./pages/Posts";
import { getJSON, postJSON } from "./api";
import "./index.css";

function Header({ user, onLogout }: { user: any, onLogout: () => void }) {
  return (
    <header>
      <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--accent)' }}>
        Simple Diary
      </div>
      <nav className="nav-links">
        {user ? (
          <>
            <NavLink to="/posts">タイムライン</NavLink>
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{user.username}</span>
            <button onClick={onLogout} className="secondary" style={{ padding: '0.4rem 0.8rem' }}>ログアウト</button>
          </>
        ) : (
          <>
            <NavLink to="/login">ログイン</NavLink>
            <NavLink to="/register">新規登録</NavLink>
          </>
        )}
      </nav>
    </header>
  );
}

function App() {
  const [user, setUser] = useState<any>(null);

  const fetchProfile = async () => {
    try {
      const res = await getJSON("/users/profile");
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        setUser(null);
      }
    } catch (e) {
      setUser(null);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleLogout = async () => {
    await postJSON("/users/logout", {});
    setUser(null);
    window.location.href = "/login";
  };

  return (
    <BrowserRouter>
      <Header user={user} onLogout={handleLogout} />
      <main>
        <Routes>
          <Route path="/login" element={<Login onLoginSuccess={fetchProfile} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/posts" element={<Posts currentUser={user} />} />
          <Route path="*" element={<Posts currentUser={user} />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;

