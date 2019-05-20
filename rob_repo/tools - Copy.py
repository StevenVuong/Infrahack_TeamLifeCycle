import numpy as np

def toAsubAval(matrix):
	T = len(matrix[0])
	asub = [[] for x in range(T)]
	aval = [[] for x in range(T)]
	nonZeros = np.nonzero(matrix)
	for k, pos in enumerate(nonZeros[0]):
		asub[nonZeros[1][k]] += [pos]
		aval[nonZeros[1][k]] += [1]
	return asub, aval