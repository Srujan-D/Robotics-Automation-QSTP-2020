Before reading this, it is advised to read the questoion given in the assignment. (The assignment is available in the 'WEEK 2' directory.)
The launch directory (in 'src' directory) contains two launch files.
Launching the file 'turtle_circle.launch' moves the turtlebot in a circle of radius given by user. 
Launching the file 'turtle_infinity.launch' moves the turtlebot in an 'eight/infinity' path consisting of two circles. The radius of the circle is to be given by the user.
The turtlebot will move only after a non-zero radius value is entered, otherwise the code will give an error.

NOTE:
The angular velocity will be computed by the program using the formula (linear velocity/radius).
The linear velocity is given in x direction only. Also, its value is taken as 0.5. 
It is advised to give a radius value around 0.5, by which the angular velocity will have a value around 1.0 .
This is particularly suggested as this ROS code will be simulated in gazebo, which is a perfect physics engine.
If a value of radius is taken such that we get angular velocity more than 1.0 (approximately), this large angular velocity will make the turtlebot go haywire.
We have to keep in mind the dynamics of the turtlebot.
Also, taking the value of linear velocity greater than 0.5 (approximately) will gives us the same undesirable result. The turtlebot will go haywire.
Thus, to obtain the desired simulation, radius value of 0.5 is suggested. This will give angular velocity value as 1.0 .
