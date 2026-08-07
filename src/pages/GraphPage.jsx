import { useCallback, useMemo, useState } from 'react';
import ReactFlow, { Background, Controls, MiniMap, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';
import SectionCard from '../components/SectionCard';

const initialNodes = [
  { id: 'developer', type: 'input', data: { label: 'Developer' }, position: { x: 250, y: 100 }, style: { background: '#22d3ee', color: '#052e2e', borderColor: '#67e8f9' } },
  { id: 'company', data: { label: 'Company' }, position: { x: 80, y: 250 }, style: { background: '#8b5cf6', color: '#fff', borderColor: '#c4b5fd' } },
  { id: 'project', data: { label: 'Project' }, position: { x: 420, y: 250 }, style: { background: '#f59e0b', color: '#fff', borderColor: '#fcd34d' } },
  { id: 'skill', data: { label: 'Skill' }, position: { x: 250, y: 400 }, style: { background: '#10b981', color: '#fff', borderColor: '#6ee7b7' } },
];

const initialEdges = [
  { id: 'e1', source: 'developer', target: 'company', animated: true, label: 'WORKED_AT' },
  { id: 'e2', source: 'developer', target: 'project', animated: true, label: 'BUILT' },
  { id: 'e3', source: 'developer', target: 'skill', animated: true, label: 'HAS_SKILL' },
];

export default function GraphPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState(null);

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
    setNodes((currentNodes) => currentNodes.map((item) => ({ ...item, style: { ...item.style, opacity: item.id === node.id ? 1 : 0.5 } })));
  }, [setNodes]);

  const summary = useMemo(() => (selectedNode ? `Selected ${selectedNode.data.label} node` : 'Click a node to inspect relationships'), [selectedNode]);

  return (
    <div className="space-y-8">
      <SectionCard title="Graph explorer" subtitle="Interactive graph visualization for developers, companies, projects, skills, and relationships.">
        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="h-[480px] rounded-3xl border border-white/10 bg-slate-950/40 p-2">
            <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onNodeClick={onNodeClick} fitView>
              <MiniMap nodeStrokeColor="#94a3b8" nodeColor="#0f172a" />
              <Controls />
              <Background gap={16} color="#ffffff20" />
            </ReactFlow>
          </div>
          <div className="rounded-3xl border border-white/10 bg-slate-950/40 p-6">
            <h4 className="text-white">Graph insights</h4>
            <p className="mt-3 text-sm leading-6 text-slate-400">{summary}</p>
            <div className="mt-6 space-y-3 text-sm text-slate-300">
              <div className="rounded-2xl bg-white/5 px-4 py-3">Nodes support zoom, pan, and selection-driven detail inspection.</div>
              <div className="rounded-2xl bg-white/5 px-4 py-3">Animated edges communicate relationship strength and direction.</div>
              <div className="rounded-2xl bg-white/5 px-4 py-3">The graph can evolve into a live CognoDB-backed network.</div>
            </div>
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
