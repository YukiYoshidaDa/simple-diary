import { useState } from "react";
import { postJSON } from "../api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const res = await postJSON("/users/login", { username, password });
    if (res.ok) {
      navigate("/posts");
    } else {
      alert("Login failed");
    }
  }

  return (
    <form onSubmit={submit}>
      <h2>Login</h2>
      <div>
        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
      </div>
      <button type="submit">Login</button>
    </form>
  );
}
