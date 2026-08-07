export default function AboutPage() {
  return (
    <div className="space-y-8">
      <section className="rounded-[2rem] border border-white/10 bg-gradient-to-br from-cyan-500/10 to-violet-500/10 p-8 backdrop-blur-xl">
        <h1 className="text-3xl font-semibold text-white">About GraphHire AI</h1>
        <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-300">
          GraphHire AI is designed for modern teams that need a richer picture of talent than keyword search can offer. By modeling developers, skills, projects, companies, technologies, and certifications as a graph, the platform reveals adjacency, similarity, and opportunity chains that static lists miss.
        </p>
      </section>
      <div className="grid gap-4 md:grid-cols-3">
        {['Graph-native data architecture', 'AI-assisted recommendations', 'Enterprise-ready analytics'].map((item) => (
          <div key={item} className="rounded-3xl border border-white/10 bg-white/10 p-6 text-slate-300">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
