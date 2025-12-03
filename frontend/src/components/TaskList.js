import React from "react";

export default function TaskList({ tasks, deleteTask }) {
  return (
    <div className="card">
      <h2>Your Tasks</h2>
      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id} className="task-item">
            <strong>{task.title}</strong>
            <p>{task.description}</p>
            <p>📅 Due: {task.due}</p>
            {task.full_note && <p>📝 {task.full_note}</p>}

            {/* --- Delete Button --- */}
            <button
              className="delete-btn"
              onClick={() => deleteTask(task.id)}
              style={{
                marginTop: "5px",
                backgroundColor: "#ff6961",
                color: "white",
                border: "none",
                borderRadius: "4px",
                padding: "2px 6px",
                cursor: "pointer",
              }}
            >
              🗑️ Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
