import RPi.GPIO as g
import time


def servoRun(pin, frequency, angle):
    # Set the gpio mode
    g.setmode(g.BCM)

    # Use a certain pin
    g.setup(pin, g.OUT)

    # pwm = Pulse Width Modulation
    # Set up pin 17 to send pulses 50 times per second
    pwm = g.PWM(pin, frequency)

    # Start the pulses
    pwm.start(0)

    # Send output
    g.output(pin, True)

    # length of pulse/period = duty cycle
    # frequency = 1/period
    # length*frequency = duty cycle
    # duty cycle = 0 - 100% => 0 - 180 degrees
    # angle*(100/180) = duty cycle

    duty = angle/1.8

    # Change by 100
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

    g.output(pin, False)
    g.cleanup()
