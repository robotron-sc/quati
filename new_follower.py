from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color

STYLE = {
    'color':Color.red,
    'org':(0, 50),
    'scale':.5,
    'thickness':2
}

def __call__(resolution, *motors):
    global x, y, w, h
    w, h = resolution
    x, y = (ii // 2 for ii in resolution)

    global geo
    geo = {
        'central': ((x, h - 100), (80, 80)),
        'wider_central': ((x, h - 100), (90, 110)),
        'llateral' : ((w // 2 - 140, h - 100), (130, 100)),
        'rlateral' : ((w // 2 + 140, h - 100), (130, 100)),
        'close' : ((x, h - 50), (w, 100))
    }

    global mv
    mv = ServoTank(*motors)
    kill = mv.kill

def track(frame):
    sto = ''
    line = central.filter([0]*3, [255, 10, 20])

    central = line(*geo['central'])
    ml = central.light 
    l, r = line(*geo['llateral']), line(*geo['rlateral'])
    ll, rl = l.light, r.light

    diff = ll - rl 

    if diff > 10:
        if ml < LO:
            stro = '9>'
            mv.fwd(SPEED, .3)
            # TODO
        else:
            stro = '->'
            mv.right(.7 * SPEED)

    elif diff < -10:
        if ml < LO:
            stro = '<6'
        else:
            stro = '<-'
            mv.left(.7 * SPEED)
    else:
        if ml < LO:
            stro = '^'
            mv.fwd(SPEED)
        else:
            stro = 'v'
            # TODO
            mv.back(speed)

    central.draw_limits(color=Color.red)
    central.draw_label(round(ml, 2), **STYLE | {'color':Color.blue})
    l.draw_limits(colorr=Color.blue) 
    central.draw_label(round(ll, 2), **STYLE)
    r.draw_limits(colorr=Color.blue) 
    central.draw_label(round(rl, 2), **STYLE)

    return sto, None