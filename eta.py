import util3 as util
import heritage3

#number of columns >= num of rows (because mirroring)

#for square
#G MUST BE SQUARE OR IT BREAK
def eta(g, l, etaG, n, Nxn):

	#rank(g) < n-1 and file(g) < n-1
	if util.rank(g) < n-1 and util.file(g) < n-1:
		#if g = correct first move for a bite
		if g[0] == n and eta[1:] == [1]*(n-1):
			if l == (n-1, n-1):
				return 2*n-2
			elif l == (n, n-1):
				return 2*n-3
			else:
				print("This should not have happend - eta case 1")
		#bite at winning square move then calc remaining moves
		else:
			#if l doesn't extend into first col or top row
			if l[0] < n and l[1] < n:
				return 2*n-1
			#turned into a rectangle board
			#if l[1] = n then l[0] = n which isn't in L therefore this is for l[0] = n
			#l[0] = n
			else:
				#getLPrime is adding a col to the right
				#getLPrime shouldn't return a full L
				return etaPrime(g, util.getLPrime(g), etaG, NXn)

#for not square, only called by eta
def etaPrime(gP, lP, etaGP, NXn):
	return etaGraph(combineGP_LP(gP, lP), NXn)

def etaGraph(node, NXn):
	"""
	get children of node,
	init num = 0
	for child:
		if childNum + 1 is odd:
			if childNum > num:
				num = childNum
		elif childNum + 1 is even and num is even and childNum > num:
			num = childNum
	"""

	children = heritage3.getChildren(node)
	num = 0

	for child in children:
		cNum = NXn[util.dKey(child)]
		#odd
		if (cNum + 1) % 2 == 1:
			if num % 2 == 0 or cNum > num:
				num = cNum
		#even
		elif cNum > num:
			num = cNum
	return num
