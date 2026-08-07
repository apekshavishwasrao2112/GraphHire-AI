import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FiArrowRight, FiCpu, FiLayers, FiSearch, FiZap } from 'react-icons/fi';

const features = [
  { title: 'Graph-native discovery', description: 'Trace relationships across developers, skills, projects, and companies in a single view.', icon: FiSearch },
  { title: 'Signal-rich insights', description: 'Surface hidden connections, emerging talent patterns, and recommendation flows instantly.', icon: FiLayers },
  { title: 'Operational intelligence', description: 'Turn recruitment strategy into an always-on, data-shaped engine.', icon: FiCpu },
];

export default function LandingPage() {
  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-[2rem] border border-cyan-400/20 bg-slate-950/60 p-8 shadow-[0_40px_120px_-40px_rgba(34,211,238,0.55)] md:p-12">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(34,211,238,0.2),_transparent_35%),radial-gradient(circle_at_bottom_right,_rgba(167,139,250,0.25),_transparent_40%)]" />
        <div className="relative grid gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <div>
            <p className="inline-flex rounded-full border border-cyan-400/20 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-200">AI-powered talent graph intelligence</p>
            <h1 className="mt-6 text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
              Discover the people behind the next breakthrough.
            </h1>
            <p className="mt-6 max-w-2xl text-lg text-slate-300">
              GraphHire AI maps how developers, skills, projects, and companies connect, so teams can find opportunity before it becomes obvious.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link to="/dashboard" className="inline-flex items-center gap-2 rounded-full bg-cyan-500 px-5 py-3 font-medium text-slate-950 transition hover:scale-[1.02]">Explore platform <FiArrowRight /></Link>
              <Link to="/developers" className="rounded-full border border-white/10 bg-white/10 px-5 py-3 font-medium text-white transition hover:bg-white/20">Browse developers</Link>
            </div>
          </div>
          <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }} className="rounded-[2rem] border border-white/10 bg-white/10 p-6 backdrop-blur-xl">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400">Live graph overview</p>
                <p className="text-2xl font-semibold text-white">128+ connected signals</p>
              </div>
              <div className="rounded-full bg-emerald-500/20 p-3 text-emerald-300"><FiZap /></div>
            </div>
            <div className="grid gap-3">
              {['Developer network', 'Skill adjacency', 'Company partnerships', 'Project dependencies'].map((item) => (
                <div key={item} className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-900/60 px-4 py-3 text-sm text-slate-300">
                  <span>{item}</span>
                  <span className="text-cyan-300">Active</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.article key={feature.title} initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: index * 0.08 }} className="rounded-3xl border border-white/10 bg-white/10 p-6 backdrop-blur-xl">
              <div className="mb-4 inline-flex rounded-2xl bg-cyan-500/20 p-3 text-cyan-200"><Icon size={20} /></div>
              <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-400">{feature.description}</p>
            </motion.article>
          );
        })}
      </section>
    </div>
  );
}
