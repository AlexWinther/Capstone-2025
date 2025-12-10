import { useNavigate } from "react-router-dom";
import { cn } from "@/lib/utils";
import type { Project } from "@/types";

interface ProjectCardProps {
  project: Project;
  index: number;
}

/**
 * Formats date with CET timezone (+2 hours) and human-readable format
 */
function formatDate(dateString: string): string {
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return dateString;
  
  // Add 2 hours for CET
  d.setHours(d.getHours() + 2);
  
  return d.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Truncates text to maxLength, adding "..." if needed
 */
function truncateText(text: string, maxLength: number): string {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3).trim() + '...';
}

export function ProjectCard({ project, index }: ProjectCardProps) {
  const navigate = useNavigate();
  const animationDelay = `${index * 0.04 + 0.1}s`;
  const truncatedDescription = truncateText(project.description, 120);

  const handleClick = () => {
    if (project.project_id) {
      navigate(`/project/${project.project_id}`);
    }
  };

  return (
    <div
      onClick={handleClick}
      className={cn(
        "project-card glass rounded-3xl p-8 flex flex-col gap-6 cursor-pointer group",
        "transition-all duration-[180ms] ease-[cubic-bezier(0.4,2,0.6,1)]",
        "hover:-translate-y-2 hover:scale-[1.035]",
        "hover:shadow-[0_16px_48px_0_rgba(0,123,255,0.18)]",
        "hover:bg-white/55 hover:border-[#b3d1ff]",
        "border-[1.5px] border-white/35",
        "opacity-0 translate-y-10 scale-[0.98]",
        "will-change-[opacity,transform]"
      )}
      style={{ 
        animationDelay,
        animation: `cardFadeIn 0.7s cubic-bezier(0.4,2,0.6,1) forwards`,
      }}
    >
      <div className="text-[1.32rem] font-bold text-text-primary mb-0.5 tracking-[0.2px] drop-shadow-[0_2px_8px_rgba(0,0,0,0.03)]">
        {project.title}
      </div>
      
      <div className="text-[1.09rem] text-[#222b] leading-[1.7] min-h-[48px] font-medium overflow-hidden line-clamp-4 max-h-[6.8em]">
        {truncatedDescription}
      </div>
      
      {project.tags && project.tags.length > 0 && (
        <div className="flex flex-wrap gap-2.5 mb-1.5">
          {project.tags.map((tag, idx) => (
            <span
              key={idx}
              className={cn(
                "inline-block bg-[#f8f9fa] text-text-light px-2 py-1 rounded-xl",
                "text-xs font-medium border border-[#e9ecef] mr-2 mb-1",
                "transition-all duration-200 ease-[cubic-bezier(0.25,0.46,0.45,0.94)]",
                "group-hover:text-primary group-hover:bg-[rgba(0,123,255,0.1)]",
                "group-hover:border-[rgba(0,123,255,0.2)] group-hover:-translate-y-0.5"
              )}
            >
              {tag}
            </span>
          ))}
        </div>
      )}
      
      <div className="mt-auto text-[0.99rem] text-[#6c7a8a] tracking-[0.1px] font-medium">
        Created: {formatDate(project.date)}
      </div>
    </div>
  );
}

