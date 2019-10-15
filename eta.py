import util3 as util
import heritage3

#number of columns >= num of rows (because mirroring)

#for square
#G MUST BE SQUARE OR IT BREAK
def eta(g, l, etaG, n, NXn):
	#print("\n\neta for g: "+str(g)+" l: "+str(l))
	#rank(g) < n-1 and file(g) < n-1
	#first part for if square
	if g[0] == len(g)  and util.rank(g) < n-1 and util.file(g) < n-1:
		#if g = correct first move for a bite
		if g[0] == n-1 and len(g) > 1 and g[1] == 1:
			#print("SQUARE bite detected for " + str(g))
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
				#l[1] was util.getLPrime(g)
				return etaPrime(g, l[1]-1, etaG, NXn)
	else:
		#print("wants to be elsa")
		return etaPrime(g, l[1]-(n-len(g)), etaG, NXn)

#for not square, only called by eta
def etaPrime(gP, lP, etaGP, NXn):
	#print("etaPrime gP: " + str(gP)+"\tlP: " + str(lP))
	if etaGP % 2 == 0:
		return etaGP + 1
	N = util.combineGP_LP(gP, lP)
	#print("etaPrime N: "+str(N))
	return etaGraph(N, NXn)

# @profile
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
	#print("children: " + str(children))

	num = 0
	#print(NXn)
	for child in children:

		if util.getN(child) >= util.getM(child):
		# if child[0] >= len(child):
			cNum = NXn[str(child)]
		else:
			mir = util.mirror(child)
			cNum = NXn[str(mir)]

		#print("child: " +str(child)+"\tcNum: " + str(cNum))

		#odd
		if (cNum + 1) % 2 == 1:
			num = cNum+1
		#even
		elif num % 2 == 0 and (cNum+1) > num:
			num = cNum+1
	return num
