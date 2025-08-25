export interface Task {
  task_id: number;
  user_name: string;
  team_name: string;
  priority_name: string;
  priority_value: number;
  effort: number;
  date_added: string;
  time_added: string;
  description: string;
}

export interface Team {
  team_id: number;
  team_name: string;
}