import sys
import numpy as np
import pandas as pd
import itertools
from functools import reduce
np.set_printoptions(precision=3)

class Table(object):
    def __init__(self, matrix, nodes):
        """
        matrix is an {MxMx...} matrix, with # dimensions equal to the # of nodes
        nodes is a (sorted) list of the nodes on the edge
        """
        self.matrix = matrix
        self.nodes = nodes
    def fetch(self, idx):
        """
        idx is a dict of (node: nodestate) that we want to use to fetch a value
        from our matrix. We will only have 2 of them.
        If we don't have both nodes, then we return 1
        """
        # fetch node names
        nodes = idx.keys()
        ours = set(nodes).intersection(self.nodes)
        ours = sorted(list(ours))
        if len(ours) != len(self.nodes):
            return 1
        return self.matrix[tuple([idx[i] for i in ours])]
    def marginalize(self, target):
        """
        Sum over all dimensions that aren't the dimension of [target]
        Target is a tuple of nodes
        """
        res = self.matrix
        num = 0
        for idx, node in enumerate(self.nodes):
            if node in target: continue
            res = np.sum(res, axis=idx-num)
            num += 1
        return res / np.sum(res)


def multiply_edge(e1,e2):
    """
    Multiplies 2 tables together, as part of a graph factorization.
    Returns a new edge with nodes = set(e1.nodes).union(set(e2.nodes)), and matrix
    with dimensions equal to the number of nodes in the new set
    """
    nodes = list(set(e1.nodes).union(set(e2.nodes)))
    states = itertools.product([0,1],repeat=len(nodes))
    result = np.zeros([2]*len(nodes))
    for state in states:
        # creates a list of (node, nodestate) for indexing into an edge and
        # retrieving the probability
        idx = dict(zip(nodes, state))
        result[(state)] = e1.fetch(idx) * e2.fetch(idx)
    return Table(result, nodes)

class Graph(object):
    def __init__(self, data, edges):
        self.data = data
        self.edges = edges

    def compute_factorization(self):
        return reduce(multiply_edge, self.edges)

    def get_empirical_marginals(self, nodelist):
        """
        nodelist is a list of numbers (i,j,k...) that we want to get the joint empirical distribution of
        df is a DataFrame w/ column names = the node names, and each column is a set of samples

        Result is a MxM matrix where M is the number of states

        Right now, assume binary variables
        """
        df = self.data
        # create the {MxMx...} matrix; the dimensionality is equal to the number of nodes in the list
        result = np.zeros([2]*len(nodelist))
        # create the list of all possible binary states of the N nodes
        states = itertools.product([0,1],repeat=len(nodelist))
        # for each of these states
        for state in states:
            # create the list of conditions (e.g. a selector into the dataframe that retrieves the rows where the state is true)
            # for example, each state is something like (0,1,0); for a nodelist of (1,2,3), we create a list of
            # (df[1] == 0) & (df[2] == 1) & (df[3] == 0). The creation of the list is done by this line; the compositiion
            # of these statements into a single condition is the next line
            cond = [(df[node] == val) for node, val in zip(nodelist, state)]
            # combine the states into a single condition
            cond = np.bitwise_and.reduce(cond)
            # df[cond].count() returns the number of rows that match all conditions
            avg = (df[cond].count() / df.count())[1]
            # assign into the matrix
            result[state] = avg
        return result

    def update_model_params(self, edge, matrix):
        """
        Updates the compat matrix for the given edge
        edge is a list of nodes (i,j,...)
        matrix is an {MxM...} matrix
        """
        for idx, e in enumerate(self.edges):
            if e == edge:
                self.edges[idx] = matrix
                break

    def get_compat_for_edge(self, edge):
        """
        edge is a list of nodes (i,j,...)
        Returns the matrix for the corresponding edge
        """
        for e in self.edges:
            if e == edge:
                return e

    def dump(self):
        res = ""
        for e in self.edges:
            res += '\nEdge {0} => {1}'.format(e.nodes, str(e.matrix).replace('\n','\n\t\t'))
        return res

    def compute_likelihood(self):
        empiricals = self.get_empirical_marginals(list(self.data.columns))
        factor = self.compute_factorization()
        print empiricals.flatten()
        print factor.matrix.flatten()
        return np.inner(empiricals.flatten(), factor.matrix.flatten())

    def compute_likelihood_edges(self):
        factor = self.compute_factorization()
        likelihood = 0
        for row in self.data.itertuples():
            row = np.array(row[1:]) # skip the first entry because its the index
            likelihood += factor.matrix[tuple(row)]
        return likelihood

def run(data, edges):
    G = Graph(data, edges)
    old = ""
    for i in range(1,100):
        for edge in G.edges:
            empirical_mean = G.get_empirical_marginals(edge.nodes)
            factor = G.compute_factorization()
            model_mean = factor.marginalize(edge.nodes)
            old_compat = G.get_compat_for_edge(edge)
            proportion = np.divide(empirical_mean, model_mean)
            new = np.multiply(old_compat.matrix, proportion)
            #new = new / np.sum(new) # re-normalize
            G.update_model_params(edge, Table(new, edge.nodes))
        new = G.dump()
        if new == old:
            print '-'*5,'run',i,'-'*5
            print new
            print G.compute_likelihood()
            break
        else:
            old = new

data = np.recfromtxt('idea1.csv')
data = pd.DataFrame.from_records(data)
print data
sys.exit(1)
#data.columns = [1,2,3,4] # rename columns

psi = np.matrix([[1,1],[1,1]])

#### (i) ####
print "\n","#"*5,"(i)","#"*5
e12 = Table(psi, (1,2))
e23 = Table(psi, (2,3))
e34 = Table(psi, (3,4))
e14 = Table(psi, (1,4))
edges = [e12,e23,e34,e14]
run(data, edges)

#### (ii) ####
print "\n","#"*5,"(ii)","#"*5
e12 = Table(psi, (1,2))
e23 = Table(psi, (2,3))
e13 = Table(psi, (1,3))
e14 = Table(psi, (1,4))
edges = [e12,e23,e13,e14]
run(data, edges)

#### (iii) ####
print "\n","#"*5,"(iii)","#"*5
e12 = Table(psi, (1,2))
e13 = Table(psi, (1,3))
e14 = Table(psi, (1,4))
e23 = Table(psi, (2,3))
e24 = Table(psi, (2,4))
e34 = Table(psi, (3,4))
edges = [e12,e13,e14,e23,e24,e34]
run(data, edges)
