import { useState } from "react";

export default function TaskForm({ addTask }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [due, setDue] = useState("");
  const [fullNote, setFullNote] = useState("");

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setDue("");
    setFullNote("");
  };

  return (
    <div className="card input-card">
      <h2>Add a Task</h2>

      <div className="input-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
        />
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Short description"
        />
        <input type="date" value={due} onChange={(e) => setDue(e.target.value)} />
        <textarea
          value={fullNote}
          onChange={(e) => setFullNote(e.target.value)}
          placeholder="Extra notes (optional)"
          rows="2"
        />
      </div>

      <button className="cute-btn" onClick={() => addTask(title, description, due, fullNote, resetForm)}>
        ➕ Add Task
      </button>
    </div>
  );
}
