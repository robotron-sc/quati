from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color
from time import sleep

HI = 110
LO = 20
HI_GREEN = 70 
LO_GREEN = 10 

SPEED = .3 

STYLE = {
    'color':Color.red,
    'org':(0, 50),
    'scale':.5,
    'thickness':2
}

def setup(resolution):
    global w, h, x, y 
    w, h = resolution 
    x, y = (ii // 2 for ii in resolution) 
   
    global geo 
    geo = {
        'central' : ((x, h - 100), (75, 75)),
        'llateral' : ((w // 2 + 100, h - 100), (150, 75)),
        'rlateral' : ((w // 2 - 100, h - 100), (150, 75)),
    }

    global mv, kill
    mv = ServoTank(6, 13)
    kill = lambda: mv.kill()

def track(image):
    central = image((x, h-100), (75, 75))
    li = central.light

    r, l= image(*geo['rlateral']), image(*geo['rlateral'])
    rl, ll = r.light, l.light

    green = check_green(image)

    if li < LO:
        diff = ll - rl
        # TODO trocar 10 por var 
        if diff > 10:
            # DESALINHADO P ESQ
            out = '->'
            mv.right(SPEED)
        elif diff < -10:
            # DESALINHADO P DIR 
            out = '<-'
            mv.left(SPEED)
        else:
            # ALINHADO
            out = '^'
            mv.fwd(SPEED)
    elif rl < LO and ll > LO:
        out = 'º->'
        mv.fwd(SPEED)
        sleep(.2)
        mv.set(SPEED, -SPEED)
        sleep(.5)
        mv.stop()
    elif ll < LO and rl > LO:
        out = '<-º'
        mv.fwd(SPEED)
        sleep(.2)
        mv.set(-SPEED, SPEED)
        sleep(.5)
        mv.stop()
    else:
        # PERDIDO
        if rl < HI and ll > HI:
            out = '-+>'
            mv.right(SPEED)
        elif ll < HI and rl > HI:
            out = '<+-'
            mv.left(SPEED)
        else:
            out = 'v'
            mv.back(SPEED*.75)

    r.draw_label(round(rl, 2), **STYLE)
    l.draw_label(round(ll, 2), **STYLE)
    central.draw_limits(color=Color.red)
    central.draw_label(round(li, 2), **STYLE)

    return out, green

def check_green(image):
    close = image((x, h-50), (w, 100))
    filtered = close.filter([60, 255, 15], [108, 255, 190])
    green = filtered.light

    if green < LO_GREEN:
        return None
    if green > HI_GREEN:
        pass
    else:
        l = close((x))

    close.draw_limits(color=Color.white)
    filtered.draw_label(
        green,
        org = filtered.center,
        color = Color.green,
        scale = 2,
        thickness = 2
    )
    
    return filtered