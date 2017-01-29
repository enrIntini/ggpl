from pyplasm import *
from math import *

def determinante(m):
    result = 0
    col = 0
    if len(m) == 1:
        return m[0][0]
    for rowEl in m[len(m)-1]:
        matrix = []
        for cont in range (0, len(m)-1):
            tmpRow = []
            for el in range (0, len(m)):
                if el <> col:
                    tmpRow.append(m[cont][el])
            matrix.append(tmpRow)
        result += pow(-1, (col+len(m)-1))*rowEl*determinante(matrix)
        col += 1
    return result

# ax + by + c = -z
def trovaPiano (A, B, C):
    m = []
    for index in range(0, 3):
        row = []
        # coefficienti di c
        if index == 2: row = [1, 1, 1]
        else: row =[A[index], B[index], C[index]]
        m.append(row)
    D = determinante(m)
    ma = [[-A[2], -B[2], -C[2]], m[1], m[2]]
    Da = determinante(ma)
    mb = [m[0], [-A[2], -B[2], -C[2]], m[2]]
    Db = determinante(mb)
    mc = [m[0], m[1], [-A[2], -B[2], -C[2]]]
    Dc = determinante(mc)
    result = [Da/D, Db/D, Dc/D]
    return result

#trovo i due punti di intersezione tra i piani all'altezza 0 e all'altezza h del tetto
def intersezioniPiani(piano1, piano2, h):
    # per il piano z = 0 ho due equazioni del tipo x + ay = - c
    # ax + by = -c
    intersezioni = []
    m = [[piano1[0], piano2[0]], [piano1[1], piano2[1]]]
    D = determinante(m)
    el1 = -piano1[2]
    el2 = -piano2[2]
    mx1 = [[el1, el2], m[1]]
    Dx1 = determinante(mx1)
    my1 = [m[0], [el1, el2]]
    Dy1 = determinante(my1)
    intersezioni.append([Dx1/D, Dy1/D, 0.])
    
    #per il punto z = h ho due equazioni del tipo x + ay = - c - bh
    # ax + by = - c -h
    el1 = -piano1[2] - h
    el2 = -piano2[2] - h
    mx2 = [[el1, el2], m[1]]
    Dx2 = determinante(mx2)
    my2 = [m[0], [el1, el2]]
    Dy2 = determinante(my2)
    intersezioni.append([Dx2/D, Dy2/D, h])
    
    return intersezioni

def retta (pt1, pt2):
    # y = mx + q
    if pt2[0] - pt1[0] != 0:
        m = (pt2[1] - pt1[1])/(pt2[0] - pt1[0])
        q = pt1[1] - m*pt1[0]
        return [m, q]
    #ax + by + c = 0 se la retta e' verticale
    else:
        return [1.0, .0, pt1[0]]

# y - mx = q
# x = k

def intersezioneRette(r1, r2):
    m1 = []
    m2 = []
    m3 = []
    r = [r1, r2]
    for retta in r:
        if len(retta[0]) == 2:
            m1.append(1.0)
            m2.append(-retta[0][0])
            m3.append(retta[0][1])
        else:
            m1.append(.0)
            m2.append(retta[0][0])
            m3.append(retta[0][2])
    m = [m1, m2]
    D = determinante(m)
    my = [m3, m2]
    Dy = determinante(my)
    mx = [m1, m3]
    Dx = determinante(mx)
    if D:
        return [Dx/D, Dy/D]
    return 0

#Devo fare in modo che scorra la lista delle rette a partire dalla retta relativa a quell'angolo concavo
#appena trova un'intersezione si ferma e ritorna il puno
def angoloConcavo (pt1, pt2, pt3, rette):
    retteCandidate = []
    ok = 0
    c = 0
    primoCandidato = 0
#scorro le rette finche' non trovo la prima retta di cui pt2 e' il vertice
    while not ok:
        if not escludiRetta(pt1, pt2, pt3, rette[c]):
            c += 1
        else:
            c += 1
            ok = 1
    
    ok = 0
    while not ok:
        if c == len(rette):
            c = 0
        if escludiRetta(pt1, pt2, pt3, rette[c]):
            c += 1
        else:
            ok = 1
    ok = 0
    while not ok:
        if c == len(rette):
            c = 0
        if not escludiRetta(pt1, pt2, pt3, rette[c]):
            retteCandidate.append(rette[c])
            c += 1
        else:
            ok = 1
            
    r12 = [retta(pt1, pt2)]
    for r in retteCandidate:
        if not escludiRetta(pt1, pt2, pt3, r):
            p = intersezione(r12, r)
            if p and intersezioneAccettabile(pt1, pt2, p):
                return p
    return 0

def intersezioneAccettabile(p1, p2, p3):
    if p1[0] > p2[0] and p3[0] > p2[0]:
        return 0
    if p1[0] < p2[0] and p3[0] < p2[0]:
        return 0
    if p1[0] == p2[0] and p3[0] != p1[0]:
        return 0
    if p1[1] > p2[1] and p3[1] > p2[1]:
        return 0
    if p1[1] < p2[1] and p3[1] < p2[1]:
        return 0
    if p1[1] == p2[1] and p3[1] != p1[1]:
        return 0
    return 1

def equals(pt1, pt2):
    if pt1[0] == pt2[0] and pt1[1] == pt2[1]:
        return 1
    return 0

def escludiRetta (A, B, C, retta):
    if equals(retta[1], A) or equals(retta[2], A) or equals(retta[1], B) or equals(retta[2], B):
        return 1
    return 0

#se il punto a e' interno al segmento bc
def compreso(a, b, c):
    if (a[0] <= b[0] and a[0] >= c[0]) or (a[0] >= b[0] and a[0] <= c[0]):
        if (a[1] <= b[1] and a[1] >= c[1]) or (a[1] >= b[1] and a[1] <= c[1]):
            return 1
    return 0

#se il punto a e' interno al segmento bc
def compresoDiverso(a, b, c):
    if (a[0] < b[0] and a[0] > c[0]) or (a[0] > b[0] and a[0] < c[0]):
        if (a[1] <= b[1] and a[1] >= c[1]) or (a[1] >= b[1] and a[1] <= c[1]):
            return 1
    if (a[1] < b[1] and a[1] > c[1]) or (a[1] > b[1] and a[1] < c[1]):
        if (a[0] <= b[0] and a[0] >= c[0]) or (a[0] >= b[0] and a[0] <= c[0]):
            return 1
    return 0

#restituisce 1 se la seconda retta passata come parametro ha uno dei due estremi in comune con la prima (solo 1!). 0 altrimenti
def rettaTrovata(r1, r2):
    eq11 = equals(r1[1], r2[1])
    eq21 = equals(r1[2], r2[1])
    eq12 = equals(r1[1], r2[2])
    eq22 = equals(r1[2], r2[2])
    if (eq11 and not eq22) or (not eq11 and eq22) or (eq12 and not eq21) or (not eq12 and eq21):
        return 1
    return 0

def ordinaRette (rette):
    nuoveRette = []
    nuoveRette.append(rette[len(rette)-1])
    indiciRetteSelezionate = [0]
    for c in range (1, len(rette)):
        ok = 0
        index = 0
        tmp = nuoveRette[len(nuoveRette)-1]
        while not ok:
            if rettaTrovata(rette[index], tmp) and not rette[index] in nuoveRette:
                nuoveRette.append(rette[index])
                ok = 1
            index += 1
    return nuoveRette

def intersezione(r1, r2):
    k = intersezioneRette(r1, r2)
    if k:
        if compreso(k, r2[1], r2[2]):
            return k
    return 0

# l'array punti e' composto da 0 per tutti i punti gia' considerati e eliminati
def celleConvesse(pti, cnc):
    punti = pti
    concavi = cnc
    celle = []
    c = 0
    ttl2 = 30
    while c < len(punti):
        aggiungi = 0
        cella = []
        #analizzo un punto per volta (escludo i punti tolti in iterazioni precedente)
        tmp = punti[c]
        opposto = 0
        if tmp:
        #vedo se il punto e' concavo (cioe' e' presente nell'array concavi). se e' concavo prendo l'intersezione dovuta a quel punto
            for cn in concavi:
                if equals(cn[0], tmp):
                    indiceConcavo = c
                    opposto = cn[1]
        # scorro tutti i punti da quello concavo fino all'intersezione e, se non ci sono altri concavi in mezzo, salvo la cella
            index = c + 1
            indiceOpposto = len(punti)
            oppostoTrovato = 0
            if opposto:
                ttl = 20
                # cerco l'opposto
                while not oppostoTrovato:
                    if ttl == 0:
                        oppostoTrovato = 1
                    if index == len(punti):
                        index = 0
                    if punti[index]:
                        tmp2 = punti[index]
                    # se il punto considerato e' un concavo cerco il suo opposto
                        for cn in concavi:
                            if equals(cn[0], tmp2):
                                indiceConcavo = index
                                opposto = cn[1]
                        if equals(opposto, tmp2):
                            oppostoTrovato = 1
                            indiceOpposto = index
                    index += 1
                    ttl -= 1

                if oppostoTrovato and indiceConcavo < indiceOpposto:
                    for r in range (indiceConcavo, indiceOpposto + 1):
                        if punti[r]:
                            cella.append(r+1)
                            # elimino dalla lista dei punti tutti i punti presi per la cella tranne l'opposto
                            if r != indiceOpposto:
                                punti[r] = 0
                if oppostoTrovato and indiceConcavo > indiceOpposto:
                    for r in range(indiceConcavo, len(punti)):
                        if punti[r]:
                            cella.append(r+1)
                            # elimino dalla lista dei punti tutti i punti presi per la cella tranne l'opposto
                            if r != indiceOpposto:
                                punti[r] = 0
                        for r in range(0, indiceOpposto + 1):
                            if punti[r]:
                                cella.append(r+1)
                                # elimino dalla lista dei punti tutti i punti presi per la cella tranne l'opposto
                                if r != indiceOpposto:
                                    punti[r] = 0
            
            if len(cella) > 0:
                celle.append(cella)
                c = 0
            if len(cella) == 0: 
                c += 1
        ttl2 -= 1
        if ttl2 == 0:
            c = 100000
    
    cella = []
    for r in range (0, len(punti)):
        if punti[r]:
            cella.append(r+1)
        
    if len(cella) > 0:
        celle.append(cella)
        
    return celle

def disegna1D (rette):
    punti = []
    vertici = []
    for r in rette:
        punti.append(r[1])
    for c in range(1, len(punti)+1):
        if c == len(punti):
            vertici.append([c, 1])
        else:
            vertici.append([c, c+1])
    return MKPOL([punti, vertici,[[1]]])

def disegnaPiano(rette):
    punti = []
    intersezioniConcavi = []
    puntiIntersezioni = []
    for r in rette:
        punti.append(r[1])
    for c in range(0, len(punti)):
        if c == 0:
            tmp = angoloConcavo(punti[len(punti)-1], punti[0], punti[1], rette)
        if c == len(punti) - 1:
            tmp = angoloConcavo(punti[len(punti)-2],punti[len(punti)-1], punti[0], rette)
        if c > 0 and c < len(punti)-1:
            tmp = angoloConcavo(punti[c-1],punti[c], punti[c+1], rette)
        if tmp:
            intersezioniConcavi.append([punti[c], tmp])

    puntiFinali = []
    for r in rette:
        puntiIntersezioni.append(r[1])
        puntiFinali.append(r[1])
        for i in intersezioniConcavi:
            if len(r[0]) == 2 and abs(i[1][1] - r[0][0]*i[1][0] - r[0][1]) < 0.000001 and compresoDiverso(i[1], r[1], r[2]):
                puntiIntersezioni.append(i[1])
                puntiFinali.append(i[1])
            if len(r[0]) == 3 and abs(i[1][0] - r[0][2]) < 0.000001 and compresoDiverso(i[1], r[1], r[2]):
                puntiIntersezioni.append(i[1])
                puntiFinali.append(i[1])
    
    celle = celleConvesse(puntiIntersezioni, intersezioniConcavi)
    disegno = MKPOL([puntiFinali, celle, [[1]]])
    return disegno