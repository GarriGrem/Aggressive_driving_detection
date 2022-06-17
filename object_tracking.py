class VehiclesParameters:
    def __init__(self):
        self.prev_point = []
        self.vehicles_speed_prev = {}
        self.vehicles_rating = {}
        self.tracking_objects = {}
        self.pixelsPerFrame = {}
        self.vehicles_frames = {}
        self.vehicles_speed_cur = {}
        self.vehicles_acceleration = {}
        self.vehicles_distance = {}
        self.vehicles_trajectory = {}
        self.track_id = 0

    def add_new_vehicle(self, track_id, current_points):
        for pt in current_points:
            self.vehicles_rating[track_id] = 'safe'
            self.vehicles_speed_prev[track_id] = 0
            self.vehicles_acceleration[track_id] = 0
            self.vehicles_trajectory[track_id] = 0
            self.vehicles_distance[track_id] = 0
            self.vehicles_frames[track_id] = 0
            self.pixelsPerFrame[track_id] = 0
            self.vehicles_speed_cur[track_id] = 0
            self.tracking_objects[track_id] = pt
            self.track_id += 1

    def remove_vehicle(self, object_id):
        self.vehicles_rating.pop(object_id)
        self.vehicles_trajectory.pop(object_id)
        self.tracking_objects.pop(object_id)
        self.vehicles_frames.pop(object_id)
        self.pixelsPerFrame.pop(object_id)
        self.vehicles_distance.pop(object_id)
        self.vehicles_speed_cur.pop(object_id)
        self.vehicles_acceleration.pop(object_id)
