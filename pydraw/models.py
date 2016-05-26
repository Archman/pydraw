#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
classes for models, e.g. Particle

Tong Zhang
2016-05-24 20:56:57 PM CST
"""

import random
import wx
import numpy as np
import time
import threading

class Particle(object):
    def __init__(self, x, y, radius=1.0, color=None):
        self._x = x
        self._y = y
        self._r = radius
        if color is None:
            self._color = wx.Colour(0,0,255,200)
        else:
            self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @staticmethod
    def gen_rand_color(mode='rgb', alpha=255):
        if mode == 'rgb':
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            c = wx.Colour(r, g, b, alpha=alpha)
            return c
        elif mode == 'hex':
            alp = '0123456789ABCDEF'
            c = '#' + ''.join([random.choice(alp) for i in range(6)])
            return c

class Simulator(object):
    def __init__(self, parent, particles, buffer, color):
        """ input all defined particles
        """
        self.pframe = parent
        self.show_trace = self.pframe.show_trace
        self.particles = particles
        self.buffer = buffer
        self.color = color

    def draw(self):
        """
        draw all particle to dc
        """
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        for p in self.particles:
            dc.SetPen(wx.Pen(p.color, width=1))
            dc.SetBrush(wx.Brush(p.color))
            dc.DrawCircle(int(p.x), int(p.y), p.r)
        self.pframe.Refresh(False)

    def clear(self, show_trace=False):
        if not show_trace:
            dc = wx.MemoryDC()
            dc.SelectObject(self.buffer)
            dc.SetBackground(wx.Brush(self.color))
            dc.Clear()
            self.pframe.Refresh(False)

class RandomWalker(Simulator):
    def __init__(self, parent, particles, buffer, color, steps=10, dt=0.05):
        Simulator.__init__(self, parent, particles, buffer, color)
        self.steps  = steps
        self.dt     = dt

        p0 = converge_particle = random.choice(self.particles)
        other_particles = [p for p in self.particles if p != p0]
        self.delx = [1./random.randint(1,steps)*(p0.x-pi.x) for pi in other_particles]
        self.dely = [1./random.randint(1,steps)*(p0.y-pi.y) for pi in other_particles]
        self.other_particles = other_particles

        self.mode = random.choice(['cop', 'dop', 'col1', 'col2'])
        self.move_func = {
                          'cop' : self._move_cop,
                          'dop' : self._move_dop,
                          'col1': self._move_col1,
                          'col2': self._move_col2
                         }

    def move(self, n=None):
        self.move_func[self.mode]()

    def _move_cop(self):
        for idx, p in enumerate(self.other_particles):
            p.x -= self.delx[idx]
            p.y -= self.dely[idx]

    def _move_dop(self):
        for idx, p in enumerate(self.other_particles):
            p.x += self.delx[idx]
            p.y += self.dely[idx]

    def _move_col1(self):
        for idx, p in enumerate(self.other_particles):
            p.x -= self.delx[idx]
            p.y += self.dely[idx]

    def _move_col2(self):
        for idx, p in enumerate(self.other_particles):
            p.x += self.delx[idx]
            p.y -= self.dely[idx]

class WorkerThread(threading.Thread):
    def __init__(self, model):
        threading.Thread.__init__(self)
        self.model = model
        self.setDaemon(True)
        self.stopflag = threading.Event()
        self.stopflag.clear()

    def stop(self):
        self.stopflag.set()
    
    def run(self):
        for i in range(self.model.steps):
            if self.stopflag.isSet():
                break
            self.model.move(i)
            wx.CallAfter(self.model.clear, self.model.show_trace)
            wx.CallAfter(self.model.draw)
            time.sleep(self.model.dt/1000.0)

class RobotDrawer(Simulator):
    def __init__(self, parent, particles, buffer, color, steps=10, dt=0.05):
        Simulator.__init__(self, parent, particles, buffer, color)
        self.steps = steps
        self.dt    = dt
        self.gen_rot_center()
    
    def gen_rot_center(self):
        r_np = np.array([p.r*random.choice(range(2,15)) for p in self.particles])
        theta_np = np.random.choice(np.linspace(0, 2*np.pi, 180), r_np.size)
        cos, sin = np.cos, np.sin
        self.omega = 2*np.pi/(np.random.choice(range(10, self.steps), r_np.size))
        self.r     = r_np
        self.theta = theta_np
        self.r_omega = self.r * self.omega
        self.r_omega = self.r * self.omega

    def move(self, n=None):
        for i, p in enumerate(self.particles):
            p.x += self.r_omega[i] * np.sin((self.theta[i] - self.omega[i] * n))
            p.y -= self.r_omega[i] * np.cos((self.theta[i] - self.omega[i] * n))

    def draw(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        for p in self.particles:
            dc.SetPen(wx.Pen(p.color))
            dc.SetBrush(wx.Brush(p.color))
            dc.DrawCircle(int(p.x), int(p.y), p.r)
        self.pframe.Refresh(False)



