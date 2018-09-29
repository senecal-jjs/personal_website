title: Deploying a Convolutional Neural Net for Image Similarity Search
date: 2018-09-23
link: image_search

## Part 1: Description of the application

### If you want to try out the app immediately, click <a href="{{ url_for('image_search.predict') }}">here.</a> 

I've been working with different machine learning models such as neural networks,and decision trees on various research projects throughout the past year, but I haven't deployed these models in any type of production environment where efficiency is key. 

For this project I built an efficient system that takes an image uploaded by a user and searches a small collection of images (~10,000) for the 10 most similar images in the collection. There are a few components that we need to make this system work.

1. We need some way to compare how similar images are.
2. We need to be able to quickly search a database for similar images.
3. We need to be able to handle uploads from multiple users concurrently. 

Let's start with the first one. How do we compare how similar two images are? I chose a common way to calculate similarity between two images using embeddings. An embedding in this case refers to a fixed length vector that in some way encodes a representation of an image. We can use cosine similarity to calculate how "close" two embeddings are in n-dimensional space, in order to return similar images to some query image.

So how do we generate embeddings for images? I used a convolutional neural network pre-trained on the ImageNet dataset to produce embeddings for all of the images in my database. We can think of a convolutional neural network as a feature extractor for images. When an image is fed into a network it undergoes successive mathematical operations, until we are left with a fixed length vector at the start of the fully connected layers that sit on top of the convolutional layers. This fixed length vector will serve as the representation of an image, the embedding that was mentioned earlier. 

<div class="img_row">
    <img class="col-9" src="{{ url_for('static', filename="img/vgg16.png") }}">
</div>

<div class="col-12 caption">
    The neural network architecture I'm using. The vector of length 4096 in the penultimate layer of the network is used as the image embedding. 
</div>

In order to quickly search for similar images we can pre-generate embeddings for all of the images in the database, by running the images through the pre-trained convolutional neural network. The problem of searching for similar vectors has been extensively studied, and there are some easy to use existing libraries to create fast indexing structures out of vectors. This approach is quick, and can scale to a large number of images. For this application I'm using the library Annoy, which maps indexes into static files that take up only a small amount of memory. At the most basic level Annoy divides up the hyperspace that the embeddings occupy into a number of different trees, so that the whole dataset does not need to be searched to find some number of approximate nearest neighbors. 

Ok, so now we have a way to generate embeddings for images, and a way to structure these embeddings so that they are quickly and easily searchable. The final part of the system we need is a way to handle concurrent image uploads from users. For this part of the application I chose to use Redis, which allows us to store data structures in memory. As users submit images, these images are placed in a queue, stored using Redis. We also have a separate process running our convolutional neural network, that continually polls the Redis queue for images. When images are in the queue, they get pulled out put into a batch, and fed through the neural network simultaneously to produce embeddings for the images. These embeddings are then stored back in Redis. Backing up a bit, when the image was originally submitted by a user, a loop was entered that continually polls Redis for a result from the thread generating the embeddings. Once a result is returned (a result consists of a list of file paths to similar images stored on my server) the similar images can be displayed to the user. 

<div class="img_row">
    <img class="col-9" src="{{ url_for('static', filename="img/image_search_structure.jpg") }}">
</div>

<div class="col-12 caption">
    The structure of the application.
</div>

## Part 2: Actually running this stuff
For this application to run smoothly we need a few components to work together. When an image is submitted by a user, the web server Nginx handles the upload, the serialized image then gets forwarded to Gunicorn which is a python web server running my Flask app (Flask is a web framework for python). The Flask endpoint then submits the image to Redis. In the background I am using Supervisor, which is a system to monitor and control processes on UNIX systems. I use Supervisor to manage Redis, and my neural network process in the background. Getting all of this configured correctly can be tricky, I'll try to add more detail in the future. 

## Part 3: Test run
Here's an example of the application in action. I uploaded an image of an airplane and my app returned 10 similar images. One caveat, my image database consists of about 20 different classes of images (airplane, bicycle, bird, car, etc.) so if you upload an unusual image, I'm not sure what you'll get back. 

<div class="img_row">
    <img class="col-9" src="{{ url_for('static', filename="img/image_search_result.png") }}">
</div>

To try out the application yourself, click <a href="{{ url_for('image_search.predict') }}">here.</a> 


