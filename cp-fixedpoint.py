import beliefprop as bp
import networkx as nx
import scipy.sparse as sp
import scipy.sparse.linalg as lin
import numpy as np
import matplotlib.pyplot as plt

n_c = 50
n_p = 50
p_cc = .6
p_cp = .3
p_pp = .2
'''
p_cc = 1
p_cp = .5
p_pp = 0
'''

G = nx.Graph(bp.make_graph(n_c, n_p, p_cc, p_cp, p_pp))

def leading_hashimoto(G):
  A = nx.to_scipy_sparse_matrix(G, dtype='d')
  I = sp.identity(A.shape[0])
  I_minus_D = sp.lil_matrix(A.shape)
  for node,deg in G.degree_iter():
    I_minus_D[node,node] = 1.0-deg
  crazy = sp.bmat([[None,I],[I_minus_D,A]])
  eig = lin.eigs(crazy,k=1,which="LR")
  return list(eig[1][:,0].real)[(len(eig[1])/2):]

perturbation = leading_hashimoto(G)

gamma = [n_c/float(n_c+n_p),n_p/float(n_c+n_p)]
omega = [[p_cc, p_cp],[p_cp, p_pp]]
sym_omega = [[.45,.5],[.5,.5]]

A = np.array(nx.adjacency_matrix(G))
#phi,gamma,omega,messages = bp.linear_expansion(gamma,omega,A,perturbation)
#ass,phi,messages = bp.bp_find_zeros(gamma,omega,A,300)
ass,phi,gamma, omega, messages = bp.bp(gamma,sym_omega,A,10)

#print perturbation
#print phi
print "messages"
#print phi
#print omega
#print messages
nx.draw(G)
plt.show()
