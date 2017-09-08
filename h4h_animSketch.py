import maya.OpenMaya as om
import pymel.core as pmc
import pymel.core.datatypes as dt
import maya
import time
import math

class animSketchTool(object):
    '''
    This is the main class for the tool, this is used to keep track of all the information the tool needs.
    Calling 'create()' will initiate a new tool with the inputed settings.
    '''

    contextname = 'animSketchContext'

    def __init__(self):
        pass


    ##### Public Methods #####

    def create(self, targets, sensitivity=1.0, timeScale=1.0, singleAxis=False, simplify=True, verticalControl=True,
               tolerance=0.05, inverted=False, framerate=24):

        # Set each of the tool settings
        self.targets = targets
        self.target = pmc.PyNode(self.targets[0].split('.')[0])
        self.framerate = framerate
        self.sensitivity = sensitivity
        self.timeScale = timeScale
        self.singleAxis = singleAxis
        self.simplify = simplify
        self.verticalControl = verticalControl
        self.tolerance = tolerance
        self.playbackSlider = maya.mel.eval('$tmpVar=$gPlayBackSlider')
        self.inverted = inverted

        # Set up default input values
        self.lastInput = (0,0,0)
        self.input = 0

        # Check if an existing dragger context exists, if so, delete it
        if (pmc.draggerContext(animSketchTool.contextname, exists=True)):
            pmc.deleteUI(animSketchTool.contextname)

        # Create the dragger context. This will create a new tool that watches for drag events
        if singleAxis:

            # Determine the cursor shape based on the direction
            if self.verticalControl:
                cursor = 'dolly'
            else:
                cursor = 'track'

            # Create the dragger context with the correct space and cursor shape
            pmc.draggerContext(animSketchTool.contextname, pressCommand=self._onPress,
                           dragCommand=self._onDrag, cursor=cursor,
                           releaseCommand=self._onRelease, undoMode='step',
                           image1='/MotionBlur.png')
        else:

            # Create the dragger context with space set to 'world'
            pmc.draggerContext(animSketchTool.contextname, pressCommand=self._onPress,
                               dragCommand=self._onDrag, cursor='hand',
                               releaseCommand=self._onRelease, undoMode='step',
                               image1='/MotionBlur.png', space='world')

        # Set the currentTool
        pmc.setToolTo(animSketchTool.contextname)


    ##### Private Methods #####

    def _onIdleFrame(self, *args, **kwargs):
        '''
        This is called for every frame during a hold.
        '''

        if not self.singleAxis:

            self.lastInput = self.input

        self._setKeys()


    def _onPress(self):
        '''
        This is called when the tool is first pressed down.
        Here we'll grab some initial values and create the callback
        '''

        # Grab the initial press position, we'll use this for reference
        self.pressPosition = pmc.draggerContext(animSketchTool.contextname, query=True, anchorPoint=True)

        # Create the timer callback, this will watch idle events when held down
        # We'll grab a reference to the id to remove later
        self.callbackID = om.MTimerMessage.addTimerCallback(1/self.framerate, self._onIdleFrame)

        # Grab the start time, this way we can track the duration of the hold
        self.startTime = time.time()

        # Grab the current frame in the timeline to start from
        self.startFrame = pmc.currentTime(q=True)

        # Grab the start value for each target
        self.targetStartValues = [pmc.getAttr(target) for target in self.targets]

        # Set the initial input value
        if self.singleAxis:
            self.input = 0
        else:
            self.lastInput = self.input
            self.input = self.pressPosition

        # Set a keyframe at the frame just before the startFrame
        for target in self.targets:
            pmc.setKeyframe(target, t=self.startFrame)

        # Begin the scrub, this way sound will play
        pmc.timeControl(self.playbackSlider, edit=True, beginScrub=True)


    def _onDrag(self):
        '''
        This is called when the tool is dragged.
        Here we want to record the drag change then set a keyframe on the target attributes.
        '''

        # Grab the drag position
        dragPosition = pmc.draggerContext(animSketchTool.contextname, q=True, dragPoint=True)

        if self.singleAxis:
            # Subtract the initial position to get the difference
            if self.verticalControl:
                delta = dragPosition[1] - self.pressPosition[1]
            else:
                delta = dragPosition[0] - self.pressPosition[0]

            # If inverted, reverse the delta
            if self.inverted:
                delta *= -1

            # Scale the value and set the input value
            self.input = delta/(100/self.sensitivity)
        else:
            self.lastInput = self.input
            self.input = dragPosition

        # Set a keyframe
        self._setKeys()


    def _onRelease(self):
        '''
        This is called when the tool is released.
        Here we'll remove our callback and cleanup everything.
        '''

        # Remove the callback
        om.MMessage.removeCallback(self.callbackID)

        # Set the current tool to the move tool
        pmc.setToolTo('moveSuperContext')

        # Simplify the animation curves
        if self.simplify:
            for target in self.targets:
                pmc.filterCurve(target, f='simplify', startTime=self.startFrame,
                                endTime=pmc.currentTime(q=True), timeTolerance=self.tolerance)

        # End the scrub
        pmc.timeControl(self.playbackSlider, edit=True, endScrub=True)


    def _setKeys(self):
        '''
        This sets a keyframe for each target attribute.
        '''

        # Calculate the ammount of time since the intitial press
        currentTime = time.time()
        deltaTime = (currentTime - self.startTime) * self.timeScale

        # Grab the frame to be keyed
        # We find this by finding the current frame decimal and rounding down
        frame = math.floor(deltaTime * self.framerate) + self.startFrame

        if self.singleAxis:
            # For each target attribute...
            for target in self.targets:

                    # Grab the start value
                    startValue = self.targetStartValues[self.targets.index(target)]

                    # Set the new value based on the input and the start input
                    pmc.setAttr(target, self.input + startValue, clamp=True)

        else:

            startVector = dt.Vector(self.lastInput[0], self.lastInput[1], self.lastInput[2])
            currentVector = dt.Vector(self.input[0], self.input[1], self.input[2])

            self.target.translateBy(currentVector-startVector, space='world')


        # Set a keyframe on each target
        for target in self.targets:
            if not pmc.getAttr(target, lock=True):
                pmc.setKeyframe(target, t=frame)

        # Move the current time forward
        pmc.currentTime(frame)
