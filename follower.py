from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color
from time import sleep

HI, LO = 200, 80
class Follower:
    def __init__(self, resolution:tuple[int, int], motors:tuple[int, int], speed = 1.5):
        w, h = resolution
        x, y = (coord // 2 for coord in resolution) 

        SAMPLE_SIZE = (70, 70)
        self.geometry = {
            'search_area_l': ((x - 60, h - 100), (80, 80)),
            'search_area_r': ((x + 60, h - 100), (80, 80)),
            'central': ((x, h - 80), SAMPLE_SIZE),
            'left': ((x - 120, h - 80), SAMPLE_SIZE),
            'right': ((x + 120, h - 80), SAMPLE_SIZE),
            'mleft': ((x - 220, h - 80), SAMPLE_SIZE),
            'mright': ((x + 220, h - 80), SAMPLE_SIZE),
            'l90check': ((x - 120, h - 180), SAMPLE_SIZE),
            'r90check': ((x + 120, h - 180), SAMPLE_SIZE),
            'close_area': ((x, h - 100), (w, 50))
        }
        self.tk = ServoTank(*motors)
        self.kill = self.tk.kill
        self.macro = Macro(self)
        self.speed = speed
        self.failsafe = 5
        self.last = ''

    def __getattr__(self, name):
        if name in self.geometry:
            return self.geometry[name]
    
    def track(self, lineframe, greenframe):
        self.frame = lineframe
        SPEED, mv = self.speed, self.tk
        sto, macro = '', None

        green = self.check_green(greenframe) 
        if green:
            if green == 2:
                mv.back(1.5*SPEED, .1)
                mv.left(1.5*SPEED, .3)
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'left', SPEED, lambda: self.tk.back(SPEED, .1))
            elif green == -1:
                sto = '<-V'
                mv.fwd(SPEED, .25)
                mv.left(SPEED, 1)
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'left', .8*SPEED) #, lambda: self.tk.back(SPEED, .1))
            elif green == 1:
                sto = 'V->'
                mv.fwd(SPEED, .25)
                mv.right(SPEED, 1)
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'right', .8*SPEED) #, lambda: self.tk.back(SPEED, .1))
            return sto, macro

        central = lineframe(*self.central)
        l, r = lineframe(*self.left), lineframe(*self.right)
        L, R = lineframe(*self.mleft), lineframe(*self.mright)

        cl, ll, rl = central.light, l.light, r.light
        Ll, Rl = L.light, R.light

        check90 = None

        #TODO mover la pra cima
        MI = 35 
        rst_failsafe = True

        if Ll > MI and ll > MI and rl > MI and Rl > MI:
            sto = '^'
            mv.fwd(SPEED, .1)
        elif ll > MI and Ll > 50 and Rl < MI:
            if cl > 30:
                check90 = lineframe(*self.r90check)
                if check90.light < MI:
                    sto = '<-90'
                    mv.fwd(SPEED, .25)
                    macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'left', .8*SPEED) #, lambda: self.tk.back(SPEED, .1))
                else:
                    sto = '9^9'
                    mv.fwd(SPEED, .1)
            else:
                sto = '<-'
                mv.left(.7*SPEED, .1)
        elif ll > MI and Ll < MI and Rl < MI:
            if '->' in self.last:
                sto = '_^_'
                mv.fwd(SPEED, .1)
            else :
                sto = '<-'
                mv.left(.7*SPEED, .1)
        elif Ll > MI and ll < MI and Rl < MI:
                sto = '<-*'
                mv.left(SPEED, .3)
                # mv.fwd(SPEED, .3)
                # macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'left', .8*SPEED) #, lambda: self.tk.back(SPEED, .1))
        #@@ 
        elif rl > MI and Rl > 50 and Ll < MI:
            if cl > 30:
                check90 = lineframe(*self.l90check)
                if check90.light < MI:
                    sto = '90->'
                    mv.fwd(SPEED, .25)
                    macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'right', .8*SPEED) # , lambda: self.tk.back(SPEED, .1))
                else:
                    sto = '9^9'
                    mv.fwd(SPEED, .1)
            else:
                sto = '->'
                mv.right(.7*SPEED, .1)
        elif rl > MI and Rl < MI and Ll < MI:
            if '<-' in self.last:
                sto = '_^_'
                mv.fwd(SPEED, .1)
            else:
                sto = '->'
                mv.right(.7*SPEED, .1)
        elif Rl > MI and rl < MI and Ll < MI:
                sto = '*->'
                mv.right(SPEED, .3)
                # mv.fwd(SPEED, .3)
                # macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'right', .8*SPEED) #, lambda: self.tk.back(SPEED, .1))
        elif cl > MI:
            sto = '^'
            mv.fwd(SPEED, .1)
        else:
            sto = 'v'
            self.failsafe += 1
            rst_failsafe = False
            if self.failsafe >= 6:
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'back', .8*SPEED, lambda: self.tk.back(SPEED, .5))

            else:
                mv.fwd(.7*SPEED, .15)

        if rst_failsafe:
            self.failsafe = 0

        for fr in [central, l, r, L, R, check90]:
            if not fr: 
                continue
            fr.draw_label(round(fr.light), org=(0, 50), color=Color.red, scale=.5)
            fr.draw_limits(color=Color.red)

        self.last = sto
        return sto, macro
    
    def check_green(self, frame):
        # TODO mover pra cimak
        HIGREEN = 55 
        LOGREEN = 2
        close = frame(*self.close_area)
        green = close.light

        frame.draw_label(round(green), org=frame.center, thickness=2, color=Color.green)
        close.draw_limits(color=Color.white)    

        x, y = close.center
        left = close((x - x // 2, y) , (x, y*2))
        right = close((x + x // 2, y), (x, y*2))
        diff = left.light - right.light

        for fr in [right, left]:
            fr.draw_limits(color=Color.blue)
            fr.draw_label(fr.light, color=Color.blue, org= (0, 40), scale=.5)

        if green > HIGREEN:
            return 2 
        else:
            if diff > 5:
                return -1
            elif diff < - 5:
                return 1
            else:
                return 0 

class Macro:
    def __init__(self, src:Follower):
        self.src = src

    def __getattr__(self, name):
        return self.src.__getattr__(name)

    def find_line(self, frame, cnt, search, speed, *afterwards):
        if search == 'left':
            lateral = frame(*self.src.right)
        #     search_area = frame(*self.src.search_area_l)
        elif search == 'right':
            lateral = frame(*self.src.left)
        #     search_area = frame(*self.src.search_area_r)
        else: 
            lateral = None
        #     search_area = frame(*self.src.central)
        search_area = frame(*self.src.central)
        li = search_area.light
        Li = 50 
        if lateral:
            Li = lateral.light

        if li < 50 and Li < 50:
            self.src.tk.__getattr__(search)(speed)
            search_area.draw_limits(color=Color.red)
            search_area.draw_label(li, color=Color.red, org=(0, 75), scale=.5)
            if lateral:
                lateral.draw_limits(color=Color.red)
                lateral.draw_label(Li, color=Color.red, org=(0, 75), scale=.5)

            return True
        else:
            self.src.tk.stop()
            search_area.draw_limits(color=Color.green)
            search_area.draw_label(li, color=Color.green, org=(0, 50), scale=.5)
            if lateral:
                lateral.draw_limits(color=Color.green)
                lateral.draw_label(Li, color=Color.green, org=(0, 50), scale=.5)
            # if cnt >= 4:
            #     self.src.tk.back(speed, .2)
            # else:
            #     self.src.tk.__getattr__(search)(speed)
            for func in afterwards:
                func()
            return False
