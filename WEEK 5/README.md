Before reading this, it is important to know what the final project is. So, it is suggested to read the QSTP Final Project file in the same directory.

For running the codes, you have to first clone the "https://github.com/ERC-BPGC/omnibase" repo. 
There are three nodes - pub_obs.py, path_planner.py and pid_controller.py
pub_obs.py publishes the centres of the desired cylindrical obstacles of radius 0.25 units and height 10 units.
path_planner.py node subscribes to the above list of obstacles and plans & publishes a path for the Trotbot to move from the start point to goal location using the RRT algorithm.
pid_controller.py node subscribes to the published path and thus publishes the required rotational and translational velocities of the Trotbot on /cmd_vel topic, by which the Trotbot moves.

Move the the pid_controller.py node from /scripts to /omnibase_controller node from the above downloaded repo.

There are some important comments on line 30 onwards in the pub_obs.py node, and it is advised to go through it before running it.
Two self-defined messeges are used - points.msg, and mylist.msg . Both are available in the /msg directory.
Other important instructions to run the nodes are given in the QSTP Final Project file.

There are some bugs in the codes, but they are not enough to stop the nodes from running. They will be updated soon.
