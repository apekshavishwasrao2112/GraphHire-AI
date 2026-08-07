import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import SectionCard from '../components/SectionCard';

const skillsData = [
  { name: 'Python', value: 74 },
  { name: 'React', value: 68 },
  { name: 'Neo4j', value: 54 },
  { name: 'AWS', value: 47 },
  { name: 'Go', value: 41 },
];

const companyData = [
  { name: 'OpenAI', value: 22 },
  { name: 'Stripe', value: 18 },
  { name: 'Notion', value: 14 },
  { name: 'Databricks', value: 13 },
];

const pieData = [
  { name: 'Senior', value: 38 },
  { name: 'Mid', value: 42 },
  { name: 'Junior', value: 20 },
];

const COLORS = ['#22d3ee', '#8b5cf6', '#f59e0b'];

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      <SectionCard title="Analytics studio" subtitle="Interactive charts reveal popularity, distribution, and graph intensity across the developer network.">
        <div className="grid gap-6 xl:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
            <h4 className="text-white">Top skills</h4>
            <div className="mt-4 h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={skillsData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#22d3ee" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
            <h4 className="text-white">Company distribution</h4>
            <div className="mt-4 h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={companyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
            <h4 className="text-white">Experience mix</h4>
            <div className="mt-4 h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
                    {pieData.map((entry, index) => (
                      <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
            <h4 className="text-white">Relationship statistics</h4>
            <div className="mt-4 space-y-3 text-sm text-slate-300">
              <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3"><span>Skills connected</span><span className="font-semibold text-cyan-300">1,280</span></div>
              <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3"><span>Projects linked</span><span className="font-semibold text-cyan-300">356</span></div>
              <div className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3"><span>Mutual connections</span><span className="font-semibold text-cyan-300">284</span></div>
            </div>
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
