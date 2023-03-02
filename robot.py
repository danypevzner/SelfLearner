import time
import numpy as np
from numpy import NaN
from zmqRemoteApi import RemoteAPIClient


class Robot:
    SPEED_BOOST = 4
    X_DISTANCE = 0.8

    def __init__(self, sim, robot_name):
        self._start_time = time.time()
        self.name = robot_name
        self.sim = sim

    def _get_sensor_data(self):
        result = bool(sim.getInt32Signal("r"))

        if result:
            point_abs_signal = sim.getStringSignal("pointDataAbs")
            points = sim.unpackTable(point_abs_signal)
            absolute_coords_2d = [[pt[0], pt[1]] if pt != {} else [NaN, NaN] for pt in points]

            point_rel_signal = sim.getStringSignal("pointDataRel")
            points = sim.unpackTable(point_rel_signal)
            relative_coords_2d = [pt if pt != [0, 0] else [NaN, NaN] for pt in points]

            dist_signal = sim.getStringSignal("distData")
            dists = sim.unpackTable(dist_signal)
            dists = [d if d != 0 else NaN for d in dists]
        else:
            absolute_coords_2d = [NaN] * 181
            relative_coords_2d = [NaN] * 181
            dists = [NaN] * 181

        return result, absolute_coords_2d, relative_coords_2d, dists

    def _set_movement(self, forward_back_vel, left_right_vel, rotation_vel):
        wheel_joints = [sim.getObject('/' + self.name + '/rollingJoint_fl'),
                        sim.getObject('/' + self.name + '/rollingJoint_rl'),
                        sim.getObject('/' + self.name + '/rollingJoint_rr'),
                        sim.getObject('/' + self.name + '/rollingJoint_fr')]
        sim.setJointTargetVelocity(wheel_joints[0], -forward_back_vel - left_right_vel - rotation_vel)
        sim.setJointTargetVelocity(wheel_joints[1], -forward_back_vel + left_right_vel - rotation_vel)
        sim.setJointTargetVelocity(wheel_joints[2], -forward_back_vel - left_right_vel + rotation_vel)
        sim.setJointTargetVelocity(wheel_joints[3], -forward_back_vel + left_right_vel + rotation_vel)

    def start(self):
        while 1:
            self._set_movement(self.SPEED_BOOST * 1, 0, 0)

            result, points_abs, points_rel, dists = self._get_sensor_data()

            distance = np.nanmin(dists)
            if result and (distance < self.X_DISTANCE):
                self._set_movement(0, 0, 0)
                break


client = RemoteAPIClient()
sim = client.getObject('sim')

client.setStepping(False)

sim.startSimulation()

robot = Robot(sim, 'youBot')
robot.start()
