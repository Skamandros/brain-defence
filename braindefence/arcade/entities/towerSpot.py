class TowerSpot:
    def __init__(self, x1, y1, x2, y2, is_used=False):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.is_used = is_used

    def is_point_in_spot(self, x, y):
        return (x > self.x1) and (x < self.x2) and (y > self.y2) and (y < self.y1)
