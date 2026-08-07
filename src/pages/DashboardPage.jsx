import { useQuery } from '@tanstack/react-query';
import { FiBriefcase, FiCpu, FiDatabase, FiUsers } from 'react-icons/fi';
import { fetchDashboard } from '../services/api';
import SectionCard from '../components/SectionCard';

// Default appearance for stat cards; values will be populated from API
const statCardConfig = [
  { key: 'active_developers', title: 'Active Developers', icon: FiUsers, accent: 'from-cyan-500/20 to-blue-500/20' },
  { key: 'companies', title: 'Companies', icon: FiBriefcase, accent: 'from-violet-500/20 to-fuchsia-500/20' },
  { key: 'tech_domains', title: 'Tech Domains', icon: FiCpu, accent: 'from-emerald-500/20 to-lime-500/20' },
  { key: 'total_relationships', title: 'Connected Graphs', icon: FiDatabase, accent: 'from-amber-500/20 to-orange-500/20' },
];

export default function DashboardPage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['dashboard'], queryFn: fetchDashboard });

  const apiData = data?.data?.data || {};

  const isEmpty = !apiData.top_skills?.length && !apiData.top_companies?.length;

  return (
    <div className="space-y-8">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statCardConfig.map((card) => {
          const Icon = card.icon;
          const value = isLoading ? '—' : apiData.metrics?.[card.key] ?? '—';
          return (
            <div key={card.key} className={`rounded-3xl border border-white/10 bg-linear-to-br ${card.accent} p-5 backdrop-blur-xl`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-400">{card.title}</p>
                  <p className="mt-2 text-3xl font-semibold text-white">{isLoading ? 'Loading...' : value}</p>
                </div>
                <div className="rounded-2xl bg-slate-950/40 p-3 text-cyan-200"><Icon /></div>
              </div>
            </div>
          );
        })}
      </div>

      <SectionCard title="Live intelligence overview" subtitle="The graph engine is ready to expose developer signals and network strength.">
        {isLoading ? (
          <div className="p-6">Loading graph intelligence...</div>
        ) : isError ? (
          <div className="rounded-2xl border border-rose-400/20 bg-rose-500/10 p-4 text-rose-200">Unable to load analytics from the API. Please check the database connection.</div>
        ) : isEmpty ? (
          <div className="rounded-2xl border border-yellow-400/20 bg-yellow-500/10 p-4 text-yellow-200">No developer data available yet.</div>
        ) : (
          <div className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-5">
              <h4 className="text-white">Top skills</h4>
              <ul className="mt-4 space-y-2">
                {(apiData.top_skills || []).map((skill) => (
                  <li key={skill.skill} className="flex items-center justify-between rounded-2xl bg-white/5 px-3 py-2 text-sm text-slate-300">
                    <span>{skill.skill}</span>
                    <span className="text-cyan-300">{skill.developers} developers</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-5">
              <h4 className="text-white">Top companies</h4>
              <ul className="mt-4 space-y-2">
                {(apiData.top_companies || []).map((company) => (
                  <li key={company.company} className="flex items-center justify-between rounded-2xl bg-white/5 px-3 py-2 text-sm text-slate-300">
                    <span>{company.company}</span>
                    <span className="text-cyan-300">{company.employees} developers</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </SectionCard>
    </div>
  );
}
