from pyplasm import *
from appartamento import *

def stairs(dx,dy,dz):
    k = 0
    n = dy/.25
    n -= n%1
    treadStep = dy/n
    riserStep = dz/n
    firstStep = CUBOID([dx,treadStep,riserStep])
    step = MKPOL([[[0,0],[0,riserStep*2],[treadStep,riserStep*2],[treadStep,riserStep]],[[1,2,3,4]],1])
    step = PROD([QUOTE([dx]), step])
    stairs = [firstStep, T(2)(treadStep), step] 
    for c in range(2,int(n)):
        stairs.append(T([2,3])([treadStep, riserStep]))
        stairs.append(step)
    stairs.append(T([2,3])([treadStep, riserStep]))
    return stairs

def pianerottolo(dx, dy, dz, a, nApp):
    n = dy/.25
    n -= n%1
    riserStep = dz/n
    if a:
        app1 = appartamento(1)[0]
        app = appartamento(3)[0]
        mx2 = appartamento(2)[1]
        app2 = appartamento(2)[0]
        piano = T(2)(-dy/2.5)(CUBOID([dx, dy/1.1, riserStep]))
        piano = STRUCT([piano, app])
        if nApp > 1: piano = STRUCT([piano, T(1)(dx), app1])
        if nApp > 2:
            if nApp >6: lista = [T(1)(-dx+mx2/1.2)]
            else: lista = [T(1)(-dx+mx2/2)]
            for r in range(2,nApp):
                lista += [app2, T(1)(mx2-.7)]
            appartamenti = STRUCT(lista)
            nAPP = nApp
            if nApp == 3:
                nAPP = 0
            piano = STRUCT([piano, T([1,2])([dx-(nApp-2)*mx2/(5+nAPP), dy/2.05]), appartamenti])
    else:
        piano = CUBOID([dy-.1, dx, riserStep])
    return piano

def pianoScale(dx, dy, dz, nApp):
    rampa = STRUCT(stairs(dx, dy, dz))
    rampa1 = stairs(dx, dy, dz)
    rampa2 = STRUCT([S(2)(-1), rampa])
    rampa1.append(pianerottolo(dx, dy, dz, 0, nApp))
    rampa1 = STRUCT(rampa1)
    muro = MKPOL ([[[0., 0.], [dx*2.45, 0.], [0., dy*1.4], [dx*2.45, dy*1.4]],[[1,3],[3,4],[2,4]],[[1]]])
    muro = OFFSET([0, .1, dz * 2])(muro)
    muro = OFFSET([.1, 0,0])(muro)
    if nApp > 2: 
        mx = appartamento(2)[1]
        n = (nApp - 2)/2
        m = 0
    else: 
        n = 0
        mx = 0
        m = appartamento(2)[1]/2
    rampa = STRUCT([rampa1, T(1)(-.1), muro, T(1)(.1), T([1,2,3])([dx + .25, dy, dz - .17]), rampa2])
    return [rampa, T([1,2])([-dx + mx*n + m/2, dy])]

def piano(dx, dy, dz, nApp):
    n = dy/.25
    n -= n%1
    riserStep = dz/n
    p = []
    p.append(T([1,2,3])([-2.5*dx, 0, 2*dz-.34]))
    p.append(S(2)(-1))
    if nApp > 2: 
        mx = appartamento(2)[1]-1
        m = 0
    else: 
        mx = 0
        m = appartamento(2)[1]/5
    p.append(pianerottolo(m + (nApp - 2)*(mx)+.3, dy * 2.5 , dz*2.5, 1, nApp))
    return p

def rampaScale(dx, dy, dz, nApp, ultimo):
    if nApp > 2: 
        mx = appartamento(2)[1]
        m = 0
    else: 
        mx = 0
        m = appartamento(2)[1]
    if not ultimo:
        scale = pianoScale(dx, dy, dz, nApp)[0]
        scale = STRUCT([pianoScale(dx,dy,dz,nApp)[1], scale])
        floor = piano (dx, dy, dz, nApp)
        scale = STRUCT([S(2)(-1), scale, floor[1], floor[2]])
    else:
        floor = piano (dx, dy, dz, nApp)
        scale = STRUCT([S(2)(-1), floor[1], floor[2]])
    return scale

def numeroPiani(h, dx, dy, dz, nApp):
    n = dy/.25
    n -= n%1
    riserStep = dz/n
    rampa = rampaScale(dx, dy, dz, nApp, 0)
    ultimoPiano = rampaScale(dx, dy, dz, nApp, 1)
    finale = [rampa]
    for r in range(1, h):
        finale.append(T(3)(2*(dz-riserStep)))
        if r == h-1: finale.append(ultimoPiano)
        else: finale.append(rampa) 
    rampaFinale = STRUCT(finale)
    return rampaFinale
