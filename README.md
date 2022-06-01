#### computational photography from video

The purpose of this project is to create a computational image from videos shot from devices that are not capable of shooting photograph with full shutter/aperture controls (phones, webcams). 

In principle, camera exposure is an accumulation of photons on sensors (in quantize perspective) over a given period of time. Theoretically speaking if the frame rate of the video is high enough, a video shot from a given device can cover all the information needed, to reconstuct a photo shot during that period (with arbitrary aperture and shutter speed). 

Based on this idea, cameras that are not typically "high-end" enough are probably capable of producing effects as [long exposures](https://en.wikipedia.org/wiki/Long-exposure_photography), or [multiple exposures](https://en.wikipedia.org/wiki/Multiple_exposure) by computational methods over the video.

#### virtual shutter

[Work by Bennett and McMillan](http://www.csbio.unc.edu/mcmillan/pubs/sig07_Bennett.pdf) introduces the concept of "virtual shutter": to emulate a shutter exposure from a series of video frames.

Here is an implementation of maximum virtual shutter, which I feel from my personal experience emulates the multiple exposure, mostly achived by film cameras. The video I used is from [Alex Lorenz, Winsordawson](https://youtu.be/oem5-_YaY1E), from 8:56 to 9:37. The sampler samples every 29 frames, and illuminance is computed according to [ITU-R Recommendation BT.709](http://www.itu.int/rec/R-REC-BT.709).

![uniform_result](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/unstabilized_manhattan_maximum_shutter.png)

#### stablization

A big problem with phone videos is camera stablization. While the industry comes up with better stablization solutions every year, for most devices, shaking is common in videos. However stablization is crucial for effects like long exposures, and professionals use tripods to hold their cameras in the same place throughout the exposure period. 

To achieve similar effects, we will need to first stablize the video at hand. Intuitively, I chose the SIFT feature extraction for this purpose. The steps are:
* extract SIFT features from all of the frames (depending on sampling method, that can be all frames in video or a subset of them)
* matching the keypoints by SIFT between current and next frame
* compute perspective transformation from the next frame to current frame
* warp the next frame by the transformation

Another nice data I found online is by [Sven Pertermann](https://youtu.be/CF_C13iPvOg). Here I used the 23:16 and 23:21 segment of the video. Apperantly the video has some shaking, and if we directly apply the maximum virtual shutter (samples every 14 frames), the result will be very blurry.

![unstabilized_result](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/unstabilized_tokyo_maximum_shutter.png)

Compare to the result from SIFT stablization (same maximum virtual shutter applied).

![stabilized_result](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/stabilized_tokyo_maximum_shutter.png)

A nice looking multiple exposure image that takes me back to the lo-fi days of shooting with Diana F+. 

It also reminds me that it might be possible to create a "long exposure" effect from the same data. Long exposures are produced by setting the shutter to extremely low speed, and is quite popular in night time city photography. In ideal case, if the video has the same update rate as the sensor update rate of the hardware, we may reconstruct images with arbitrary shutter speed from the video alone. However with typical framerate (30fps/60fps/120fps) we may only give an approximation. 

Since we are trying to sample as much frames as possible, I used all of the frames in the 6-second segment, stablized them, and put them through an average virtual shutter. 

![average_tokyo](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/average_tokyo.jpg)

The "extended exposure virtual shutter" by Bennett and McMillan proposed an averaging with a weighting function, which gives more weight to more recent frames. It sounds rather counter-intuitive at the beginning, but since with a sampler we are
taking less frames into consideration, the blurring inroduced by minor errors in stablization is greatly reduced in result.

![extended_exposure_tokyo-1](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/extended_exposure_tokyo.png)

#### more data
I have shot a few videos with my old iphone 5 to test this method further. It seems the extended exposure virtual shutter works really well with SIFT stabilization. And the result also proves that simply averaging out the frame by frame calibration is not going to work if there are large portions of the scene moving (the accumulated error gets big eventually)!

![tube](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/average_tube.jpg)

Compares to the sampled (every 14 frames) extended exposure virtual shutter result.

![extended_exposure_tube-2](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/extended_exposure_tube.png)

A few more results using the extended exposure virtual shutter.

![extended_exposure_road-1](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/extended_exposure_road.png)

![extended_exposure_stairs-1](https://raw.githubusercontent.com/Alprazolam/virtual_shutter/master/extended_exposure_stairs.png)


#### summary
This method provides a way to be creative about shutter speed when you have neither a tripod nor a pro camera. Essentially it allows people to play with exposure with just smart phones ([well... playing with exposures is not a thing to do with high-end cameras to begin with](http://www.bbc.com/future/story/20171113-the-toy-camera-that-inspired-instagram)).

I can imagine the method also works when you would like to capture something (or some motion) when you do not have good enough shutter synchronization, or simply lacks the reaction time to get a perfect snap. Instead it is possible to video the whole process in a relatively stable stance and do computational tricks to restore the supposed image.

#### possible improvements?
The method works when features can be tracked in background (static reference for camera stablization) and is not real time. SIFT is not a fast method in feature extraction but I used it for its accuracy; therefore it is possible to speed the process using other keypoint matching methods as SURF or sparse optical flow.

I also suppose there are way more effects one can achieve by playing with the virtual shutter part: Bennett and McMillan paper suggests effects that are not possible with physical cameras as well. This part is where people can get really creative in term of art.

#### additional info
To run the code you need the OpenCV 3 library with Python 3 (I think minor version does not matter too much).
The SIFT feature for OpenCV3 is moved to a seperate package so please make sure you have that installed as well.
