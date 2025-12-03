import React, { useState, useEffect } from "react";
import "./App.css";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import AIPlan from "./components/AIPlan";

function App() {
  const [tasks, setTasks] = useState([]);
  const [ai, setAi] = useState({});

  const API = process.env.REACT_APP_API_URL;

  // Fetch tasks from backend on mount
  useEffect(() => {
    fetch(`${API}/tasks`)
      .then((res) => res.json())
      .then((data) => setTasks(data))
      .catch((err) => console.error("Error fetching tasks:", err));
  }, [API]);

  // Add a new task
  const addTask = (title, description, due, fullNote, resetForm) => {
    if (!title.trim()) return;

    const dueDate = new Date(due);

    fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description,
        due: dueDate.toISOString().split("T")[0],
        full_note: fullNote || null,
      }),
    })
      .then((res) => res.json())
      .then((data) => setTasks((prev) => [...prev, data]))
      .catch((err) => console.error("Error adding task:", err));

    resetForm();
  };

  // Delete a task
  const deleteTask = (id) => {
    fetch(`${API}/tasks/${id}`, {
      method: "DELETE",
    })
      .then((res) => {
        if (res.ok) {
          setTasks((prev) => prev.filter((task) => task.id !== id));
        } else {
          console.error("Failed to delete task");
        }
      })
      .catch((err) => console.error("Error deleting task:", err));
  };

  // Generate AI plan
  const generatePlan = () => {
    fetch(`${API}/plan-with-ai`)
      .then((res) => res.json())
      .then((data) => setAi(data.plan))
      .catch((err) => console.error("Error fetching AI plan:", err));
  };

  return (
    <div className="page">
      <h1 className="title">🌸 Study Planner 🌸</h1>

      <TaskForm addTask={addTask} />
      <TaskList tasks={tasks} deleteTask={deleteTask} />

      <button className="ai-btn" onClick={generatePlan}>
        ✨ Generate Plan With AI
      </button>

      <AIPlan ai={ai} />
    </div>
  );
}

export default App;
