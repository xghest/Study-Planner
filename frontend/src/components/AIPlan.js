export default function AIPlan({ ai }) {
  return (
    <div className="card ai-card">
      <h2>Daily Plan</h2>

      {Object.keys(ai).length === 0 ? (
        <p>No plan yet.</p>
      ) : (
        <div className="plan-table-container">
          <table className="plan-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Tasks</th>
              </tr>
            </thead>

            <tbody>
              {Object.entries(ai)
                .filter(([_, tasks]) => tasks.length > 0)
                .map(([date, tasks]) => (
                  <tr key={date}>
                    <td>{date}</td>
                    <td>
                      <ul className="task-list">
                        {tasks.map((task, idx) => (
                          <li key={idx} className="task-item">
                            <span className="task-icon">🌸</span>
                            <span>{task}</span>
                          </li>
                        ))}
                      </ul>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
