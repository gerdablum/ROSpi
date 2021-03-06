import TOFSensors
import SRF02_rangefinder as SRF02

import Engine
import Servos
from TOFSensors import State
import time

import atexit


def stop_at_exit(engine):
    """
    Stops all wheels when exiting program.
    :param engine:
    :return:
    """
    engine.stop_all_wheels()


def main():
    """
    Main method of the project. Starts with an init procedure and calls the functions of the used sensors in an
    infinite loop. Waits a short time after one loop step.
    :return:
    """
    # Create objects for each used sensor or actuator
    sensors = TOFSensors.TOFSensors()
    engine = Engine.Engine()
    servos = Servos.Servos()
    rf = SRF02.SRF02()

    atexit.register(stop_at_exit, engine)

    # Short init phase where wheels are rotating backwards and forwards and servos moving up and down.
    engine.move_all_wheels_forward(40)
    servos.both_servos_down()
    servos.front_servo_forward()
    time.sleep(1)
    engine.move_all_wheels_backward(40)
    servos.both_servos_forward()
    time.sleep(1)
    engine.stop_all_wheels()
    servos.both_servos_down()


    while (1):
        rf.run()
        sensors.run()
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_right_sensor.name,
                                                                 sensors.state_left_sensor.name))

        print("State RF: {}".format(rf.srf02_state.name))

        if rf.srf02_state is State.BLOCKED:

            engine.turn_around_left()

        elif sensors.state_left_sensor is State.BLOCKED:
            engine.move_all_wheels_backward(30)
            time.sleep(1.5)
            engine.turn_around_right()
            time.sleep(1.5)

        elif sensors.state_right_sensor is State.BLOCKED:
            engine.move_all_wheels_backward(30)
            time.sleep(1.5)
            engine.turn_around_left()
            time.sleep(1.5)

        else:
            engine.move_all_wheels_forward(40)

        time.sleep(0.1)


if __name__ == '__main__':
    main()
