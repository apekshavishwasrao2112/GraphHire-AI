import { motion } from 'framer-motion';
import { NavLink, Outlet } from 'react-router-dom';
import { FiCompass, FiHome, FiLayers, FiMoon, FiSun, FiUsers } from 'react-icons/fi';
import { useTheme } from '../context/ThemeContext';

const navigation = [
  { name: 'Home', href: '/' },
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Developers', href: '/developers' },
  { name: 'Graph', href: '/graph' },
  { name: 'Analytics', href: '/analytics' },
];

export default function MainLayout() {
  const { darkMode, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(92,124,250,0.18),_transparent_30%),linear-gradient(135deg,_#07111f,_#0f172a)] text-slate-100 transition-colors duration-300">
      <header className="sticky top-0 z-50 border-b border-white/10 bg-slate-950/60 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">
          <div>
            <p className="text-lg font-semibold tracking-wide text-cyan-300">GraphHire AI</p>
            <p className="text-sm text-slate-400">Graph-powered talent intelligence</p>
          </div>
          <nav className="hidden items-center gap-2 rounded-full border border-white/10 bg-white/5 p-2 md:flex">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition ${
                    isActive ? 'bg-cyan-500/20 text-cyan-200 shadow-lg shadow-cyan-500/10' : 'text-slate-300 hover:bg-white/10'
                  }`
                }
              >
                <Icon />
                {label}
              </NavLink>
            ))}
          </nav>
          <button
            onClick={toggleTheme}
            className="rounded-full border border-white/10 bg-white/10 p-3 text-slate-200 transition hover:bg-cyan-500/20"
          >
            {darkMode ? <FiSun /> : <FiMoon />}
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
          <Outlet />
        </motion.div>
      </main>

      <footer className="border-t border-white/10 bg-slate-950/70 px-6 py-10 text-sm text-slate-400">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <p>© 2026 GraphHire AI. Built for modern hiring intelligence.</p>
          <p>Developer graph networks • Skills intelligence • Company signal discovery</p>
        </div>
      </footer>
    </div>
  );
}
