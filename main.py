import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.graphics import Rectangle, Color, Rotate, PushMatrix, PopMatrix

from Modules import Adapter

PATH = "." + "/resources/"

import os
os.environ['KIVY_INPUT'] = 'mouse,multitouch_on_demand'

class Horizon(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle  = 0
            self.rot.origin = self.center
            self.rot.axis = (0, 0, 1)

        with self.canvas.after:
            PopMatrix()

        self.source = PATH + "Background.png"
        self.reload()

        self.texture_size = 1920*2.5, 1080*2
        self.fit_mode = "contain"
        self.size = 1920*2.5, 1080*2

        self.center = 1920//2, 1080//2

        self.angle = 0
        self.rot.origin = self.center

        #self.animate()

    def animate(self):
        self.anim = Animation(angle=self.angle, duration=0)
        self.anim.bind(on_complete=self.update_anim)
        self.anim.repeat = False
        self.anim.start(self.rot)

    def update_anim(self, *kargs):
        #self.animate()
        pass


class SimpleApp(App):
    def build(self):
        Window.fullscreen = 'auto'
        self.root = Widget()

        self.mav = Adapter.Adapter("udp:0.0.0.0:14550")

        self.horizon = Horizon()

        self.root.add_widget(self.horizon)

        Clock.schedule_interval(self.update_mav, 0)

        return self.root
    
    def update_mav(self, dt):
        self.mav.update()
        if self.mav.data["heading"] != None:
            self.horizon.rot.angle = self.mav.data["attitude"]["roll"]
        print(self.mav.data)

    def ok2(self, dt):
        pass

if __name__ == '__main__':
    SimpleApp().run()
