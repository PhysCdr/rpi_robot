from gpiozero import Robot

SPEED_THRESHOLD = 1e-2

class DiffDrive(Robot):
	"""docstring for DiffDrive"""
	def __init__(self, left_pins, right_pins):
		super().__init__(left_pins, right_pins)


	def go(self, l_speed, r_speed):
		if abs(l_speed) < SPEED_THRESHOLD:
			self.left_motor.stop()
		elif l_speed > 0:
			self.left_motor.forward(l_speed)
		elif l_speed < 0:
			self.left_motor.backward(abs(l_speed))

		if abs(r_speed) < SPEED_THRESHOLD:
			self.right_motor.stop()
		elif r_speed > 0:
			self.right_motor.forward(r_speed)
		elif l_speed < 0:
			self.right_motor.backward(abs(r_speed))
