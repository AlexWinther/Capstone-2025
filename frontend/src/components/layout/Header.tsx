import { Link } from "react-router-dom";
import { UserButton } from "@clerk/clerk-react";

export default function Header() {
  return (
    <header className="glass-strong sticky top-0 z-10 mb-8 flex items-center justify-between rounded-b-3xl px-8 py-6 shadow-md">
      <div className="flex items-center gap-5">
        <Link to="/" className="flex items-center gap-5 no-underline text-inherit">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
            <span className="text-xl font-bold text-white">C</span>
          </div>
          <h1 className="m-0 text-2xl font-bold text-text-primary">Capstone 2025</h1>
        </Link>
      </div>
      <div className="flex items-center gap-10">
        <Link
          to="/create-project"
          className="rounded-3xl bg-gradient-to-r from-primary to-primary-light px-10 py-4 font-bold text-white shadow-lg transition-all hover:scale-105 hover:shadow-xl"
        >
          Start a New Project
        </Link>
        <UserButton />
      </div>
    </header>
  );
}

