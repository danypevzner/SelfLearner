import time
from zmqRemoteApi import RemoteAPIClient

class Robot:
    SPEED_BOOST = 1

    def __init__(self, sim, robot_name):
        self._start_time = time.time()

        def init_sensors():
            _ = self._get_sensor_data(self._sensor)


        self.name = robot_name
        self.sim = sim
        self._sensor = self.sim.getObject('/' + self.name + '/FRONTSENS')
        init_sensors()

    def _get_sensor_data(self, sensor):
        sensor_output = ['result',
                         'distance',
                         'detectedPoint',
                         'detectedObjectHandle',
                         'detectedSurfaceNormalVector']
        return {sensor_output[i]: sim.readProximitySensor(sensor)[i] for i in range(len(sensor_output))}

    def _wall_detection(self):
        return self._get_sensor_data(self._sensor)['distance'], self._get_sensor_data(self._sensor)['result']


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
            distance, result = self._wall_detection()
            print( result, distance)
            if result and (distance < 0.3):
                self._set_movement(0, 0, 0)
                break
            else:
                self._set_movement(self.SPEED_BOOST * 1, 0, 0)
            # print(self._get_sensor_data(self._sensor))


client = RemoteAPIClient()
sim = client.getObject('sim')

client.setStepping(False)

sim.startSimulation()
while (t := sim.getSimulationTime()) < 10:
    s = f'Simulation time: {t:.2f} [s]'
    # print(s)
robot = Robot(sim, 'youBot')
if sim.getSimulationTime() > 1:
    robot.start()
