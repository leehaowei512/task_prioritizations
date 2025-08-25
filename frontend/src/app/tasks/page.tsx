'use client';

import { useState, useEffect } from 'react';

interface Task {
  task_id: number;
  user_name: string;
  team_name: string;
  priority_name: string;
  effort: number;
  description: string;
}

interface Team {
  team_id: number;
  team_name: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError('');

      // Fetch teams
      const teamsResponse = await fetch(`${API_BASE}/api/v1/teams`);
      if (!teamsResponse.ok) {
        throw new Error(`HTTP error! status: ${teamsResponse.status}`);
      }
      const teamsData = await teamsResponse.json();
      setTeams(teamsData);

      // Fetch tasks
      const tasksResponse = await fetch(`${API_BASE}/api/v1/tasks`);
      if (!tasksResponse.ok) {
        throw new Error(`HTTP error! status: ${tasksResponse.status}`);
      }
      const tasksData = await tasksResponse.json();
      setTasks(tasksData);

    } catch (err) {
      setError('Failed to load data. Please check if the server is running on port 8000.');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTeamChange = (teamName: string) => {
    setSelectedTeam(teamName);

    if (teamName === '') {
      // Show all tasks
      fetch(`${API_BASE}/api/v1/tasks`)
        .then(res => res.json())
        .then(setTasks)
        .catch(console.error);
    } else {
      // Filter by team
      fetch(`${API_BASE}/api/v1/tasks?team=${encodeURIComponent(teamName)}`)
        .then(res => res.json())
        .then(setTasks)
        .catch(console.error);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '20px' }}>
        <h1>Tasks Dashboard</h1>
        <p>Loading data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px' }}>
        <h1>Tasks Dashboard</h1>
        <div style={{ color: 'red', padding: '10px', border: '1px solid red' }}>
          {error}
        </div>
        <button
          onClick={fetchData}
          style={{ marginTop: '10px', padding: '8px 16px' }}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Tasks Dashboard</h1>

      {/* Team Filter */}
      <div style={{ margin: '20px 0' }}>
        <label style={{ marginRight: '10px' }}>Filter by Team:</label>
        <select
          value={selectedTeam}
          onChange={(e) => handleTeamChange(e.target.value)}
          style={{ padding: '8px', minWidth: '200px' }}
        >
          <option value="">All Teams</option>
          {teams.map(team => (
            <option key={team.team_id} value={team.team_name}>
              {team.team_name}
            </option>
          ))}
        </select>
      </div>

      {/* Tasks Table */}
      <div>
        <h2>Tasks ({tasks.length})</h2>
        {tasks.length === 0 ? (
          <p>No tasks found</p>
        ) : (
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            marginTop: '20px',
            border: '1px solid #ddd'
          }}>
            <thead>
              <tr style={{ backgroundColor: '#f5f5f5' }}>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Description</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Assignee</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Team</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Priority</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Effort (h)</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(task => (
                <tr key={task.task_id}>
                  <td style={{ padding: '12px', border: '1px solid #ddd' }}>{task.description}</td>
                  <td style={{ padding: '12px', border: '1px solid #ddd' }}>{task.user_name}</td>
                  <td style={{ padding: '12px', border: '1px solid #ddd' }}>{task.team_name}</td>
                  <td style={{ padding: '12px', border: '1px solid #ddd' }}>{task.priority_name}</td>
                  <td style={{ padding: '12px', border: '1px solid #ddd' }}>{task.effort}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Navigation to Allocations */}
      <div style={{ marginTop: '30px' }}>
        <a
          href="/allocations"
          style={{
            color: 'blue',
            textDecoration: 'none',
            padding: '10px 20px',
            border: '1px solid blue',
            borderRadius: '4px'
          }}
        >
          Go to Resource Allocation →
        </a>
      </div>
    </div>
  );
}