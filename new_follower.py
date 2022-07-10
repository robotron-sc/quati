from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color

STYLE = {
    'color':Color.red,
    'org':(0, 50),
    'scale':.5,
    'thickness':2
}
LO = 10 
HI = 80 
SPEED = .5
FAIL_CNT = 5

def setup(resolution, *motors):
    global x, y, w, h
    w, h = resolution
    x, y = (ii // 2 for ii in resolution)

    global geo
    geo = {
        'central': ((x, h - 100), (80, 80)),
        'wider_central': ((x, h - 100), (90, 110)),
        'llateral' : ((w // 2 - 100, h - 70), (80, 140)),
        'rlateral' : ((w // 2 + 100, h - 70), (80, 140)),
        'close' : ((x, h - 50), (w, 100))
    }

    global mv, kill
    mv = ServoTank(*motors)
    kill = mv.kill

failsafe = FAIL_CNT
def track(frame):
    global failsafe
    sto = ''
    macro = None

    central = frame(*geo['central'])
    ml = central.light 
    l, r = frame(*geo['llateral']), frame(*geo['rlateral'])
    ll, rl = l.light, r.light

    if ml < 2:
        if ll > LO and rl < LO:
            sto = '<-'
            macro = lambda fr: Macros.find_line(fr, .7*SPEED, 'left')
        elif rl > LO and ll < LO:
            sto = '->'
            macro = lambda fr: Macros.find_line(fr, .7*SPEED, 'right')
        else:
            sto = 'v'
            mv.back(SPEED)
    else:
        diff = ll - rl
        if diff > 10:
            sto = '<-.'
            macro = lambda fr: Macros.find_line(fr, SPEED, 'left')
        elif diff < -10:
            sto = '.->'
            macro = lambda fr: Macros.find_line(fr, SPEED, 'right')
        else:
            sto = '^'
        mv.fwd(SPEED)


    central.draw_limits(color=Color.red)
    central.draw_label(round(ml, 2), **STYLE)
    l.draw_limits(color=Color.blue) 
    l.draw_label(round(ll, 2), **STYLE | {'color': Color.blue})
    r.draw_limits(color=Color.blue) 
    r.draw_label(round(rl, 2), **STYLE | {'color': Color.blue})

    return sto, macro 

class Macros:
    def __init__(self):
        pass

    @staticmethod
    def find_line(frame, speed, dir, *afterwards):
        central = frame(*geo['wider_central'])

        central.draw_limits(color=Color.red)
        central.draw_label(round(central.light, 3), **STYLE)

        # mv.stop()
        if central.light < LO:
            mv.__getattr__(dir)(speed)
            return True 
        else:
            mv.stop()
            for func in afterwards:
                func()
            return False 