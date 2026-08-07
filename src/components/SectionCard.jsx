import { motion } from 'framer-motion';

export default function SectionCard({ title, subtitle, children, accent = 'from-cyan-500/20 to-violet-500/20' }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.15 }}
      className={`rounded-3xl border border-white/10 bg-white/10 p-6 shadow-[0_20px_80px_-30px_rgba(0,0,0,0.65)] backdrop-blur-xl ${accent}`}
    >
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h3 className="text-xl font-semibold text-white">{title}</h3>
          <p className="mt-1 text-sm text-slate-400">{subtitle}</p>
        </div>
      </div>
      {children}
    </motion.section>
  );
}
