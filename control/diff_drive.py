from gpiozero import Robot

SPEED_THRESHOLD = 1e-2

class DiffDrive(Robot):
	"""docstring for DiffDrive"""
	def __init__(self, left_pins, right_pins):
		super().__init__(left_pins, right_pins)


	def go(self, l_speed, r_speed):
		if abs(l_speed) < SPEED_THRESHOLD:
			left_func = lambda l_speed: self.left_motor.stop()
		elif l_speed > 0:
			left_func = lambda l_speed: self.left_motor.forward(l_speed)
		elif l_speed < 0:
			left_func = lambda l_speed: self.left_motor.backward(-l_speed)

		if abs(r_speed) < SPEED_THRESHOLD:
			right_func = lambda r_speed: self.right_motor.stop()
		elif r_speed > 0:
			right_func = lambda r_speed: self.right_motor.forward(r_speed)
		elif r_speed < 0:
			right_func = lambda r_speed: self.right_motor.backward(-r_speed)

		left_func(l_speed)
		right_func(r_speed)
