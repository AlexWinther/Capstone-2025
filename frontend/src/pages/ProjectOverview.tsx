import { useParams } from "react-router-dom";

export default function ProjectOverview() {
  const { projectId } = useParams<{ projectId: string }>();
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-8 text-3xl font-bold text-text-primary">Project Overview</h1>
      <p>Project ID: {projectId}</p>
      <p>Project Overview page - Coming soon</p>
    </div>
  );
}
