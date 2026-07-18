import asyncio
import app
import math

from .flag import *

from tildagonos import tildagonos, led_colours
from system.eventbus import eventbus
from system.patterndisplay.events import *
from events.input import Buttons, BUTTON_TYPES

class RoundPride(app.App):

    currentFlag = 0
    startIndex = 0
    startLed = 0
    brightness = 1
    freq = 1


    def updateLeds(self):

        toDraw = flags[self.currentFlag % len(flags)]

        for i in range(0, 12):
            colour = [0, 0, 0]
            index = (self.startIndex + i * 10) % 120
            colour[0] = round(toDraw.ledLoop[index][0] * self.brightness)
            colour[1] = round(toDraw.ledLoop[index][1] * self.brightness)
            colour[2] = round(toDraw.ledLoop[index][2] * self.brightness)
            tildagonos.leds[(i + self.startLed) % 12 + 1] = colour

        tildagonos.leds.write()
        self.startIndex = int(self.startIndex + 120/(self.freq+12)) % 120
        self.startLed = (self.startLed + 1) % 12


    def __init__(self):
        self.button_states = Buttons(self)
        eventbus.emit(PatternDisable())

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()
            self.minimise()
        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.button_states.clear()
            # Add an overlay rectangle
            self.currentFlag = self.currentFlag + 1
        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.button_states.clear()
            # Remove an overlay rectangle
            self.currentFlag = self.currentFlag - 1
        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            self.brightness = self.brightness + 0.1 if self.brightness < 1 else 1
        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            self.brightness = self.brightness - 0.1 if self.brightness > 0 else 0
        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()
            self.freq = (self.freq + 1)
            if self.freq > 6:
                self.freq = 1;

        self.updateLeds()

    def background_update(self, delta):
        self.updateLeds()


    def draw(self, ctx):

        toDraw = flags[self.currentFlag % len(flags)]
        bands = len(toDraw.colours)
        for i in range(bands):
            colour = toDraw.colours[i]
            radius = 120 * (bands-i)/bands
            ctx.save()
            ctx.rgb(colour[0]/255, colour[1]/255, colour[2]/255)
            ctx.arc(0, 0, radius, 0, 2*math.pi, True).fill()
            ctx.restore()



__app_export__ = RoundPride
