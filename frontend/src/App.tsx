import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Posts from "./pages/Posts";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/posts">Posts</Link> | <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
      </nav>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/posts" element={<Posts />} />
        <Route path="*" element={<Posts />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
