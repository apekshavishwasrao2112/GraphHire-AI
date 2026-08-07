import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center rounded-[2rem] border border-white/10 bg-white/10 p-10 text-center backdrop-blur-xl">
      <p className="text-6xl font-semibold text-cyan-300">404</p>
      <h1 className="mt-4 text-3xl font-semibold text-white">The page you are looking for doesn’t exist.</h1>
      <p className="mt-4 max-w-xl text-slate-400">The route may have moved, or the graph view you requested isn’t available yet.</p>
      <Link to="/" className="mt-8 rounded-full bg-cyan-500 px-5 py-3 font-medium text-slate-950 transition hover:scale-[1.02]">Return home</Link>
    </div>
  );
}
