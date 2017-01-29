from pyplasm import *
import csv

def window(X,Y,Z,occupancy):
    def door0(dx,dy,dz):
        def door1(cod):
            
            scX = 0
            scY = 0
            scZ = 0
            for el in X:
                scX += el
            for el in Y:
                scY += el
            for el in Z:
                scZ += el
            scX = dx/scX
            scY = dy/scY
            scZ = dz/scZ
            
            structure = CUBOID([0,0,0])
            ix = 0
            sommaX = 0
            
            for piano in occupancy:
                page = CUBOID([0,0,0])
                iz = 0
                sommaZ = 0
                
                for riga in piano:
                    tmp = []
                    iy = 0
                    tuttiNegativi = 1

                    for val in riga:
                        if val == cod: 
                            tmp.append(Y[iy]*scY)
                            tuttiNegativi = 0
                        else: tmp.append(-Y[iy]*scY)

                        iy += 1

                    if tuttiNegativi == 0:
                        #1d
                        qy = QUOTE(tmp)
                        #2d
                        rxy = PROD([QUOTE([X[ix]*scX]), qy])
                        #ryz = PROD([qy, QUOTE([Z[iz]])])
                        #3d
                        row = PROD([rxy, QUOTE([Z[iz]*scZ])])
                        #unisco le righe
                        page = STRUCT([page, T(3)(sommaZ), row])

                    sommaZ += Z[iz]*scZ
                    iz += 1

                structure = STRUCT([structure, T(1)(sommaX), page])
                sommaX += X[ix]*scX
                ix += 1

            return structure
         #vetro
        ambient = [0,0,0,1]
        diffuse = [0.588235, 0.670588, 0.729412, .65]
        specular = [.9,.9,.9,1]
        emission = [ 0,0,0,1]
        shininess = [96]
        
        cGlass = [210.0/255, 1.0, 1.0]
        cFrame = [80.0/255, 40.0/255, .0/255]
        frame = COLOR(cFrame)(door1(1))
        glass = MATERIAL(ambient+diffuse+specular+emission+shininess)(door1(2))
        
        return STRUCT([T([1,2])([-dx/2, -dy/2]),frame,glass])

    return door0

#ogni elemento delle righe di occ si riferisce alle y
occ1 = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]
occ2 = [[1,1,1,1,1],[1,0,1,0,1],[1,0,1,0,1],[1,0,1,0,1],[1,1,1,1,1]]
occ3 = [[1,1,1,1,1],[0,2,1,2,0],[0,2,1,2,0],[0,2,1,2,0],[1,1,1,1,1]]
occ4 = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]
occ = [occ1, occ2,occ3, occ4]

def muriEsterni():
    j = 0
    with open ('esterni.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 0:
                    mura = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    j = 1
                else:
                    mura = STRUCT([mura, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
    mura = OFFSET([0.4, 0.4, 3])(mura)
    return mura
#VIEW(mura)

def muriInterni(mura):
    j = 0
    with open ('interni.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 0:
                    muriInterni = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    j = 1
                else:
                    muriInterni = STRUCT([muriInterni, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
    muriInterni = OFFSET([.15, .15, 3])(muriInterni)
    #pianta = STRUCT([mura, T(2)(2.7), muriInterni])
    pianta = STRUCT([mura, muriInterni])

    return pianta
	
def porteEsterne(pianta):
    j = 0
    with open ('porte.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 0:
                    porte = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    j = 1
                else:
                    porte = STRUCT([porte, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
    porte = OFFSET([.6, 1, 5])(porte)
    pianta = DIFF([pianta, porte])
    return pianta
	
def finestre(pianta):
    j = 0
    k = 0
    finestreOrizzontali = 0
    finestreVerticali = 0
    with open ('finestre.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 1 and abs(punti[0] - punti[2]) < .05:
                    finestreVerticali = STRUCT([finestreVerticali, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                if j == 0 and abs(punti[0] - punti[2]) < .05:
                    finestreVerticali = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    j = 1

                if k == 1 and abs(punti[1] - punti[3]) < .05:
                    finestreOrizzontali = STRUCT([finestreOrizzontali, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                if k == 0 and abs(punti[1] - punti[3]) < .05:
                    finestreOrizzontali = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    k = 1
    if finestreVerticali:
        finestreVerticali = OFFSET([.8, .01, 1.5])(finestreVerticali)
    if finestreOrizzontali:
        finestreOrizzontali = OFFSET([.01, .8, 1.5])(finestreOrizzontali)
    if finestreOrizzontali and finestreVerticali:
        finestre = STRUCT([finestreVerticali, finestreOrizzontali])
    if finestreOrizzontali and not finestreVerticali:
        finestre = finestreOrizzontali
    if not finestreOrizzontali and finestreVerticali:
        finestre = finestreVerticali
    finestre = STRUCT([T([1,2,3])([-.05, -.05, 1]), finestre])
    #VIEW(STRUCT([pianta, finestre]))
    pianta = DIFF([pianta, finestre])
    return pianta
	
def porteInterne(pianta):
    j = 0
    k = 0
    with open ('porteInterne.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 1 and abs(punti[0] - punti[2]) < .05:
                    porteInterneVerticali = STRUCT([porteInterneVerticali, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                if j == 0 and abs(punti[0] - punti[2]) < .05:
                    porteInterneVerticali = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    j = 1
                if k == 1 and abs(punti[1] - punti[3]) < .05:
                    porteInterneOrizzontali = STRUCT([porteInterneOrizzontali, MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                if k == 0 and abs(punti[1] - punti[3]) < .05:
                    porteInterneOrizzontali = STRUCT([MKPOL([[[punti[0], punti[1], 0], [punti[2], punti[3], 0]],[[1,2]],[[1]]])])
                    k = 1
    porteInterneVerticali = OFFSET([.5, .01, 5])(porteInterneVerticali)
    porteInterneOrizzontali = OFFSET([.01, .5, 5])(porteInterneOrizzontali)
    porteInterne = STRUCT([porteInterneVerticali, porteInterneOrizzontali])
    #porteInterne = STRUCT([T(2)(-.03), porteInterne])
    #VIEW(STRUCT([pianta, porteInterne]))
    pianta = DIFF([pianta, porteInterne])
    return pianta
	
def correzione(pianta):
    a = [194.0, 537.7]
    b = [239.3, 537.7]
    c = [506.9, 535.5]
    d = [552.0, 535.5]
    A = CUBOID([(b[0] - a[0])/20 -.05, 2.0, 5.0])
    C = CUBOID([(d[0] - c[0])/20 -.05, 2.0, 5.0])
    AB = STRUCT([T([1,2])([a[0]/20 +.3, a[1]/20 -2]), A])
    AB = STRUCT([AB, T([1,2])([c[0]/20 + .2, d[1]/20 -2]), C])
    pianta  = DIFF([pianta, AB])
    return pianta

# distinguo le finestre a seconda dell'orientamento
def aggiungiFinestre(pianta):
    j = 0
    k = 0
    with open ('finestre.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)

                #finestre con lunghezza sull'asse x
                if j == 0 and abs(punti[1] - punti[3]) < .05:
                    finestreX = STRUCT([T([1,2,3])([(punti[0]+punti[2])/2, punti[1],1]), R([1,2])(math.pi/2), window([.03,.015,.015,.03],[.1,.3,.05,.3,.1],[.1,.5,.05,.5,.1],occ)(.2, abs(punti[0]-punti[2])+.1, 1.5)])
                    j = 1

                if j == 1 and abs(punti[1] - punti[3]) < .05:
                    finestreX = STRUCT([finestreX, T([1,2,3])([(punti[0]+punti[2])/2, punti[1],1]), R([1,2])(math.pi/2), window([.03,.015,.015,.03],[.1,.3,.05,.3,.1],[.1,.5,.05,.5,.1],occ)(.2, abs(punti[0]-punti[2])+.1, 1.5)])

                    #finestre con lunghezza sull'asse x
                if k == 0 and abs(punti[0] - punti[2]) < .05:
                    finestreY = STRUCT([T([1,2,3])([punti[0], (punti[1]+punti[3])/2, 1]), window([.03,.015,.015,.03],[.1,.3,.05,.3,.1],[.1,.5,.05,.5,.1],occ)(.2, abs(punti[1]-punti[3])+.3, 1.5)])
                    k = 1

                if k == 1 and abs(punti[0] - punti[2]) < .05:
                    finestreY = STRUCT([finestreY, T([1,2,3])([punti[0], (punti[1]+punti[3])/2, 1]), window([.03,.015,.015,.03],[.1,.3,.05,.3,.1],[.1,.5,.05,.5,.1],occ)(.2, abs(punti[1]-punti[3])+.6, 1.5)])

    if j and k:
        finestre= STRUCT([T([1,2])([-.05, .05]), finestreX, finestreY])
    if j and not k:
        finestre= STRUCT([T([1,2])([-.05, .05]), finestreX])
    if not j and k:
        finestre= STRUCT([T([1,2])([.05, .05]), finestreY])
    #VIEW(finestre)
    pianta = STRUCT([pianta, finestre])
    return pianta
	
def portaEsterna(x, y):
    return STRUCT([COLOR([80.0/255, 40.0/255, .0/255])(CUBOID([abs(x)+.1, abs(y), 3.]))])

def portaEsternaV(x, y):
    return STRUCT([COLOR([80.0/255, 40.0/255, .0/255])(CUBOID([abs(x), abs(y)+.1, 3.]))])

def aggiungiPorte(pianta):
    j = 0
    with open ('porte.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 0:
                    if punti[0] > punti[2]:
                        porte = STRUCT([T([1,2])([(punti[2]), punti[1]]), portaEsterna(punti[0]-punti[2]+.5, .04)])
                    else:
                        porte = STRUCT([T([1,2])([(punti[0]), punti[1]]), portaEsterna(punti[0]-punti[2]+.5, .04)])
                    j = 1
                else:
                    if punti[0] > punti[2]:
                        porte = STRUCT([porte, T([1,2])([(punti[2]), punti[1]]), portaEsterna(punti[0]-punti[2]+.5, .04)])
                    else:
                        porte = STRUCT([porte, T([1,2])([(punti[0]), punti[1]]), portaEsterna(punti[0]-punti[2]+.5, .04)])
    porte = STRUCT([T(1)(.05), porte])
    pianta = STRUCT([pianta, porte])
    return pianta
    #VIEW(pianta)
	
def aggiungiPorteInterne(pianta):
    j = 0
    k = 0
    with open ('porteInterne.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if j == 1 and abs(punti[0] - punti[2]) < .05:
                    if punti[1] > punti[3]:
                        porteV = STRUCT([porteV, T([1,2])([(punti[0]), punti[3]]), portaEsternaV(.02, punti[1]-punti[3])])
                    else:
                        porteV = STRUCT([porteV, T([1,2])([(punti[0]), punti[1]]), portaEsternaV(.02, punti[1]-punti[3])])
                if j == 0 and abs(punti[0] - punti[2]) < .05:
                    if punti[1] > punti[3]:
                        porteV = STRUCT([T([1,2])([(punti[0]), punti[3]]), portaEsternaV(.02, punti[1]-punti[3])])
                    else:
                        porteV = STRUCT([T([1,2])([(punti[0]), punti[1]]), portaEsternaV(.02, punti[1]-punti[3])])
                    j = 1
                if k == 1 and abs(punti[1] - punti[3]) < .05:
                    if punti[0] > punti[2]:
                        porte = STRUCT([porte, T([1,2])([(punti[2]), punti[1]]), portaEsterna(punti[0]-punti[2], .02)])
                    else:
                        porte = STRUCT([porte, T([1,2])([(punti[0]), punti[1]]), portaEsterna(punti[0]-punti[2], .02)])
                if k == 0 and abs(punti[1] - punti[3]) < .05:
                    if punti[0] > punti[2]:
                        porte = STRUCT([T([1,2])([(punti[2]), punti[1]]), portaEsterna(punti[0]-punti[2], .02)])
                    else:
                        porte = STRUCT([T([1,2])([(punti[0]), punti[1]]), portaEsterna(punti[0]-punti[2], .02)])
                    k = 1
    if j:
        porteV = STRUCT([T(1)(.15), porteV])
    if k:
        #porte = STRUCT([T(2)(.25), porte])
        porte = STRUCT([porte])
    if j and k:
        pianta = STRUCT([pianta, porte, porteV])
    if j and not k:
        pianta = STRUCT([pianta, porteV])
    if not j and k:
        pianta = STRUCT([pianta, porte])
    return pianta

def minMaxX():
    j = 0
    minX = 1000
    maxX = 0
    with open ('interni.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if punti[0] < minX:
                    minX = punti[0]
                if punti[0] > maxX:
                    maxX = punti[0]
    return [minX, maxX]

def minMaxY():
    j = 0
    minY = 1000
    maxY = 0
    with open ('interni.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if punti[1] < minY:
                    minY = punti[1]
                if punti[1] > maxY:
                    maxY = punti[1]
    return [minY, maxY]

def minMaxTot():
    minX = 1000
    maxX = 0
    minY = 1000
    maxY = 0
    with open ('interni.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                punti = []
                for val in row:
                    punti.append(float(val)/60)
                if punti[0] < minX:
                    minX = punti[0]
                if punti[0] > maxX:
                    maxX = punti[0]
                if punti[1] < minY:
                    minY = punti[1]
                if punti[1] > maxY:
                    maxY = punti[1]
                if punti[2] < minX:
                    minX = punti[2]
                if punti[2] > maxX:
                    maxX = punti[2]
                if punti[3] < minY:
                    minY = punti[3]
                if punti[3] > maxY:
                    maxY = punti[3]
    return [minX, maxX, minY, maxY]
    
def appartamento(n):
    with open ('porte.lines', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                    portaX = float(row[0])/60
                    portaY = float(row[1])/60
    mura = CUBOID([.001, .001, .001])
    pianta = muriInterni(mura)
    pianta = porteEsterne(pianta)
    pianta = finestre(pianta)
    pianta = porteInterne(pianta)
    pianta = correzione(pianta)
    pianta = aggiungiFinestre(pianta)
    pianta = aggiungiPorte(pianta)
    pianta = aggiungiPorteInterne(pianta)
    mtot = minMaxTot()
    soffitto = CUBOID([mtot[1]-mtot[0], mtot[3]-mtot[2], .17])
    pianta = STRUCT([pianta, T([1,2,3])([mtot[0]+.1, mtot[2]+.1, 3.]), soffitto, T(3)(-3-.17), soffitto])
    mX = minMaxX()
    mediaX = (mX[0] + mX[1])/2
    mY = minMaxY()
    mediaY = (mY[0] + mY[1])/2
    pianta = STRUCT([T([1,2])([-mediaX, -mediaY]), pianta])
    pianta = STRUCT([R([1,2])(n*math.pi/2), pianta])
    if n == 0:
        pianta = STRUCT([T([1,2])([-portaX + mediaX, -portaY + mediaY]), pianta])
    if n == 1:
        pianta = STRUCT([T([1,2])([portaY - mediaY, -portaX + mediaX]), pianta])
        pianta = S(2)(-1)(pianta)
    if n == 2:
        pianta = STRUCT([T([1,2])([portaX - mediaX, portaY - mediaY]), pianta])
    if n == 3:
        pianta = STRUCT([T([1,2])([-portaY + mediaY, +portaX - mediaX]), pianta])
        #pianta = S(2)(-1)(pianta)
        
    return [pianta, mX[1], mY[1]]
    
