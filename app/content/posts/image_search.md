title: Deploying a Convolutional Neural Net for Image Similarity Search
date: 2018-09-23
link: image_search

I've been working with different machine learning models such as neural networks, and decision trees on various research projects throughout the past year, but I haven't deployed these models in any type of production environment where efficiency is key. 

For this project I built an efficient system that takes an image uploaded by a user and searches a small collection of images (~10,000) for the 10 most similar images in the collection. There are a few components that we need to make this system work.

1) We need some way to compare how similar images are.
2) We need to be able to quickly search a database for similar images.
3) We need to be able to handle uploads from multiple users concurrently. 

Let's start with the first one. How do we compare how similar two images are? I chose a common way to calculate similarity between two images using embeddings. An embedding in this case refers to a fixed length vector that in some way encodes a representation of an image. We can use cosine similarity to calculate the how "close" two embeddings are in n-dimensional space, in order to return similar images to some query image.

So how do we generate embeddings for images? I used a convolutional neural network pre-trained on the ImageNet dataset to produce embeddings for all of the images in my database. We can think of a convolutional neural network as a feature extractor for images. When an image is fed into a network it undergoes successive mathematical operations, until we are left with a fixed length vector at the start of the fully connected layers that sit on top of the convolutional layers. This fixed length vector will serve as the representation of an image, the embedding that was mentioned earlier. 

In order to quickly search for similar images we can pre-generate embeddings for all of the images in the database. The problem of searching for similar vectors has been extensively studied, and there are some easy to use existing libraries to create fast indexing structures out of vectors. This approach is quick, and scale to a large number of images. For this application I'm using the library Annoy, which maps indexes into static files that take up only a small amount of memory. At the most basic level Annoy divides up the hyperspace that the embeddings occupy into a number of different trees, so that the whole dataset does not need to be searched to find some number of approximate nearest neighbors. 