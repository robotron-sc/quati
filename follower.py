from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color
from time import sleep

SPEED = .5

STYLE = {
    'color':Color.red,
    'org':(0, 50),
    'scale':.5,
    'thickness':2
}

STYLEG = {
    'color':Color.green,
    'org':(0, 30),
    'scale':.5,
    'thickness':2
}

STYLEF = {
    'color':Color.magenta,
    'org':(0, 80),
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
        'wider_central' : ((x, h - 100), (90, 110)),
        'llateral' : ((w // 2 - 140, h - 100), (130, 100)),
        'rlateral' : ((w // 2 + 140, h - 100), (130, 100)),
        'close' : ((x, h - 50), (w, 100))
    }

    global mv, kill
    mv = ServoTank(33, 31)
    kill = lambda: mv.kill()

failsafe = FAIL_CNT
def track(image):
    # TODO testar sem global
    global failsafe
    central = image(*geo['central'])
    li = central.light

    close = image(*geo['close'])
    close.draw_limits(color=Color.white)
    gdir, green = check_green(image)

    r, l= image(*geo['rlateral']), image(*geo['llateral'])
    rl, ll = r.light, l.light

    strd = ''
    scope = None 
    fail_add = False

    diff = ll - rl

    if li < LO:
        if ll < LO and rl > HI:
            strd = '<-90'
            mv.fwd(SPEED, .3)
            after = lambda : mv.back(SPEED)
            scope = lambda fr : Macros.findLine(fr, .9*SPEED, 'left', after)
        elif rl < LO and ll > HI:
            strd = '90->'
            mv.fwd(SPEED, .3)
            after = lambda : mv.back(SPEED)
            scope = lambda fr : Macros.findLine(fr, .9*SPEED, 'right', after)
        else:
            strd = '^'
            mv.fwd(SPEED)
    else:
        if diff < -DIFF: 
            strd = '<-'
            mv.left(.7 * SPEED)
        elif diff > DIFF:
            strd = '->'
            mv.right(.7 * SPEED)
        else: 
            strd = 'v'
            fail_add = True 
            failsafe += 1
            if failsafe >= FAIL_CNT:
                mv.back(1.2*SPEED)
            else:
                mv.fwd(.8*SPEED)
    if not fail_add: 
        failsafe = 0

    r.draw_limits(color=Color.blue)
    l.draw_limits(color=Color.blue)
    r.draw_label(round(rl, 2), **STYLE)
    l.draw_label(round(ll, 2), **STYLE)
    central.draw_limits(color=Color.red)
    central.draw_label(round(li, 2), **STYLE)
    central.draw_label(round(gdir, 2), **STYLEG)
    central.draw_label(failsafe, **STYLEF)

    return strd, scope

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

    # frame.draw_limits(color=Color.white)
    # filtered.draw_label(
    #     green,
    #     org = filtered.center,
    #     color = Color.green,
    #     scale = 2,
    #     thickness = 2
    # )
    
    return index, filtered

class Macros:
    def __init__(self):
        pass
        
    @staticmethod
    def turn90deg(speed, dir):
        mv.fwd(speed, 1)
        mv.stop(time=1)
        mv.left(speed*dir)
    
    @staticmethod
    def findLine(frame, speed, dir, *afterwards):
        central = frame(*geo['wider_central'])

        central.draw_limits(color=Color.red)
        central.draw_label(round(central.light, 3), **STYLE)

        mv.stop()
        if central.light > HI:
            mv.__getattr__(dir)(speed)
            return True 
        else:
            for func in afterwards:
                func()
            return False 
    