from rbsc.movement import Coord, CoordMove

TIME = .7

coords = {
    'claw_close': Coord(12, 1.5, time=TIME),
    'claw_open': Coord(4.5, 6.8, time=TIME),
    'claw_up': Coord(2,time=TIME),
    'claw_down': Coord(10,time=TIME),
    
    'claw_store': Coord(8,time=TIME),
    'storage_down': Coord(7, 4.5,time=TIME),
    'storage_up': Coord(2, 10,time=TIME),
    'open_alive': Coord(2, 1.5,time=TIME),
    'open_dead': Coord(12, 6.8,time=TIME),
}

claw_arm = CoordMove(5, coords)
claw_grab = CoordMove((27, 22), coords)
storage = CoordMove((4, 17), coords)
