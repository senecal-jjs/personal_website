title: Autonomous Submarine
date: 2018-07-13
link: sub

For this post I wanted to give a brief overview of my senior capstone project, the "Robosub", and 
demonstrate some of its capabilities. The robosub is an autonomous submarine that can complete a variety of different tasks. The sub is capable of locating targets and firing its pneumatically powered torpedoes, and it can also use its robotic arm to open doors and pickup objects! I worked with a team 
of 7 other students on the robosub as part of our senior capstone project. The project was 
sponsored by the Naval Undersea Warfare Center in Keyport, Washington. 

There is a large number of systems and sub-systems that make up an autonomous submarine. There's the 
mechanical system, consisting of the main waterproof capsule that houses the sub's electronics, the frame on which the capsule and thrusters are mounted, and the robotic arm that is used to open doors that 
are present in the obstacle course built by AUVSI, the organization that sponsors the Robosub competition. The electrical system must power all of the sub's components for up to 20 minutes at a time during competition runs. The final main systems is the "brain" of the the sub, and it consists of an Intel NUC compact computer, and a Nvidia Jetson TX2 GPU. 

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/scheme.png") }}">
</div>

<span class="col-12 caption">
    Schematic of the Robosub systems.
</span>

Autonomous navigation is a complex topic. A vehicle often has to fuse data from multiple
sources to inform the vehicle's belief of where it is located. This problem is often referred to as SLAM,
which stands for simulataneous localization and mapping, and it's still an open area of research. In the
case of the Robosub, navigation sensors consist of an inertial measurement unit with a 3-axis gyroscope, 
a 3-axis accelerometer, a front facing camera, and a downward facing camera. The information from these
sensors is fused together using an extended Kalman filter, which is essentially a way to update a system's
model about it's current state using various sensor data when it's available. Kalman filters are also
a rather extensive topic and there's a lot of research literature available if you're interested in 
learning more. 

The video below shows the Robosub completing a navigation task that involved tracking buoys. The goal was to have the Robosub identify different colored buoys, and then approach and tap each buoy. The computer vision system on board the sub identifies objects using a convolutional neural network. Once an object has been detected, that information is converted to commands to fire the thrusters to move the sub to the desired destination. 

<div class="img_row">
    <iframe width="440" height="335"
        src="https://www.youtube.com/embed/rltVbQ8TxQI?controls=1">
    </iframe>
</div>

One of the main Robosub systems I worked on was the design and construction of a prototype robotic arm.
There were two main considerations I had to keep in mind when designing the robotic arm. Since it was a 
prototype it had to be easy to test different components and swap in new ones. We were also doing all of the manufacturing for the grip portion of the robotic arm in house, so when designing the parts for the grip I wanted them to be easy to build since we only had access to a basic mill and lathe. The final 
design featured a rotary pneumatic actuator and a linear pneumatic actuator that can move the robotic arm into a position where it can grab objects below or in front of the sub. The grip consisted of four simple pieces. Two "fingers" that actually grab the objects, a baseplate that the fingers slide and rotate about,
and an adapter piece that connects the linear actuator that moves the grip. The entire grip is mounted on 
a piece of t-frame aluminum that allowed easy swaps of different grip components during testing. The sub's robotic arm can be used to open doors and lids, and grab objects. The arm is pneumatically 
powered with a maximum grip force of approximately 25 lbs. 

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/grip.png") }}">
</div>

<div class="col-12 caption">
    Schematic of the sub's robotic arm.
</div>

A new version of the robosub is currently being produced with improved thusters, and electronics management. The updated design will also allow for easier upgrades in the future.

<div class="img_row">
    <img class="col-6" src="{{ url_for('static', filename="img/new_sub_frame.jpg") }}">
    <img class="col-6" src="{{ url_for('static', filename="img/new_sub_electric.jpg") }}">
</div>

<div class="col-12 caption">
    The new version of the Robosub currently in production.
</div>


