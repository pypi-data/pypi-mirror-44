from rb.comprehension.utils.graph.cm_node_do import CmNodeDO
from rb.comprehension.utils.graph.cm_edge_do import CmEdgeDO
from rb.comprehension.utils.graph.cm_node_type import CmNodeType
from copy import deepcopy
from typing import List, Dict
from spacy.language import Language
Nodes = List[CmNodeDO]
Edges = List[CmEdgeDO]


class CmGraphDO:
    
    def __init__(self) -> None:
        self.node_list = [] 
        self.edge_list = []


    def __init__(self, node_list: Nodes, edge_list: Edges) -> None:
        self.node_list = node_list
        self.edge_list = edge_list


    def contains_node(self, node: CmNodeDO) -> bool:
        return node in self.node_list

    
    def contains_edge(self, edge: CmEdgeDO) -> bool:
        return edge in self.edge_list


    def get_node(self, node: CmNodeDO) -> CmNodeDO:
        for in_node in self.node_list:
            if in_node == node:
                return in_node
        return None

    def get_edge(self, edge: CmEdgeDO) -> CmEdgeDO:
        for in_edge in self.edge_list:
            if in_edge == edge:
                return in_edge
        return None


    def remove_node_links(self, node: CmNodeDO) -> None:
        if not self.contains_node(node):
            return

        graph_node = self.get_node(node)
        
        node_edges = []
        for edge in self.edge_list:
            if edge.get_opposite_node(graph_node):
                node_edges.append(edge)

        for edge in node_edges:
            self.edge_list.remove(edge)


    def add_node_or_update(self, node: CmNodeDO) -> None:
        if not self.contains_node(node):
            self.node_list.append(node)
            return

        graph_node = self.get_node(node)
        graph_node.activation_score += node.activation_score
        graph_node.deactivate()
        if node.is_active():
            graph_node.activate()

        # if the other node is inferred we keep the graph node as it is
        if node.node_type == CmNodeType.TextBased:
            graph_node.node_type = CmNodeType.TextBased


    def add_edge_or_update(self, edge: CmEdgeDO) -> None:
        if not self.contains_edge(edge):
            self.edge_list.append(edge)
            return

        graph_edge = self.get_edge(edge)
        graph_edge.deactivate()
        if edge.is_active():
            graph_edge.activate()


    def get_edges_for_node(node: CmNodeDO) -> Edges:
        edges = []
        for edge in self.edge_list:
            if edge.node1 == node or edge.node2 == node:
                edges.append(edge)
        return edges


    def get_activate_edges_for_node(node: CmNodeDO) -> Edges:
        edges = self.get_edges_for_node(node)
        active_edges = []
        for edge in edges:
            if edge.is_active():
                active_edges.append(edge)
        return active_edges


    def restrict_active_nodes(max_active_concepts: int) -> None:
        self.node_list.sort(key=lambda x: x.activation_score, reverse=True)

        partial_node_list = self.node_list[max_active_concepts:]

        for node in partial_node_list:
            if node.is_active():
                node.deactivate()
                node_edges = self.get_edges_for_node(node)
                for edge in node_edges:
                    edge.deactivate()


    def set_node_list(self, node_list: Nodes) -> None:
        self.node_list = node_list


    def set_edge_list(self, edge_list: Nodes) -> None:
        self.edge_list = edge_list


    def combine_links_from_graph(self, other_graph: CmGraphDO) -> None:
        for edge in other_graph.edge_list:
            if not self.contains_edge(edge):
                self.add_node_or_update(edge.node1)
                self.add_node_or_update(edge.node2)
                self.add_edge_or_update(edge)

    
    def combine_with_syntactic_links(syntactic_graph: CmGraphDO,
            semantic_model: Language, max_dictionary_expansion: int) -> None:



    def get_combined_graph(self, other_graph: CmGraphDO) -> CmGraphDO:
        new_node_list = deepcopy(self.node_list)
        for node in other_graph.node_list:
            if node not in new_node_list:
                new_node_list.append(node)

        new_edge_list = deepcopy(self.edge_list)
        for edge in other_graph.edge_list:
            if edge not in new_edge_list:
                new_edge_list.append(edge)

        graph = CmGraphDO(new_node_list, new_edge_list)
        return graph

    
    def get_activation_map(self) -> Dict:
        activation_map = {}
        for node in self.node_list:
            activation_map[node] = node.activation_score
        return activation_map


    def __repr__(self):
        return str(self.node_list) + '\n' + str(self.edge_list)


    def __str__(self):
        return str(self.node_list) + '\n' + str(self.edge_list)

