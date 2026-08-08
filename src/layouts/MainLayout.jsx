import { motion } from 'framer-motion';
import { NavLink, Outlet } from 'react-router-dom';
import {
  FiBarChart2,
  FiGitBranch,
  FiHome,
  FiMoon,
  FiSun,
  FiUsers,
} from 'react-icons/fi';
import { useTheme } from '../context/ThemeContext';

const navigation = [
  { name: 'Home', href: '/', icon: FiHome },
  { name: 'Dashboard', href: '/dashboard', icon: FiBarChart2 },
  { name: 'Developers', href: '/developers', icon: FiUsers },
  { name: 'Graph', href: '/graph', icon: FiGitBranch },
  { name: 'Analytics', href: '/analytics', icon: FiBarChart2 },
];

export default function MainLayout() {
  const { darkMode, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <h1 className="text-xl font-bold text-white">
              GraphHire AI
            </h1>
            <p className="text-xs text-slate-400">
              Graph-powered talent intelligence
            </p>
          </div>
          <nav className="flex max-w-full gap-1 overflow-x-auto sm:gap-2">
          {navigation.map(({ name, href }) => (
            <NavLink
              key={href}
              to={href}
              className={({ isActive }) =>
                `flex shrink-0 items-center rounded-full px-3 py-2 text-sm font-medium transition sm:px-4 ${
                  isActive
                    ? 'bg-cyan-500/20 text-cyan-200 shadow-lg shadow-cyan-500/10'
                    : 'text-slate-300 hover:bg-white/10'
                }`
              }
            >
              {name}
            </NavLink>
          ))}
        </nav>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Outlet />
        </motion.div>
      </main>

      <footer className="border-t border-white/10 bg-slate-950/70 px-6 py-10 text-sm text-slate-400">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <p>© 2026 GraphHire AI. Built for modern hiring intelligence.</p>
          <p>
            Developer graph networks • Skills intelligence • Company signal
            discovery
          </p>
        </div>
      </footer>
    </div>
  );
}

