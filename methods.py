import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm

# Basic statistic
def calc_basic_metrics(G):
    # return number of nodes, number of edges, average degree, density
    n = G.number_of_nodes()
    m = G.number_of_edges()
    avg_deg = m /n
    density = m/n/(n-1)
    print("Nr. of nodes: ", n)
    print("Nr. of edges: ", m)
    print("Average degree: ", avg_deg)
    print("Density: ", density)
    return n, m,avg_deg, density


# OUT - degree distribution
def get_outdegree_distr(G, n_bins: int = 100):
    nr_of_nodes = G.number_of_nodes()
    degree_seq = [deg for _, deg in G.out_degree(weight='weight')]

    min_degree = min(degree_seq)
    max_degree = max(degree_seq)

    distr = dict()
    for degree in degree_seq:
        bin = int(((degree-min_degree)*n_bins) / (max_degree-min_degree))
        distr[bin] = distr[bin] + 1 if bin in distr else 1

    for (k, v) in distr.items():
        distr[k] = v / nr_of_nodes

    return distr


# IN - degree distribution
def get_indegree_distr(G, n_bins: int = 100):
    nr_of_nodes = G.number_of_nodes()
    degree_seq = [deg for _, deg in G.in_degree(weight='weight')]
    
    min_degree = min(degree_seq)
    max_degree = max(degree_seq)

    distr = dict()
    for degree in degree_seq:
        bin = int(((degree-min_degree)*n_bins) / (max_degree-min_degree))
        distr[bin] = distr[bin] + 1 if bin in distr else 1

    for (k, v) in distr.items():
        distr[k] = v / nr_of_nodes
    
    return distr


def show_deg_distr(G, n_bins: int = 100):
    distrib_out, distrib_in = get_outdegree_distr(G, n_bins=n_bins), get_indegree_distr(G, n_bins=n_bins)
    plt.figure(figsize=(10,8), dpi=150)

    plt.loglog(distrib_out.keys(), distrib_out.values(), 'o', alpha=0.5, markersize=4, label='Out-Degree')
    plt.loglog(distrib_in.keys(), distrib_in.values(), 'o', alpha=0.5, markersize=4, label='In-Degree')

    plt.title('Weighted degree distribution plotted on log–log graph')
    plt.xlabel('Bin Number')
    plt.ylabel('Weighted Degree distributions')
    plt.legend()

    plt.savefig('degree_dist.png', bbox_inches='tight')
    
def is_weakly_conn(G):
    weakly_conn = nx.is_weakly_connected(G)
    #print("Weakly connected: ", weakly_conn) # pomoje ns sam to zanima
    #strongly_conn = nx.is_strongly_connected(G)
    #print("Strongly connected: ", strongly_conn)
    #nr_strongly_conn = nx.number_strongly_connected_components(G)
    #print("Nr. of strongly conn. comp.: ", nr_strongly_conn)
    return weakly_conn

def clustering_coef(G):
    clust_coeff = nx.clustering(G, weight='weight')
    avg_clust_coeff = nx.average_clustering(G, weight='weight')
    print("Average clustering coeficient: ", avg_clust_coeff)
    return clust_coeff, avg_clust_coeff

def weighted_centr_measures(G):
    # BETWEEENES
    betweenes = nx.betweenness_centrality(G, weight='distance', normalized=True)
    betweenes_sorted = list(map(lambda x: (x, str(betweenes[x])), sorted(betweenes, key= lambda x: float(betweenes[x]), reverse=True)))
    #print("Betweenes centrality: ", betweenes_sorted)
    
    # CLOSENES
    clossenes = nx.closeness_centrality(G, distance='distance')
    clossenes_sorted =  list(map(lambda x: (x, str(clossenes[x])), sorted(clossenes, key= lambda x: float(clossenes[x]) , reverse=True))) 
    #print("Clossenes centrality: ", clossenes_sorted)

    # DEGREE (IN and OUT)
    in_degrees = G.in_degree(weight='weight')
    out_degrees = G.out_degree(weight='weight')
    max_in_degree = max(list(in_degrees), key=lambda x: x[1])
    max_out_degree = max(list(out_degrees))
    in_degree_centrality = list(map(lambda x: (x[0], x[1]/max_in_degree[1]), list(in_degrees)))
    out_degree_centrality = list(map(lambda x: (x[0], x[1]/max_in_degree[1]), list(out_degrees)))
    #print("In_degree_centraity: ", in_degree_centrality)
    #print("Out_degree_centrality: ", out_degree_centrality)
   
    return betweenes, clossenes, in_degree_centrality, out_degree_centrality
    
# MODULARITY oz. community detection
# LOUVAIN https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html#networkx.algorithms.community.louvain.louvain_communities
def louvain_community(G):
    return nx_comm.louvain_communities(G, weight='weight')