# Animation Sketch

![Anim Sketch Demo](/images/demo.gif?raw=true)

Anim Sketch is a motion recording tool that allows for quick and inuitive animation creation through direct user input. The tool is functionally similar to motion sketch in Adobe After Effects and supports direct positon recording as well as channel box recording. 

Originally built for a commercial project at [Hero4Hire Creative](http://www.hero4hirecreative.com/), the studio has since given me permission to update and release the source code under the MIT license. 

## Origin

While other free tools exist elsewhere at the time, we were unable to find a motion sketching solution that was functionally complete and did not accept compromises. The two main issues we found with most tools were:
* It was unable to record stationary input. This was vital to recording a believable performance with natural pauses.
* It did not support undo on a per-recording basis. Some tools made use of Maya's built in `recordAttr()` function, however this does not support native undoing and was a dealbreaker for recording anything of considerable length.

This tool was built without compromise and performs as one would expect.

## Usage
There are two main functions of the tool. *Record Position* and *Record Channel*. 

*Record Position* will use drag input to offset the world space position of the target. This is a 1:1 transfer, the target will move in the scene the exact amount dragged in screenspace.

*Record Channel* will use drag input to offset a selected channel in the channel box. A *Sensitivity* setting determines the ratio of change between the two. There are settings to change the drag direction as well as a setting to invert the direction if needed.

The *Simplify Curves* checkbox will apply a simplify filter on the curves after recording. The *Simplify Tolerance* setting will determine the how simplified the curves will be.

## Installation

1. Download a .zip of the project and extract the 'animSketch' folder to you maya scripts directory
2. Open the python script editor and run this:

```
from animSketch import animSketch_maya
animSketch_maya.load()
```

## License

MIT License

Copyright (c) 2017 HERO4HIRE CREATIVE LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.