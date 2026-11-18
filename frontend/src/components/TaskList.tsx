/**
 * Composant React strictement typé – consomme le contrat TaskResponse.
 * Styling Tailwind. Aucune logique métier ici, uniquement présentation.
 */
import React from "react";

export type TaskStatus = "todo" | "in_progress" | "done" | "cancelled";
export type TaskPriority = "low" | "medium" | "high" | "critical";

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onStatusChange?: (id: string, status: TaskStatus) => void;
  loading?: boolean;
}

const priorityStyles: Record<TaskPriority, string> = {
  low: "bg-slate-100 text-slate-700",
  medium: "bg-blue-100 text-blue-800",
  high: "bg-orange-100 text-orange-800",
  critical: "bg-red-100 text-red-800",
};

const statusStyles: Record<TaskStatus, string> = {
  todo: "border-l-4 border-slate-400",
  in_progress: "border-l-4 border-blue-500",
  done: "border-l-4 border-green-500 opacity-75",
  cancelled: "border-l-4 border-red-400 line-through",
};

export const TaskList: React.FC<TaskListProps> = ({ tasks, onStatusChange, loading = false }) => {
  if (loading) {
    return <div className="p-4 text-slate-500">Chargement des tâches…</div>;
  }

  if (tasks.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-slate-300 p-8 text-center text-slate-500">
        Aucune tâche pour le moment. Créez-en une via l’API.
      </div>
    );
  }

  return (
    <ul className="space-y-3">
      {tasks.map((task) => (
        <li
          key={task.id}
          className={`rounded-lg bg-white p-4 shadow-sm ${statusStyles[task.status]}`}
        >
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0 flex-1">
              <h3 className="truncate font-semibold text-slate-900">{task.title}</h3>
              {task.description && (
                <p className="mt-1 text-sm text-slate-600 line-clamp-2">{task.description}</p>
              )}
              <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
                <span className={`rounded-full px-2 py-0.5 font-medium ${priorityStyles[task.priority]}`}>
                  {task.priority}
                </span>
                <span className="text-slate-500">
                  {new Date(task.created_at).toLocaleDateString("fr-FR")}
                </span>
              </div>
            </div>
            {onStatusChange && (
              <select
                value={task.status}
                onChange={(e) => onStatusChange(task.id, e.target.value as TaskStatus)}
                className="rounded border border-slate-300 px-2 py-1 text-sm"
                aria-label={`Changer le statut de ${task.title}`}
              >
                <option value="todo">À faire</option>
                <option value="in_progress">En cours</option>
                <option value="done">Terminé</option>
                <option value="cancelled">Annulé</option>
              </select>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
