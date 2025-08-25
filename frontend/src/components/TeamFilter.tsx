import { Team } from '../types';

interface TeamFilterProps {
  teams: Team[];
  selectedTeam: string;
  onTeamChange: (teamName: string) => void;
  loading: boolean;
}

export default function TeamFilter({ teams, selectedTeam, onTeamChange, loading }: TeamFilterProps) {
  return (
    <div className="filter-container">
      <label className="filter-label">Filter by Team:</label>
      <select
        value={selectedTeam}
        onChange={(e) => onTeamChange(e.target.value)}
        disabled={loading}
        className="filter-select"
      >
        <option value="">All Teams</option>
        {teams.map(team => (
          <option key={team.team_id} value={team.team_name}>
            {team.team_name}
          </option>
        ))}
      </select>
    </div>
  );
}