# graph_analysis.py
import networkx as nx

class GraphEngine:
    def __init__(self):
        self.G = nx.DiGraph()
        self.node_meta = {}

    def add_node(self, node_id: str, text: str, meta: dict):
        self.G.add_node(node_id)
        self.node_meta[node_id] = {'text': text, 'meta': meta}

    def add_edge(self, src: str, dst: str):
        self.G.add_edge(src, dst)

    def summary(self):
        num_nodes = self.G.number_of_nodes()
        num_edges = self.G.number_of_edges()
        degree = dict(self.G.degree())
        top = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]
        return {'nodes': num_nodes, 'edges': num_edges, 'top_degree': top}

    def find_coordinated_clusters(self):
        scc = list(nx.strongly_connected_components(self.G))
        clusters = [list(c) for c in scc if len(c) > 2]
        return clusters

    def compute_centrality(self):
        return nx.betweenness_centrality(self.G)
