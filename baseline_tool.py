"""
Problem Statement:
    The previous anomaly visualizer aimed to provide a hierarchical visualization of data, 
    enabling the analysis of hierarchical relationships between data attributes.
Current Method:
    The anomaly visualizer functioned by recursively generating nodes and edges based on the 
    distinct values of each column in the dataset. 
    It considered parameters such as the distinct value limit, default node color, 
    and the total count of unique values in each column. 
    The visualization included dynamic node sizes and colors based on the weight of each node, 
    representing the percentage of samples associated with that node. 
    The final visualization depicted a river flow metaphor, showcasing the hierarchical structure of the data.
Concept:
    The script utilized the NetworkX and Matplotlib libraries to generate the hierarchical visualization. 
    It provided flexibility in adjusting distinct value limits and default colors, 
    allowing users to customize the visualization according to their requirements. 
    The visualization process involved recursive node generation based on the distinct values of each column, 
    ensuring a comprehensive representation of the data hierarchy.
"""
__author__ = "Sryborg"
__status__ = "Dev"

##############################################################################################
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import argparse

class AnomalyVisualizer():
    def __init__(self, args):
        self.graph = nx.DiGraph()
        self.distinct_value_limit = args.distinct_value_limit
        self.default_color = args.default_color
        self.save_analysis = args.save_analysis
    
    def find_pos(self, total_cols, node_seq, each_col, count_dict, base_node, last_x, last_y):
        scaling = total_cols-last_x
        previous_node_pos = base_node[1]['pos']
        max_slots = count_dict[each_col]
        available_slots = previous_node_pos[0]*max_slots
        last_y += available_slots+(node_seq*scaling)
        if previous_node_pos[1]<0 or node_seq%2:
            last_y = last_y*(-1)
        else:
            last_y = last_y+0.5
        if node_seq%2:
            last_x = last_x+0.5
        return last_x, last_y

    def recursive_node_gen(self, count_dict, the_dataframe, one_col, nodes=[('root', {'pos': (0, 0), 'weight':500})], \
        edges=[], base_edge="root", base_node=('root', {'pos': (0, 0), 'weight':300}), last_x=0, last_y=0):
        
        cols_list = list(the_dataframe.columns)
        last_y = 0
        for each_col in cols_list:
            last_x += 1
            values_dict = dict(the_dataframe[one_col].value_counts().sort_values())
            if len(values_dict.keys()) < self.distinct_value_limit:
                sum_of_vals = sum(values_dict.values())
                for node_seq, (each_key, each_val) in enumerate(values_dict.items()):
                    last_x, last_y = self.find_pos(len(cols_list), node_seq, each_col, count_dict, base_node=base_node, last_x=last_x, last_y=last_y)
                    node_name = f"{each_col}_{each_key}={each_val}"
                    base_node = (node_name, {'pos':(last_x, last_y), 'weight':float(each_val*100/sum_of_vals)})
                    edges.append( (base_edge, node_name) )
                    nodes.append( base_node )
                    subset_df = the_dataframe[the_dataframe[each_col]==each_key]
                    subset_df = subset_df.drop(each_col, axis=1)
                    if len(subset_df.columns) >= 1:
                        nodes, edges = self.recursive_node_gen(count_dict, subset_df, subset_df.columns[0], \
                        nodes, edges, base_edge=node_name, base_node=base_node, last_x=last_x, last_y=last_y)
                break
            else:
                raise ValueError(f"Too mant distinct values in {each_col} column. Please consider removing it from analysis or adjust distinct value limit.")
                
        return nodes, edges

    def count_total_unique_values(self, the_dataframe):
        count_dict = {}
        max_count = 0
        for each_col in the_dataframe.columns:
            curr_count = len(the_dataframe[each_col].value_counts())
            count_dict[each_col] = curr_count
            if curr_count > max_count:
                max_count = curr_count
        count_dict["max_count"] = max_count
        return count_dict

    def anomaly_visualizer(self, the_dataframe, features_to_track=[]):
        if features_to_track:
            the_dataframe = the_dataframe[features_to_track]
        count_dict = self.count_total_unique_values(the_dataframe)
        nodes, edges = self.recursive_node_gen(count_dict, the_dataframe, the_dataframe.columns[0])
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

        node_pos = {node: data['pos'] for node, data in self.graph.nodes(data=True)}
        node_weights = nx.get_node_attributes(self.graph, 'weight')
        node_weights = [node_weights[node] * 100 for node in self.graph.nodes()]
        node_colors = ['red' if self.graph.nodes[node]['weight'] < 5 else self.default_color for node in self.graph.nodes()]
        plt.figure(figsize=(50, 40))
        nx.draw(self.graph, pos=node_pos, with_labels=True, node_size=node_weights, node_color=node_colors, font_size=10, font_weight='bold')
        plt.title('River Flow Metaphor')
        if self.save_analysis:
            plt.savefig('visualization.png')
        else:
            plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Anomaly Visualizer - Visualize hierarchical data.')
    parser.add_argument('--data_path', type=str, help='Please provide the path to your data CSV.')
    parser.add_argument('--distinct_value_limit', type=int, default=15, help='Distinct value limit for each column (default: 15)')
    parser.add_argument('--default_color', type=str, default='lightblue', help='Default color for nodes (default: lightblue)')
    parser.add_argument('--save_analysis', type=bool, default=False, help='Flag to be set if you want to save your analysis (default: False)')
    args = parser.parse_args()
    big_df = pd.read_csv(args.data_path)
    big_df.fillna('0')
    av_obj = AnomalyVisualizer(args)
    av_obj.anomaly_visualizer(big_df)