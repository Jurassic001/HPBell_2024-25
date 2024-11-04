# HPBell_2024-25/AVR/Test code
This year's AVR test code. A lot of this stuff is pretty *special* so unless you wrote something or at least understand it don't mess with it.
## Navigation
### `AT Video Feed Files`
A set of files intended to bring the colored video that the apriltag camera captures to the user's GUI. The code in this directory is an **early, untested prototype**. This code is just a proof-of-concept. Don't just merge it with your AVR code without knowing what you're doing first. Note that you'll need to build the apriltag module locally in order for this code to work. If you do implement this code it *shouldn't* put much more strain on the Jetson, but I'm not promising anything. **IMPORTANT:** in order to implement this you'll need to import the `base64.h` C++ library in order to encode the camera data.
***
### `objscanner`
A custom software module designed to use the CSI camera to scan for field elements matching certain images, and both report the data and automatically align itself with the field element. It comes with a dockerfile, a readme, a requirements.txt file, and MQTT topics for control. Unfortunately, it doesn't work on the Jetson, likely because of the insane amount of proprietary software and custom hardware that you have to use to analyze camera data on the poor Jetson Nano. For this to work, it'll likely have to be coded in C++ and use some of Nvidia's proprietary stuff (at least for the Jetson). That isn't a rabbit hole I'm planning to go down, but if someone else is interested, by all means, go ahead.
***
