import asyncio
import app
import math

import apps.pridecircles.flag as flag

from tildagonos import tildagonos, led_colours
from system.eventbus import eventbus
from system.patterndisplay.events import *
from events.input import Buttons, BUTTON_TYPES

class RoundPride(app.App):

    currentFlag = 0
    startLed = 0
    brightness = 1

    def updateLeds(self):
        toDraw = flag.flags[self.currentFlag % len(flag.flags)]

        for i in range(0, 12):
            colour = [0, 0, 0]
            colour[0] = round(toDraw.ledLoop[i][0] * self.brightness)
            colour[1] = round(toDraw.ledLoop[i][1] * self.brightness)
            colour[2] = round(toDraw.ledLoop[i][2] * self.brightness)
            tildagonos.leds[(i + self.startLed) % 12 + 1] = colour

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

        self.updateLeds()

    def background_update(self, delta):
        self.updateLeds()


    def draw(self, ctx):

        toDraw = flag.flags[self.currentFlag % len(flag.flags)]
        bands = len(toDraw.colours)
        for i in range(bands):
            colour = toDraw.colours[i]
            radius = 120 * (bands-i)/bands
            ctx.save()
            ctx.rgb(colour[0]/255, colour[1]/255, colour[2]/255)
            ctx.arc(0, 0, radius, 0, 2*math.pi, True).fill()
            ctx.restore()

        # TODO: Fix this when the badge team fix image loading
        #if flag.image != None:
        #    image = flag.image
        #    ctx.save()
        #    ctx.image(image.path, image.pos[0], image.pos[1],
        #              image.dims[0], image.dims[1])
        #    ctx.restore()




__app_export__ = RoundPride
