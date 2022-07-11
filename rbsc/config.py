from movement import Coord, CoordMove

TIME = .7

coords = {
    'claw_open': Coord(4.5, 8, time=TIME),
    'claw_close': Coord(12, 2, time=TIME),
    'claw_up': Coord(2,time=TIME),
    'claw_down': Coord(9,time=TIME),
    
    'claw_store': Coord(8,time=TIME),
    'storage_down': Coord(7.4, 6.5,time=TIME),
    'storage_up': Coord(2, 10,time=TIME),
    'storage_alive': Coord(0, 10,time=TIME),
    'open_alive': Coord(2, 1.5,time=TIME),
    'open_dead': Coord(12, 6.8,time=TIME),
}

claw_arm = CoordMove(29, coords)
claw_grab = CoordMove((13, 15), coords)
storage = CoordMove((7, 11), coords)
