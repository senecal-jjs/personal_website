title: Autonomous Submarine
date: 2018-07-13

The robosub is an autonomous submarine that can complete a variety of different tasks. 
The sub is capable of locating targets and firing its pneumatically powered torpedoes, 
and it can also use its robotic arm to open doors and pickup objects! I worked with a team 
of 7 other students on the robosub as part of our senior capstone project. The project was 
sponsored by the Naval Undersea Warfare Center in Keyport, Washington. 

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/scheme.png") }}">
</div>

<span class="col-12 caption">
    Schematic of the Robosub systems.
</span>

The video below shows the Robosub completing a buoy tracking task. The goal was to have the Robosub identify different colored buoys, and then approach and tap each buoy. The computer vision system on board the sub identifies objects using a convolutional neural network. Once an object has been detected, that information is converted to commands to fire the thrusters to move the sub to the desired destination.  

<div class="img_row">
    <iframe width="440" height="335"
        src="https://www.youtube.com/embed/rltVbQ8TxQI?controls=1">
    </iframe>
</div>

The sub's robotic arm can be used to open doors and lids, and grab objects. The arm is pneumatically 
powered with a maximum grip force of approximately 25 lbs. The rotary actuator allows the arm to 
grab objects beneath the sub, while the sliding actuator can extend the arm out in front of the sub.
A new version of the robosub is currently being produced with improved thusters, and electronics management. The updated design will also allow for easier upgrades in the future.

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/grip.png") }}">
</div>

<div class="col-12 caption">
    Schematic of the sub's robotic arm.
</div>




