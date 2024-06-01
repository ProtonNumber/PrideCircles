import asyncio
import app
import math
from tildagonos import tildagonos, led_colours

from system.eventbus import eventbus
from system.patterndisplay.events import *

from events.input import Buttons, BUTTON_TYPES

class Image:
    path = ""
    pos = (0, 0)
    dims = (0, 0)

    def __init__ (self, path, pos, dims):
        self.path = path
        self.pos = pos
        self.dims = dims

class Flag:
    colours = [] # The colours, as [R, G, B] from the outside to the inside
    image = None

    def __init__(self, colours, image):
        self.colours = colours
        self.image = image



class RoundPride(app.App):

    flags = [
        Flag([[228, 3, 3], [255, 140, 0], [255, 237, 0],             # Pride
              [0, 128, 38], [36, 64, 142], [15, 41, 130]], None),    # Will add progress when images work
        Flag([[91,206,250], [245,169,184], [255,255,255]], None),    # Trans
        Flag([[252, 244, 52], [255, 255, 255], [156, 89, 209],       # Enby
              [44, 44, 44]], None),
        Flag([[214, 2, 112], [214, 2, 112], [155, 79, 150],          # Bi
              [0, 56, 168], [0, 56, 168]], None), #
        Flag([[213, 45, 0], [239, 118, 39], [255, 154, 86],          # Lesbian
              [255, 255, 255], [209, 98, 164], [181, 86, 144], [163, 2, 98]], None),
        Flag([[255, 216, 0], [255, 216, 0], [121, 2, 170],           # Intersex
              [255, 216, 0], [255, 216, 0]], None),
        Flag([[7, 141, 112], [38, 206, 170], [152, 232, 193],        # MLM
              [255, 255, 255], [123, 173, 226], [80, 73, 204], [61, 26, 120]], None),
        Flag([[253, 139, 168], [251, 242, 255], [199, 107, 197],
              [253, 215, 104]],                                      # Sapphic
             Image("/apps/pridecircles/sapphic.png", (-50, 50), (100, 100))),
        Flag([[255, 33, 140], [255, 216, 0], [33, 177, 255]], None), # Pan
        Flag([[0, 0, 0], [163, 163, 163], [255, 255, 255],           # Ace
              [128, 0, 128]], None),
        Flag([[255, 118, 164], [255, 255, 255], [192, 17, 215],      # Genderfluid
              [0, 0, 0], [47, 60, 190]], None)


    ]
    currentFlag = 0
    startLed = 0
    ledLoop = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def placeBand(self, n, t):
        return round((12/(t)*(n)))

    def generateLoop(self):
        flag = self.flags[self.currentFlag % len(self.flags)]
        bands = len(flag.colours)
        for i in range(bands):
            currentPos = self.placeBand(i, bands)
            nextPos = self.placeBand(i+1, bands)
            delta = nextPos-currentPos

            startColour = flag.colours[i]
            endColour = flag.colours[(i+1)%bands]

            rstep = (endColour[0]-startColour[0])/delta
            gstep = (endColour[1]-startColour[1])/delta
            bstep = (endColour[2]-startColour[2])/delta


            self.ledLoop[self.placeBand(i, bands)] = startColour
            for j in range(delta):
                self.ledLoop[currentPos+j] = [round(startColour[0] + rstep * j),
                                              round(startColour[1] + gstep * j),
                                              round(startColour[2] + bstep * j)]

    def __init__(self):
        self.button_states = Buttons(self)
        self.generateLoop()
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
            self.generateLoop()
        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.button_states.clear()
            # Remove an overlay rectangle
            self.generateLoop()
            self.currentFlag = self.currentFlag - 1

        for i in range(0, 12):
            tildagonos.leds[(i + self.startLed) % 12 + 1] = self.ledLoop[i]

        self.startLed = (self.startLed + 1) % 12

        # Lazy fix for a concurrency issue. Hopefully your battery doesnt mind.
        self.generateLoop()


    def draw(self, ctx):

        flag = self.flags[self.currentFlag % len(self.flags)]
        bands = len(flag.colours)
        for i in range(bands):
            colour = flag.colours[i]
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
