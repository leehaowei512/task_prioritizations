'use client';

import { useState } from 'react';

interface Task {
  task_id: number;
  user_name: string;
  team_name: string;
  priority_name: string;
  effort: number;
  description: string;
}

export default function AllocationsPage() {
  const [resourceInput, setResourceInput] = useState('');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAllocate = async () => {
    if (!resourceInput) return;

    setLoading(true);
    setError('');

    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(
        `${API_BASE}/api/v1/allocate-tasks/?available_effort=${resourceInput}`
      );

      if (!response.ok) throw new Error('Failed to allocate tasks');

      const result = await response.json();
      setTasks(result.allocated_tasks || []);
    } catch (err) {
      setError('Failed to allocate tasks. Please check if the server is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Resource Allocation</h1>

      {error && (
        <div style={{ color: 'red', margin: '10px 0', padding: '10px', border: '1px solid red' }}>
          Error: {error}
        </div>
      )}

      <div style={{ margin: '20px 0' }}>
        <label>Available Resources: </label>
        <input
          type="number"
          value={resourceInput}
          onChange={(e) => setResourceInput(e.target.value)}
          placeholder="Enter resource units"
          style={{ padding: '5px', margin: '0 10px' }}
        />
        <button
          onClick={handleAllocate}
          disabled={loading || !resourceInput}
          style={{ padding: '5px 15px' }}
        >
          {loading ? 'Allocating...' : 'Allocate'}
        </button>
      </div>

      {tasks.length > 0 && (
        <div>
          <h2>Allocated Tasks ({tasks.length})</h2>
          <table style={{ borderCollapse: 'collapse', width: '100%', marginTop: '20px' }}>
            <thead>
              <tr style={{ backgroundColor: '#f2f2f2' }}>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Description</th>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Assignee</th>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Team</th>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Priority</th>
                <th style={{ border: '1px solid #ddd', padding: '8px' }}>Effort</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(task => (
                <tr key={task.task_id}>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.description}</td>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.user_name}</td>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.team_name}</td>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.priority_name}</td>
                  <td style={{ border: '1px solid #ddd', padding: '8px' }}>{task.effort}h</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div style={{ marginTop: '30px' }}>
        <a href="/tasks" style={{ color: 'blue', textDecoration: 'none' }}>
          ← Back to Tasks Dashboard
        </a>
      </div>
    </div>
  );
}