#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Drawing application for fun.

    Tong Zhang
    2016-05-24 15:30:04 PM CST
"""

import wx
import random
import models
import time

class DrawFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        
        self.mode_list = ['Random Walker', 'Robot Drawer']
        self.mode = self.mode_list[0]
        self.paint_modes = {
                            'Random Walker': self._drawCircles,
                            'Robot Drawer' : self._drawRobot,
                           }
        self.fmt='%Y-%m-%d %H:%M:%S %Z'
        self.npart = 2000
        self.stop_ms = 50  # 50 millisecond
        self.show_trace = False

        self.initUI()

        self.time_now = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTickTime, self.time_now)
        self.time_now.Start(1000)

        self.initBuffer()

    def onTickTime(self, event):
        self.time_now_st.SetLabel(time.strftime(self.fmt, time.localtime()))

    def initUI(self):
        sb = wx.StaticBox(self, label='Drawing Canvas', style=wx.ALIGN_CENTER)
        sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)

        draw_btn  = wx.Button(self, label='&Draw')
        start_btn = wx.Button(self, label='&Start')
        stop_btn  = wx.Button(self, label='Sto&p')
        exit_btn  = wx.Button(self, label='&Exit')
        about_btn = wx.Button(self, label='&About')
        clear_btn = wx.Button(self, label='&Clear')

        mode_cb = wx.ComboBox(self, value=self.mode_list[0], 
                    choices=self.mode_list, style=wx.CB_READONLY)
        npart_st = wx.StaticText(self, label=u'Particle Number')
        npart_tc = wx.TextCtrl(self, value=str(self.npart), style=wx.TE_PROCESS_ENTER)
        trace_ck = wx.CheckBox(self, label=u'Trace')
        speed_st = wx.StaticText(self, label=u'Speed')
        speed_sp = wx.SpinCtrl(self, value='20', min=1, max=100, initial=20)
        fract_st = wx.StaticText(self, label=u'Shape')
        fract_cb = wx.ComboBox(self, value=u'Circle', choices=['Circle','Koch'],
                               style=wx.CB_READONLY)
        self.npart_st  = npart_st
        self.npart_tc  = npart_tc
        self.trace_ck  = trace_ck
        self.speed_sp  = speed_sp
        self.start_btn = start_btn
        self.draw_btn  = draw_btn
        self.fract_cb  = fract_cb
        self.fract_st  = fract_st
        self.fract_cb.Hide()
        self.fract_st.Hide()
        
        self.hbox1 = hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(mode_cb,  0, wx.TOP | wx.BOTTOM, 6)
        hbox1.Add(npart_st, 0, wx.TOP | wx.BOTTOM | wx.LEFT | wx.ALIGN_CENTER, 6)
        hbox1.Add(npart_tc, 0, wx.LEFT | wx.ALIGN_CENTER, 6)
        hbox1.Add(fract_st, 0, wx.TOP | wx.BOTTOM | wx.LEFT | wx.ALIGN_CENTER, 6)
        hbox1.Add(fract_cb, 0, wx.LEFT | wx.ALIGN_CENTER, 6)
        hbox1.Add(trace_ck, 0, wx.LEFT | wx.ALIGN_CENTER, 10)
        hbox1.Add(speed_st, 0, wx.LEFT | wx.ALIGN_CENTER, 10)
        hbox1.Add(speed_sp, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 6)
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(draw_btn,  0, wx.TOP | wx.BOTTOM, 6)
        hbox2.Add(start_btn, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 6)
        hbox2.Add(stop_btn,  0, wx.TOP | wx.BOTTOM | wx.LEFT, 6)
        hbox2.Add(clear_btn, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 6)
        hbox2.Add(exit_btn,  0, wx.TOP | wx.BOTTOM | wx.LEFT, 6)
        hbox2.Add(about_btn, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 6)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(hbox1, 1, wx.ALIGN_LEFT)
        hbox.Add(hbox2, 0, wx.ALIGN_RIGHT)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#EDECEB')
        self.color = self.panel.GetBackgroundColour()
        sbs.Add(self.panel, 1, wx.EXPAND)
        
        title_st = wx.StaticText(self, label=u'Welcome to Game World!')
        font = title_st.GetFont()
        font.SetPointSize(20)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        font.SetFaceName('Comic Sans MS')
        title_st.SetFont(font)
        title_st.SetForegroundColour(models.Particle.gen_rand_color(mode='hex'))
        self.time_now_st = wx.StaticText(self, label=time.strftime(self.fmt, time.localtime()))

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(title_st,         0, wx.ALIGN_CENTER | wx.TOP, 5)
        vbox.Add(self.time_now_st, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        vbox.Add(sbs,  4, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON,     self.onExit,       exit_btn )
        self.Bind(wx.EVT_BUTTON,     self.onDraw,       draw_btn )
        self.Bind(wx.EVT_BUTTON,     self.onStart,      start_btn)
        self.Bind(wx.EVT_BUTTON,     self.onStop,       stop_btn )
        self.Bind(wx.EVT_BUTTON,     self.onClear,      clear_btn)
        self.Bind(wx.EVT_BUTTON,     self.onAbout,      about_btn)
        self.Bind(wx.EVT_COMBOBOX,   self.onChooseMode, mode_cb  )
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnterN,     npart_tc )
        self.Bind(wx.EVT_CHECKBOX,   self.onTraceBool,  trace_ck )
        self.Bind(wx.EVT_SPINCTRL,   self.onSpeed,      speed_sp )

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE,  self.onSize)
        self.Bind(wx.EVT_IDLE,  self.onIdle)

    def onAbout(self, e):
        dlg = wx.MessageDialog(self, "This app is created just for fun\n(Tong Zhang, May. 2016)", 
                caption='About This App', 
                style=wx.OK | wx.CANCEL | wx.ICON_INFORMATION | wx.CENTER)
        if dlg.ShowModal() == wx.OK:
            dlg.Destroy()
        else:
            img = self.buffer.ConvertToImage()
            img.SaveFile('pic.png', wx.BITMAP_TYPE_PNG)
    
    def onSpeed(self, e):
        self.stop_ms = 1000.0/int(self.speed_sp.GetValue())

    def onEnterN(self, e):
        self.npart = int(self.npart_tc.GetValue())
        self.initBuffer()
        self.draw()
    
    def onTraceBool(self, e):
        if e.GetEventObject().IsChecked():
            self.show_trace = True
        else:
            self.show_trace = False

    def onChooseMode(self, e):
        self.mode = e.GetEventObject().GetStringSelection()
        if self.mode == 'Robot Drawer':
            #self.draw_btn.Hide()
            self.npart_st.SetLabel('Robot Number')
            self.npart = 20
            self.npart_tc.SetValue(str(self.npart))
            self.trace_ck.Hide()
            self.fract_cb.Show()
            self.fract_st.Show()
            self.Layout()
        else:
            #self.draw_btn.Show()
            self.npart_st.SetLabel('Particle Number')
            self.npart = 2000
            self.npart_tc.SetValue(str(self.npart))
            self.trace_ck.Show()
            self.fract_cb.Hide()
            self.fract_st.Hide()
            self.Layout()

    def onClear(self, e):
        self.clear()

    def clear(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.SetBackground(wx.Brush(self.color))
        dc.Clear()
        self.Refresh(False)

    def onExit(self, e):
        dlg = wx.MessageDialog(self, 'Go back to play?', caption='Exit Warning',
                               style=wx.YES_NO | wx.ICON_QUESTION | wx.CENTER)
        if dlg.ShowModal() == wx.ID_NO:
            self.Destroy()

    def onStart(self, e):
        self.paint()
        
    def onStop(self, e):
        try:
            self.randomModel_worker.stop()
        except:
            pass

    def onDraw(self, e):
        self.initBuffer()
        self.draw()

    def onIdle(self, e):
        if self.reInitBuffer:
            self.initBuffer()
            self.draw()
            self.Refresh(False)

    def onSize(self, e):
        self.Layout()
        self.reInitBuffer = True
    
    def onPaint(self, event):
        dc = wx.BufferedPaintDC(self.panel, self.buffer)

    def initBuffer(self):
        size = self.panel.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.color))
        dc.Clear()
        self.reInitBuffer = False

    def draw(self):
        """ draw new particles
        """
        particles = []
        for i in range(self.npart):
            w, h = self.GetClientSize()
            x = random.randint(1, w-1)
            y = random.randint(1, h-1)
            rho = random.random()*10
            p = models.Particle(x, y, radius=rho)
            p.color = models.Particle.gen_rand_color(alpha=200)
            particles.append(p)
        self.particles = particles
        models.Simulator(self, particles, self.buffer, self.color).draw()

    def paint(self):
        self.paint_modes[self.mode]()

    def _drawCircles(self):
        randomModel = models.RandomWalker(self, self.particles, self.buffer, self.color, 200, self.stop_ms)
        self.randomModel_worker = models.WorkerThread(randomModel)
        self.randomModel_worker.start()

    def _drawRobot(self):
        self.clear()
        self.show_trace = True
        robotModel = models.RobotDrawer(self, self.particles, self.buffer, self.color, 200, self.stop_ms)
        self.robotModel_worker = models.WorkerThread(robotModel)
        self.robotModel_worker.start()
       
def run():
    app = wx.App()
    drawFrame = DrawFrame(None, -1, 'Drawing Game')
    drawFrame.Center()
    drawFrame.SetMinSize((1360, 768))
    drawFrame.SetSize((1360, 1058))
    drawFrame.Show()
    app.MainLoop()

if __name__ == '__main__':
    run()

