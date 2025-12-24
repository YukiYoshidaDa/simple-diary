import { useState } from "react";
import { postJSON } from "../api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const res = await postJSON("/users/register", { username, email, password });
    if (res.ok) {
      navigate("/login");
    } else {
      const body = await res.json().catch(()=>null);
      alert(body?.message || "Register failed");
    }
  }

  return (
    <form onSubmit={submit}>
      <h2>Register</h2>
      <div>
        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label>Password</label>
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
      </div>
      <button type="submit">Register</button>
    </form>
  );
}
