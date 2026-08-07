import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { FiFilter, FiSearch } from 'react-icons/fi';
import { fetchDevelopers } from '../services/api';
import SectionCard from '../components/SectionCard';

export default function DevelopersPage() {
  const [query, setQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');

  const { data, isLoading, isError } = useQuery({
    queryKey: ['developers', query],
    queryFn: () => fetchDevelopers(query, 20),
    keepPreviousData: true,
  });

 
const filtered = useMemo(() => {
  const items = Array.isArray(data?.data?.data)
    ? data.data.data
    : [];

  console.log("API DATA:", data);
  console.log("ITEMS:", items);

  if (activeFilter === 'all') return items;

  return items.filter(
    (item) => (item?.developer?.experience ?? 0) >= 5
  );

}, [activeFilter, data]);

  return (
    <div className="space-y-8">
      <SectionCard title="Developer directory" subtitle="Explore the graph-powered talent network with smart search and interactive filters.">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <label className="flex flex-1 items-center gap-3 rounded-2xl border border-white/10 bg-slate-950/50 px-4 py-3 text-sm text-slate-300">
            <FiSearch />
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search developers by name or email" className="w-full bg-transparent outline-none" />
          </label>
          <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/10 px-4 py-3">
            <FiFilter />
            <select value={activeFilter} onChange={(e) => setActiveFilter(e.target.value)} className="bg-transparent text-sm outline-none">
              <option value="all">All developers</option>
              <option value="senior">Senior developers</option>
            </select>
          </div>
        </div>

        {isLoading ? (
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {Array.from({ length: 4 }).map((_, index) => (
              <div key={index} className="h-40 animate-pulse rounded-3xl bg-white/10" />
            ))}
          </div>
        ) : isError ? (
          <div className="mt-6 rounded-2xl border border-rose-400/20 bg-rose-500/10 p-4 text-rose-200">The developer directory could not be loaded.</div>
        ) : (
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {filtered.map((entry, index) => {
              const developer = entry.developer || {};
              return (
                <div key={developer.email || index} className="rounded-3xl border border-white/10 bg-slate-950/40 p-5 transition hover:-translate-y-1 hover:border-cyan-400/30">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-lg font-semibold text-white">{developer.name || 'Developer profile'}</h4>
                      <p className="text-sm text-slate-400">{developer.email || 'No email available'}</p>
                    </div>
                    <div className="rounded-full bg-cyan-500/20 px-3 py-1 text-sm text-cyan-200">{developer.experience || 'N/A'} yrs</div>
                  </div>
                  <p className="mt-4 text-sm leading-6 text-slate-400">{developer.bio || 'Graph-connected professional ready for high impact work.'}</p>
                </div>
              );
            })}
          </div>
        )}
      </SectionCard>
    </div>
  );
}
