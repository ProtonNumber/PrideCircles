class Image:
    path = ""
    pos = (0, 0)
    dims = (0, 0)

    def __init__ (self, path, pos, dims):
        self.path = path
        self.pos = pos
        self.dims = dims

class Flag:
    def placeBand(self, n, t):
        return round((12/(t)*(n)))

    def __init__(self, colours, image):
        self.colours = colours
        self.image = image
        self.ledLoop = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

        bands = len(self.colours)

        for i in range(bands):
            currentPos = self.placeBand(i, bands)
            nextPos = self.placeBand(i+1, bands)
            delta = nextPos-currentPos

            startColour = self.colours[i]
            endColour = self.colours[(i+1)%bands]

            rstep = (endColour[0]-startColour[0])/delta
            gstep = (endColour[1]-startColour[1])/delta
            bstep = (endColour[2]-startColour[2])/delta

            self.ledLoop[self.placeBand(i, bands)] = startColour
            for j in range(delta):
                self.ledLoop[currentPos+j] = [round(startColour[0] + rstep * j),
                                              round(startColour[1] + gstep * j),
                                              round(startColour[2] + bstep * j)]

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
