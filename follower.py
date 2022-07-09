from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color
from time import sleep

HI = 100
LO = 80 
HI_GREEN = 70 
LO_GREEN = 10 
DIFF_GREEN = 15 
FAIL_CNT = 5 

SPEED = .5

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
        'central' : ((x, h - 100), (80, 80)),
        'llateral' : ((w // 2 - 140, h - 100), (130, 80)),
        'rlateral' : ((w // 2 + 140, h - 100), (130, 80)),
        'close' : ((x, h - 50), (w, 100))
    }

    global mv, kill
    mv = ServoTank(33, 31)
    kill = lambda: mv.kill()

failsafe = 0
def track(image):
    global failsafe
    central = image(*geo['central'])
    li = central.light

    close = image(*geo['close'])
    close.draw_limits(color=Color.white)
    # gdir, green = check_green(image)

    r, l= image(*geo['rlateral']), image(*geo['llateral'])
    rl, ll = r.light, l.light

    strd = ''
    fail_add = False
    if li < LO:
        if ll < LO and rl > LO:
            strd = '<-90'
            mv.left(2*SPEED)
        elif rl < LO and ll > LO:
            strd = '90->'
            mv.right(2*SPEED)
        else:
            strd = '^'
            mv.fwd(SPEED)
    elif li < HI:
        if ll < LO and rl > HI:
            strd = '<-+'
            mv.left(SPEED)
        elif rl < LO and ll > HI:
            strd = '+->'
            mv.right(SPEED)
        elif ll < LO and rl > LO:
            strd = '<-'
            mv.left(SPEED)
        elif rl < LO and ll > LO:
            strd = '->'
            mv.right(SPEED)
        elif ll < HI and rl > HI:
            strd = '<-m'
            mv.left(1.2*SPEED)
        elif rl < HI and ll > HI:
            strd = 'm->'
            mv.right(1.2*SPEED)
        else: 
            strd = 'v'
            mv.back(SPEED)
    else:
        if ll < HI and rl > HI:
            strd = '<-?'
            mv.left(.8*SPEED)
        elif rl < HI and ll > HI:
            strd = '?->'
            mv.right(.8*SPEED)
        else:
            strd = 'v'
            fail_add = True 
            if failsafe >= FAIL_CNT:
                mv.back(1.2*SPEED)
    if not fail_add: 
        failsafe = 0

    r.draw_limits(color=Color.blue)
    l.draw_limits(color=Color.blue)
    r.draw_label(round(rl, 2), **STYLE)
    l.draw_label(round(ll, 2), **STYLE)
    central.draw_limits(color=Color.red)
    central.draw_label(round(li, 2), **STYLE)

    return strd 

def check_green(frame:img.Data) -> tuple[int, img.Data]:
    filtered = frame.filter([60, 255, 15], [108, 255, 190])
    green = filtered.light
    index = 0

    if green < LO_GREEN:
        # SEM VERDE
        pass
    elif green < HI_GREEN:
        # UM VERDE
        fw, fh = frame.shape
        fx, fy = frame.center
        l = frame((fx // 2, fy), (fx, fh))
        r = frame(((3 * fx) // 2, fy), (fx, fh))

        diff = l.light - r.light
        if diff > DIFF_GREEN:
            index = -1 
        else: 
            index = +1 
    else:
       index = 2 

    frame.draw_limits(color=Color.white)
    filtered.draw_label(
        green,
        org = filtered.center,
        color = Color.green,
        scale = 2,
        thickness = 2
    )
    
    return index, filtered

    class Macros:
        def __init__(self):
            pass
        
        @staticmethod
        def turn90deg(speed, dir):
            mv.fwd(speed, 1)
            mv.stop(time=1)
            mv.left(speed*dir)