from rbsc.movement import ServoTank
from rbsc.camera import Image as img, Color
from time import sleep

HI, LO = 200, 60
class Follower:
    def __init__(self, resolution:tuple[int, int], motors:tuple[int, int], speed = .5):
        w, h = resolution
        x, y = (coord // 2 for coord in resolution) 

        self.geometry = {
            'x': x,
            'y' : y,
            'w' : w,
            'h' : h,
            'central': ((x, h - 100), (80, 80)),
            'search_area_l': ((x - 50, h - 100), (80, 80)),
            'search_area_r': ((x + 50, h - 100), (80, 80)),
            'left': ((x - 130, h - 100), (110, 80)),
            'right': ((x + 130, h - 100), (110, 80)),
        }
        self.tk = ServoTank(*motors)
        self.kill = self.tk.kill
        self.macro = Macro(self)
        self.speed = speed
        self.failsafe = 5

    def __getattr__(self, name):
        if name in self.geometry:
            return self.geometry[name]
    
    def track(self, frame):
        SPEED, mv = self.speed, self.tk
        sto, macro = '', None
        central = frame(*self.central)
        l, r = frame(*self.left), frame(*self.right)

        cl, ll, rl = central.light, l.light, r.light

        rst_failsafe = True
        # TODO ré quando todos forem > LO e < HI
        if cl > HI:
            if ll > HI and rl < LO:
                sto = '<-90'
                mv.fwd(SPEED, .3)
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'left', SPEED)
            elif rl > HI and ll < LO:
                sto = '90->'
                mv.fwd(SPEED, .3)
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'right', SPEED)
            elif ll > LO and rl < LO:
                sto = '<-'
                mv.left(.8*SPEED, .1)
            elif rl > LO and ll < LO:
                sto = '->'
                mv.right(.8*SPEED, .1)
            else:
                sto = '^'
                mv.fwd(1, .1)
        elif cl > LO:
            if ll > LO and rl < LO:
                sto = '<-'
                mv.left(.8*SPEED, .1)
            elif rl > LO and ll < LO:
                sto = '->'
                mv.right(.8*SPEED, .1)
            else:
                sto = '^'
                mv.fwd(1, .1)
        else:
            if ll > LO and rl < LO:
                sto = '<-?'
                mv.stop()
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'left', .8*SPEED)
            elif rl > LO and ll < LO:
                sto = '?->'
                mv.stop()
                macro = lambda fr, cnt: self.macro.find_line(fr, cnt, 'right', .8*SPEED)
            else:
                sto = 'v'
                self.failsafe += 1
                rst_failsafe = False
                if self.failsafe >= 8:
                    mv.back(SPEED, .1)
                else:
                    mv.fwd(1, .1)
        if rst_failsafe:
            self.failsafe = 0

        for fr in [central, l, r]:
            fr.draw_label(fr.light, org=(0, 70), color=Color.yellow, scale=.5)
            fr.draw_limits(color=Color.yellow)

        return sto, macro
    
class Macro:
    def __init__(self, src:Follower):
        self.src = src

    def __getattr__(self, name):
        return self.src.__getattr__(name)

    def find_line(self, frame, cnt, search, speed, *afterwards):
        if search == 'left':
            search_area = frame(*self.src.search_area_l)
        if search == 'right':
            search_area = frame(*self.src.search_area_r)
        li = search_area.light

        if li < LO:
            self.src.tk.__getattr__(search)(speed)
            search_area.draw_limits(color=Color.red)
            search_area.draw_label(li, color=Color.red, org=(0, 75), scale=.5)
            return True
        else:
            self.src.tk.stop()
            search_area.draw_limits(color=Color.green)
            search_area.draw_label(li, color=Color.green, org=(0, 75), scale=.5)
            if cnt >= 3:
                self.src.tk.back(speed, .2)
            else:
                self.src.tk.__getattr__(search)(speed)
            for func in afterwards:
                func()
            return False
