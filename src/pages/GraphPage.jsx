import { useEffect, useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import { FiSearch } from 'react-icons/fi';
import 'reactflow/dist/style.css';

import SectionCard from '../components/SectionCard';
import { fetchGraphSearch } from '../services/api';

const getNodeLabel = (node) => {
  const properties = node?.properties || {};
  const labels = node?.labels || [];

  if (labels.includes('Developer')) {
    return (
      properties.full_name ||
      properties.name ||
      properties.email ||
      'Developer'
    );
  }

  if (labels.includes('Company')) {
    return properties.name || 'Company';
  }

  if (labels.includes('Project')) {
    return properties.name || 'Project';
  }

  if (labels.includes('Skill')) {
    return properties.name || 'Skill';
  }

  if (labels.includes('Technology')) {
    return properties.name || 'Technology';
  }

  if (labels.includes('Certification')) {
    return properties.name || 'Certification';
  }

  if (labels.includes('Location')) {
    return (
      properties.city ||
      properties.country ||
      'Location'
    );
  }

  return properties.name || labels[0] || 'Node';
};

const getNodeStyle = (node) => {
  const labels = node?.labels || [];

  if (labels.includes('Developer')) {
    return {
      background: '#22d3ee',
      color: '#052e2e',
      borderColor: '#67e8f9',
    };
  }

  if (labels.includes('Company')) {
    return {
      background: '#8b5cf6',
      color: '#ffffff',
      borderColor: '#c4b5fd',
    };
  }

  if (labels.includes('Project')) {
    return {
      background: '#f59e0b',
      color: '#ffffff',
      borderColor: '#fcd34d',
    };
  }

  if (labels.includes('Skill')) {
    return {
      background: '#10b981',
      color: '#ffffff',
      borderColor: '#6ee7b7',
    };
  }

  if (labels.includes('Technology')) {
    return {
      background: '#ec4899',
      color: '#ffffff',
      borderColor: '#f9a8d4',
    };
  }

  if (labels.includes('Certification')) {
    return {
      background: '#6366f1',
      color: '#ffffff',
      borderColor: '#a5b4fc',
    };
  }

  return {
    background: '#475569',
    color: '#ffffff',
    borderColor: '#94a3b8',
  };
};




const createPositions = (nodes) => {
  const centerX = 300;
  const centerY = 220;

  // Create an empty position array
  const positions = new Array(nodes.length);

  const developerIndex = nodes.findIndex((node) =>
    (node?.labels || []).includes('Developer')
  );

  // Developer stays in the center
  if (developerIndex !== -1) {
    positions[developerIndex] = {
      x: centerX,
      y: centerY,
    };
  }

  const groups = {
    Company: [],
    Project: [],
    Skill: [],
    Technology: [],
    Certification: [],
    Location: [],
    Other: [],
  };

  nodes.forEach((node, index) => {
    if (index === developerIndex) return;

    const labels = node?.labels || [];

    if (labels.includes('Company')) {
      groups.Company.push(index);
    } else if (labels.includes('Project')) {
      groups.Project.push(index);
    } else if (labels.includes('Skill')) {
      groups.Skill.push(index);
    } else if (labels.includes('Technology')) {
      groups.Technology.push(index);
    } else if (labels.includes('Certification')) {
      groups.Certification.push(index);
    } else if (labels.includes('Location')) {
      groups.Location.push(index);
    } else {
      groups.Other.push(index);
    }
  });

  const placeGroup = (indexes, centerXOffset, centerYOffset) => {
    if (!indexes.length) return;

    const radius = Math.max(100, indexes.length * 30);

    indexes.forEach((nodeIndex, index) => {
      const angle =
        (2 * Math.PI * index) / indexes.length;

      positions[nodeIndex] = {
        x:
          centerX +
          centerXOffset +
          radius * Math.cos(angle),
        y:
          centerY +
          centerYOffset +
          radius * Math.sin(angle),
      };
    });
  };

  placeGroup(groups.Company, 0, -180);
  placeGroup(groups.Project, 240, 0);
  placeGroup(groups.Skill, -240, 0);
  placeGroup(groups.Technology, 0, 180);
  placeGroup(groups.Certification, 240, 180);
  placeGroup(groups.Location, -240, 180);
  placeGroup(groups.Other, 0, 300);

  return positions;
};




const transformGraphData = (graph) => {
 const backendNodes = Array.isArray(graph?.nodes)
  ? graph.nodes.slice(0, 25)
  : [];

const backendEdges = Array.isArray(graph?.edges)
  ? graph.edges
      .filter(
        (edge) =>
          backendNodes.some((node) => String(node.id) === String(edge.source)) &&
          backendNodes.some((node) => String(node.id) === String(edge.target))
      )
      .slice(0, 40)
  : [];

const visibleNodes = backendNodes.slice(0, 15);

const visibleNodeIds = new Set(
  visibleNodes.map((node) => String(node.id))
);

const visibleEdges = backendEdges
  .filter(
    (edge) =>
      visibleNodeIds.has(String(edge.source)) &&
      visibleNodeIds.has(String(edge.target))
  )
  .slice(0, 20);


const positions = createPositions(visibleNodes);
const nodes = visibleNodes.map((node, index) => {
  const labels = node?.labels || [];
  const isDeveloper = labels.includes('Developer');

  return {
    id: String(node.id),
    data: {
      label: getNodeLabel(node),
      original: node,
    },
    position: positions[index],
   style: {
  ...getNodeStyle(node),
  padding: isDeveloper ? '16px 20px' : '10px 14px',
  borderWidth: isDeveloper ? 3 : 1,
  borderRadius: '14px',
  minWidth: isDeveloper ? 180 : 120,
  textAlign: 'center',
  fontWeight: isDeveloper ? 700 : 600,
  fontSize: isDeveloper ? '16px' : '13px',
  boxShadow: isDeveloper
    ? '0 0 30px rgba(34, 211, 238, 0.55)'
    : 'none',
},
  };
});

const edges = visibleEdges
  .slice(0, 20)
  .map((edge, index) => ({
    id: String(edge.id || `edge-${index}`),
    source: String(edge.source),
    target: String(edge.target),
    animated: false,
    style: {
      strokeWidth: 1.5,
      opacity: 0.65,
    },
  }))

  .filter(
    (edge) =>
      nodes.some((node) => node.id === edge.source) &&
      nodes.some((node) => node.id === edge.target)
  );
  return { nodes, edges };
};

export default function GraphPage() {
  const [searchInput, setSearchInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNode, setSelectedNode] = useState(null);

  const {
    data,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['graph-search', searchQuery],
    queryFn: () => fetchGraphSearch(searchQuery),
    enabled: Boolean(searchQuery),
  });

  const graphData = useMemo(() => {
    if (!data?.data?.data) {
      return {
        nodes: [],
        edges: [],
      };
    }

    return transformGraphData(data.data.data);
  }, [data]);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
  setNodes(graphData.nodes);
  setEdges(graphData.edges);
  setSelectedNode(null);
}, [graphData, setNodes, setEdges]);


 const handleSearch = () => {
  const value = searchInput.trim();

  if (!value) {
    return;
  }

  if (value === searchQuery) {
    return;
  }

  setSelectedNode(null);
  setSearchQuery(value);
};

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

 const handleNodeClick = (_, node) => {
  setSelectedNode(node);

  const connectedNodeIds = new Set([node.id]);

  edges.forEach((edge) => {
    if (edge.source === node.id) {
      connectedNodeIds.add(edge.target);
    }

    if (edge.target === node.id) {
      connectedNodeIds.add(edge.source);
    }
  });

  setNodes((currentNodes) =>
    currentNodes.map((item) => ({
      ...item,
      style: {
        ...item.style,
        opacity: connectedNodeIds.has(item.id) ? 1 : 0.2,
      },
    }))
  );

  setEdges((currentEdges) =>
    currentEdges.map((edge) => {
      const isConnected =
        edge.source === node.id ||
        edge.target === node.id;

      return {
        ...edge,
        animated: isConnected,
        style: {
          ...edge.style,
          strokeWidth: isConnected ? 3 : 1,
          opacity: isConnected ? 1 : 0.15,
        },
      };
    })
  );
};

const handlePaneClick = () => {
  setSelectedNode(null);

  setNodes((currentNodes) =>
    currentNodes.map((node) => ({
      ...node,
      style: {
        ...node.style,
        opacity: 1,
      },
    }))
  );

  setEdges((currentEdges) =>
    currentEdges.map((edge) => ({
      ...edge,
      animated: false,
      style: {
        ...edge.style,
        strokeWidth: 1.5,
        opacity: 1,
      },
    }))
  );
};

  const selectedProperties =
  selectedNode?.data?.original?.properties || {};

const selectedLabels =
  selectedNode?.data?.original?.labels || [];

const selectedType =
  selectedLabels.find((label) =>
    [
      'Developer',
      'Company',
      'Project',
      'Skill',
      'Technology',
      'Certification',
      'Location',
    ].includes(label)
  ) || 'Node';

const summary = selectedNode
  ? `Selected ${selectedNode.data.label}`
  : searchQuery
  ? `Showing graph relationships for "${searchQuery}"`
  : 'Search for a developer, company, skill, project, or technology';
  
  return (
    <div className="space-y-8">
      <SectionCard
        title="Graph explorer"
        subtitle="Search the live graph and explore connected developers, companies, projects, skills, and technologies."
      >
        {/* SEARCH */}
        <div className="mb-6 flex gap-3">
          <div className="flex flex-1 items-center gap-3 rounded-2xl border border-white/10 bg-slate-950/50 px-4 py-3">
            <FiSearch className="text-slate-400" />

            <input
              value={searchInput}
              onChange={(event) =>
                setSearchInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Search developer name, email, skill, company..."
              className="w-full bg-transparent text-white outline-none placeholder:text-slate-500"
            />
          </div>

        <button
      type="button"
      onClick={handleSearch}
      disabled={!searchInput.trim() || isLoading}
      className="rounded-2xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {isLoading ? 'Searching graph...' : 'Search graph'}
    </button>

        </div>

        {/* ERROR */}
        {isError && (
          <div className="mb-6 rounded-2xl border border-rose-400/20 bg-rose-500/10 p-4 text-rose-200">
            Unable to load the graph.
            <div className="mt-1 text-xs text-rose-300/70">
              {error?.response?.data?.details ||
                error?.message ||
                'Unknown error'}
            </div>
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
                {/* GRAPH */}
      <div className="h-[560px] rounded-3xl border border-white/10 bg-slate-950/40 p-2">
        {isLoading ? (
          <div className="flex h-full items-center justify-center text-center">
            <div>
              <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-cyan-400/20 border-t-cyan-400" />

              <div className="mt-4 text-lg font-semibold text-white">
                Exploring graph...
              </div>

              <p className="mt-2 text-sm text-slate-400">
                Finding connected developers, companies, skills, and projects.
              </p>
            </div>
          </div>
        ) : searchQuery && graphData.nodes.length === 0 ? (
          <div className="flex h-full items-center justify-center text-center">
            <div>
              <div className="text-lg font-semibold text-white">
                No graph data found
              </div>

              <p className="mt-2 text-sm text-slate-400">
                Try a developer name such as Apeksha,
                an email, company, skill, or project.
              </p>
            </div>
          </div>
        ) : !searchQuery ? (
          <div className="flex h-full items-center justify-center text-center">
            <div>
              <div className="text-lg font-semibold text-white">
                Search the graph
              </div>

              <p className="mt-2 text-sm text-slate-400">
                Enter a developer name and click Search.
                The static placeholder graph has been replaced
                with live graph data.
              </p>
            </div>
          </div>
        ) : (
          <ReactFlow
            key={searchQuery}
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={handleNodeClick}
            fitView
            fitViewOptions={{
              padding: 0.2,
            }}
          >
            <MiniMap
              nodeStrokeColor="#94a3b8"
              nodeColor="#0f172a"
            />

            <Controls />

            <Background
              gap={16}
              color="#ffffff20"
            />
          </ReactFlow>
        )}
      </div>

      {/* INSIGHTS */}
          <div className="rounded-3xl border border-white/10 bg-slate-950/40 p-6">
            <h4 className="text-white">
              Graph insights
            </h4>

            <p className="mt-3 text-sm leading-6 text-slate-400">
              {summary}
            </p>
            {selectedNode && (
  <div className="mt-5 rounded-2xl border border-cyan-400/20 bg-cyan-500/5 p-4">
    <div className="text-xs font-semibold uppercase tracking-wider text-cyan-300">
      {selectedType}
    </div>

    <div className="mt-2 text-lg font-semibold text-white">
      {selectedNode.data.label}
    </div>

    <div className="mt-4 space-y-2">
      {Object.entries(selectedProperties)
        .filter(([key]) => key !== 'embedding')
        .slice(0, 8)
        .map(([key, value]) => (
          <div
            key={key}
            className="flex items-start justify-between gap-4 border-b border-white/5 py-2 last:border-0"
          >
            <span className="text-xs text-slate-500">
              {key}
            </span>

            <span className="text-right text-xs text-slate-300">
              {String(value)}
            </span>
          </div>
        ))}
    </div>
  </div>
)}

            {searchQuery && (
              <div className="mt-6 grid grid-cols-2 gap-3">
                <div className="rounded-2xl bg-white/5 p-4">
                  <div className="text-2xl font-bold text-cyan-300">
                    {nodes.length}
                  </div>
                  <div className="text-xs text-slate-400">
                    Nodes
                  </div>
                </div>

                <div className="rounded-2xl bg-white/5 p-4">
                  <div className="text-2xl font-bold text-violet-300">
                    {edges.length}
                  </div>
                  <div className="text-xs text-slate-400">
                    Relationships
                  </div>
                </div>
              </div>
            )}

            <div className="mt-6 space-y-3 text-sm text-slate-300">
              <div className="rounded-2xl bg-white/5 px-4 py-3">
                Search results come from the live backend graph.
              </div>

              <div className="rounded-2xl bg-white/5 px-4 py-3">
                Click any node to inspect it.
              </div>

              <div className="rounded-2xl bg-white/5 px-4 py-3">
                Relationships show their actual graph relationship type.
              </div>
            </div>
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
