title: Monitoring Produce with Machine Learning and Hyperspectral Imagery
date: 2018-09-07
link: hyp

For the past few months I've been working on an Intel sponsored research project to assess what kinds of information can be gleaned from using machine learning techniques to analyze hyperspectral images of produce 
inside of a grocery store (fruits, vegetables, etc). 

Most standard images, like jpeg files, are made of of 3 visible wavelengths; red (~750 nm), blue (~450 nm), and green (~500 nm). A hyperspectral image consists of many more wavelengths, typically spaced a few nanometers apart (but it varies for every imager). The particular camera used for this project is capable of capturing wavelengths every 2 nm ranging from ~400 nm to ~1000 nm, which is approaching the near infrared range.  

When we take pictures of produce with the hyperspectral camera, we hope to see signatures in some of the spectral bands that are not in the visible spectrum, and so cannot be seen by the human eye. Ideally these signatures would give us additional information about the aging process or quality of the produce we are examining before such information would ever be apparent to a human visually examining the produce. 

Capturing hyperspectral images in a grocery store provides some challenges that aren't encountered as often when imaging outdoors. In order to get information from a large range of the spectrum we need to have a light source that is emitting a broadband spectrum which reflects off the produce we are imaging and into our optics for processing. Outdoors we have an excellent broadband light source in the Sun. When we initially started taking measurements in our lab we used halogen lights as our source.

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/imaging_setup.png") }}">
</div>

In grocery stores there is generally a mix of fluorescent and LED light sources, and while not as good as the Sun, the LED lights in the several grocery stores we've taken measurements at, have provided enough energy across the spectrum to capture the information we need to try and predict the age and quality of produce. 

However, capturing the images is only half the battle. While hyperspectral images contain a wealth of information, they can be difficult to interpret. A single 200 x 300 pixel hyperspectral image that we acquire is about 1 Gb in size. It can be difficult for a human to look at all of these spectral bands and pixels and accurately process how things are changing over time in the image. One way to make the images easier to interpret is to create an average reflectance spectra for a large portion of an image that corresponds to a single piece of produce. A reflectance spectra shows the percentage of light reflected by a piece produce at each wavelength along the spectrum.

The figure on the left below shows how the reflectance spectra changes for a banana as it ages, while the figure on the right shows how the reflectance spectra differs for different types of bell peppers. 

<div class="img_row">
    <img class="col-6" src="{{ url_for('static', filename="img/banana_spectra.png") }}">
    <img class="col-6" src="{{ url_for('static', filename="img/bell_pepper_spectra.png") }}">
</div>

<span class="col-12 caption">
    Reflectance spectra for a banana, and different types of peppers. 
</span>

The images below show a fresh banana, and an old banana. Notice how different the reflectance spectra are!

<div class="img_row">
    <img class="col-11" src="{{ url_for('static', filename="img/early_fruit_spectra.png") }}">
</div>

<div class="img_row">
    <img class="col-11" src="{{ url_for('static', filename="img/late_fruit_spectra.png") }}">
</div>

Reflectance spectra change as the produce ages because things like water content and chlorophyll levels change. While the changes in the banana spectra above are clearly visible to the human eye, ideally we would be able to detect changes automatically, and detect changes that are more subtle, before we can visibly see any of these changes in the banana. Using machine learning we can automatically detect changes in reflectance spectra as produce ages. 

To estimate the age of produce requires a few steps. We first need to capture an image, then calibrate the image to produce accurate reflectance values. We then have to classify what produce is in the image since each type of produce requires its own specific age model. Classification is performed by dividing the image into a grid of cells where each cell consists of a set of 5x5 pixels. The spectra in each cell is averaged then classified using a simple two layer, fully connected neural network. After classification the age of the produce in each grid cell can be predicted using the average spectra in the cell, and a produce type specific fully connected neural network. The figure below summarizes the process.

<div class="img_row">
    <img class="col-10" src="{{ url_for('static', filename="img/Data Pipeline.png") }}">
</div>

An example of produce classification and age prediction is shown in the example below. For future work we would like to try and develop a low cost imager that images in less wavelengths but can still provide the same amount of "relevant" information. 

<div class="img_row">
    <img class="col-12" src="{{ url_for('static', filename="img/prediction.png") }}">
</div>

