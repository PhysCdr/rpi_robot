import numpy as np
import matplotlib.pyplot as plt
from threading import Event


class OdoControl(Event):
    """Odometry commands for a Raspberry Pi robot"""

    def __init__(self, run_method=None):
    	super().__init__()
        self.l_speed = 0.0
        self.r_speed = 0.0
        self.run_method = run_method 
        self.clear()

        # plot attributes
        # self.fig, self.ax = plt.subplots()
        # self.ax.set_xlim((-1.1, 1.1))
        # self.ax.set_ylim((-1.1, 1.1))
        # self.left_motor, = self.ax.plot([], [], color='blue', linewidth=6.0)
        # self.right_motor, = self.ax.plot([], [], color='red', linewidth=6.0)
        # self.fig.canvas.draw()
        # self.ax_bckgrnd = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        # plt.show(block=False)

    def get_speeds(self):
        return (self.l_speed, self.r_speed)

    def set_speeds(self, **kwargs):
    	self.clear()
        for key, value in kwargs.items():
            if key == 'l_speed':
                self.l_speed = value
            if key == 'r_speed':
                self.r_speed = value
        self.set()

    # def plot_state(self):
    #     self.left_motor.set_data([-0.5, -0.5], [0, self.l_speed])
    #     self.right_motor.set_data([0.5, 0.5], [0, self.r_speed])
    #     # restore background
    #     self.fig.canvas.restore_region(self.ax_bckgrnd)

    #     # redraw just vec
    #     self.ax.draw_artist(self.left_motor)
    #     self.ax.draw_artist(self.right_motor)

    #     # fill in the axes rectangle
    #     self.fig.canvas.blit(self.ax.bbox)
    #     self.fig.canvas.flush_events()


    def js_axis_to_lr_speeds(self, joystick):
        """
        Convert the joystick axis state (x,y) to left and right motor speeds
        """
        _, axis_states = joystick.get_state()
        x, y = axis_states['rx'], axis_states['ry']
        if np.allclose(x, 0) and np.allclose(y, 0):
            phi = 0
        elif np.allclose(x, 0):
            phi = np.pi / 2 * np.sign(y)
        else:
            if x > 0 and y >= 0:
                phi = np.arctan(y / x)
            elif (x < 0 and y >= 0) or (x < 0 and y <= 0):
                phi = np.pi + np.arctan(y / x)
            elif x > 0 and y <= 0:
                phi = 2 * np.pi + np.arctan(y / x)

        v = np.sqrt(x**2 + y**2)
        phi_r = phi + np.pi / 4
        phi_l = phi - np.pi / 4
        heaviside = np.abs(np.cos(phi_r)) >= np.cos(np.pi / 4)
        self.r_speed = -v * np.sign(np.cos(phi_r)) * heaviside - \
                                    v * np.cos(phi_r) / \
                                               np.cos(np.pi / 4) * (1 - heaviside)
        heaviside = np.abs(np.cos(phi_l)) >= np.cos(np.pi / 4)
        self.l_speed = v * np.sign(np.cos(phi_l)) * heaviside + \
                                   v * np.cos(phi_l) / np.cos(np.pi / 4) * \
                                              (1 - heaviside)

    def send_joystick_control(self, js_event):
        while True:
        	self.clear()
            js_event.wait()
            self.js_axis_to_lr_speeds(js_event)
            if self.run_method:
            	self.run_method((self.l_speed, self.r_speed))
            #self.plot_state()
            js_event.clear()
            self.set()

    def receive_control(self, ctl_event):
        while True:
        	self.clear()
            ctl_event.wait()
            if self.run_method:
            	(self.l_speed, self.r_speed) = self.run_method()
            #self.plot_state()
            ctl_event.clear()
            self.set()
