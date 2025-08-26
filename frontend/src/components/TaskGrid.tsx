'use client';

import { AgGridReact } from 'ag-grid-react';
import { Task } from '../types';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

interface TaskGridProps {
  tasks: Task[];
  loading: boolean;
}

export default function TaskGrid({ tasks, loading }: TaskGridProps) {
  const columnDefs = [
    {
      headerName: 'Description',
      field: 'description',
      flex: 2,
      filter: true,
      sortable: true
    },
    {
      headerName: 'Assignee',
      field: 'user_name',
      filter: true,
      sortable: true
    },
    {
      headerName: 'Team',
      field: 'team_name',
      filter: true,
      sortable: true
    },
    {
      headerName: 'Priority',
      field: 'priority_name',
      filter: true,
      sortable: true,
      width: 120
    },
    {
      headerName: 'Effort (h)',
      field: 'effort',
      filter: true,
      sortable: true,
      width: 120
    }
  ];

  const defaultColDef = {
    resizable: true,
    filter: true,
    sortable: true,
  };

  if (loading) {
    return <div className="loading">Loading tasks...</div>;
  }

  return (
    <div className="grid-container">
      <h2 className="grid-title">Tasks ({tasks.length})</h2>

      {tasks.length === 0 ? (
        <div className="empty-state">No tasks found</div>
      ) : (
        <div className="ag-theme-alpine" style={{ height: 500, width: '100%' }}>
          <AgGridReact
            rowData={tasks}
            columnDefs={columnDefs}
            defaultColDef={defaultColDef}
            pagination={true}
            paginationPageSize={20}
            suppressCellFocus={true}
            domLayout='normal'
          />
        </div>
      )}
    </div>
  );
}