# VTuber
Simple Python application which can be used on several platforms like Twitch, YouTube, Microsoft Teams, Zoom and so on. While this can be useful and fun for content creation, I made this to help out teachers during COVID, as it can be hard and depressing to talk and listen to students while looking at static images. 

I also don't have a webcam (and probably wouldn't use it if I did), so that was also another reason for making this.

---

### To-Do
Currently the focus is to extend it a bit more, simplify code and improve user-friendliness. There's also a couple of optimizations to be made. But so far there's:  
- [x] Basic animations
- [x] Basic costumes
- [x] Support for different stages
- [x] Volume specific frames (animations on specific mic volume)

These are the current features/changes I want to make:  
- [ ] Add image resizing
- [ ] Add user-friendly volume setup
- [ ] Improve animation support (avatars, frames/steps)
- [ ] Improve costume support (loading, displaying, keybinds)
- [ ] Improve/simplify stage system

---

### Requirements
- Python 3+
	- PIL / pillow
	- pygame
	- pyaudio (requires Visual Studio 2014+ C++ Build Tools _(for some stupid reason)_)
	- aubio
	- numpy
- OBS (Open Broadcaster Software)

### Installation  
The Python modules can be installed with:   
`pip install pillow, pygame, numpy, pyaudio, aubio`

---

Due to pip being trash at times, you might have problems with installing `pyaudio` on Windows. Open your console > type `python` > take note of the version:

```
Python 3.9.0 (...) [MSC v.1927 64 bit (AMD64)] on win32
                               ^^^^^^^^^^^^^^
```

Then go to [PyAudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and download the matching .whl file. Then run `pip install <filename.whl>` to install it.

---

Then you download / clone this repository, and run `./vtuber.py`. By default there should be a white screen. Use the following keybinds to get introduced to the default character Bob:
- **i** (makes Bob walk into the screen)
- **o** (makes Bob walk out of the screen)
- **f** (make Bob formal _(great for school presentations)_)
- **g** (make Bob a gangster _(don't ask me why)_)
- **s** (make Bob a sheriff _(again, don't ask me why)_)
- **d** (make Bob dance)

When you've made Bob walk into the screen and you start talking, it probably won't match your volume very well. For this you have to load up `vtuber.py` in a text editor, and then uncomment `#print(volume)` on line 142. Try running it again, and pay attention to the default noise level and your normal talking level. Edit the if-statements right above line 142 to match your volumes. My default talking volume is around 26, and the general noise level (noise, keyboard/mouse, breathing, etc...) is around 4-5.

So this is what my volume settings look like on line 131:
```py
if (volume > 25): # Normal talking volume
    step = 4
elif (volume > 19):
    step = 3
elif (volume > 12):
    step = 2
elif (volume > 6):
    step = 1
elif (volume <= 6): # General noise level
    step = 0
```
Customize this and test it a few times. Try talking in different volumes to see if it changes frames correctly.
