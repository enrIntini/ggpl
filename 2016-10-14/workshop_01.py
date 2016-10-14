from pyplasm import *

def out ():

	x = QUOTE([.1,-.3]*5)
	#xa = QUOTE([2.6])
	xa = QUOTE([.8,-.15]*5)
	a = PROD([x, xa])
	
	ya = QUOTE([-.8,.15]*5)
	y = QUOTE([1.7])
	#y = QUOTE([-.1,.3]*5)
	b = PROD([y, ya])
	
	ab = STRUCT([a,b])
	z = QUOTE([.5])
	abc = PROD([z, ab])

	
	return abc

def out2(px, py, bx, bz, dpDato, dbDato, beamPriority):

	dp = [py]
	for val in dpDato:
		dp.append(-val+bz)
		dp.append(py)
	db = []
	for val in dbDato:
		db.append(-val+py)
		db.append(bz)

	dpn = []
	dbn = []

	dbSum = 0
	for val in db:
		dbSum += abs(val)
		dbn.append(-val)
		
	dpSum = 0
	for val in dp:
		dpSum += abs(val)
		dpn.append(-val)
		
	x = QUOTE(dp)
	if beamPriority:
		xa = QUOTE(dbn)
	else: 
		xa = QUOTE([dbSum])
	a = PROD([x, xa])
	
	ya = QUOTE(db)
	if beamPriority:
		y = QUOTE([dpSum])
	else: 
		y = QUOTE(dpn)
	
	b = PROD([y, ya])
	
	ab = STRUCT([a,b])
	za = QUOTE([px])
	zb = QUOTE([bx])
	#abc = PROD([z, ab])
	abc = STRUCT([T(1)(-px/2), PROD([za, a]), T(1)(-(bx-px)/2),PROD([zb,b])])

	return abc
dpDato = [1.3, 1.5, 1.7]
dbDato = [1.8, 1.8, 1.8]
px = 0.2
bx = 0.5
py = 0.3
bz = 0.4

result = out2(px, py, bx, bz, dpDato, dbDato, TRUE) 
VIEW(result)