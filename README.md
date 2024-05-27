## Machine-Vision-Collision-Avoidance-Control-Demonstrator

The Machine-Vision-Collision-Avoidance-Control-Demonstrator (MVCACD) shows the benefits of electromechanical control and automation for repetitive and time critical tasks, through a collision avoidance-based arcade machine. The device is aimed at inspiring 11–14 year-olds to consider a career in Engineering. 

<img src="https://github.com/MattJmt/Machine-Vision-Collision-Avoidance-Control-Demonstrator/blob/main/figures/Device_Labeled.png" width="500"/> <img src="https://github.com/MattJmt/Machine-Vision-Collision-Avoidance-Control-Demonstrator/blob/main/gifs/exhibition.gif" width="280"/>


We used the `OpenCV` library to detect the different obstacles in real time, and avoid them with a stepper motor controlled via a Raspberry Pi. 

<img src="https://github.com/MattJmt/Machine-Vision-Collision-Avoidance-Control-Demonstrator/blob/main/gifs/ObstacleDetection.gif" width="200"/>


| Function | Purpose |
|---------|---------|
|drivetest()| Controls the motor direction and steps based on parameters.|
|drive()| Adjusts the motor's position.|
|colourid()| Processes video input to identify specific colors within the captured frame, using HSV color space and predefined color boundaries.|
|whichtrack()| Determines track positions based on coordinates.|
|channels()| Determines the target position based on identified tracks.|


# Modes of Operation

The MVCACD has three different modes of operation which are increasingly automated to exemplify the notion of control systems.

| Mode | Instruction |
|---------|---------|
|1) Fully Manual | Manipulating the joystick moves the pin left or right continuously without computer assistance|
|2) Computer Assistance | Manipulating the joystick moves the pin to one of three discrete tracks.|
|3) Computer Controlled | Fully automated machine-vision control, using the camera as input.|


<img src="https://github.com/MattJmt/Machine-Vision-Collision-Avoidance-Control-Demonstrator/blob/main/gifs/Joystick_Mode1.gif" width="200"/>
The device was succesfully presented at the Great Exhibition Road Festival, and was awarded the highest grade of the cohort.
