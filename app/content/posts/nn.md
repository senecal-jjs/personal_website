title: Neural Network from Scratch
date: 2018-07-13

Link to code: <a target="_blank" href="https://bitbucket.org/jsene/ga_evolve_mlp/src/master/">Click here</a>

Link to paper: <a target="_blank" href="{{ url_for('static', filename="pdf/ml-project3-final.pdf") }}">Click here</a>

Several variations of neural networks exist, including Multi-layer perceptron (MLP) networks, 
recurrent networks, and convolutional networks. I implemented a MLP network capable of performing 
regression tasks, and with a later update, classification tasks. Code for the networks can be found 
<a style="color:Blue;" target="_blank" href="https://bitbucket.org/jsene/neural-network">here</a> and
<a style="color:Blue;" target="_blank" href="https://bitbucket.org/jsene/ga_evolve_mlp">here</a>.
A neural network consists of an input layer, hidden layers, and an output layer. In a feed forward network nodes in adjacent layers are connected to one another. Each connection in the network is assigned a weight value, which is updated during network training. 

<div class="img_row">
    <img class="col-7" src="{{ url_for('static', filename="img/NeuralNetwork.png") }}">
</div>

<div class="col-12 caption">
    Example of a feed-forward neural network with one hidden layer. 
</div>

For this project myself and two of my classmates programmed all of the components required for a neural network from scratch in Python, including functionality to create networks with arbitrary numbers of layers and neurons, with the option of a hyperbolic tangent or sigmoid activation function. The network could be trained for either regression or classification. 

In addition to implementing backpropagation to train networks, we also implemented several variants of evolutionary algorithms to train networks, including genetic algorithms and differential evolution. 

My classmates and I expected backpropagation with stochastic gradient descent to be the faster training method (in terms of iterations to convergence) as it is a much more direct method for updating network parameters compared to evolutionary approaches. However, in most cases the evolutionary training algorithms performed comparably to backpropagation. 

<div class="img_row">
    <img class="col-7" src="{{ url_for('static', filename="img/concrete.jpg") }}">
</div>

<div class="col-12 caption">
    In terms of regression error the evolutionary algorithms performed similarly to backpropagation. However, in terms of wall clock runtime training with an evolutionary approach was significantly slower. A distributed version of the evolutionary approach may be able to eliminate the runtime disadvantage. 
</div>

While I wouldn't use this network and code for any serious research, tensorflow and pytorch are much more capable in this regard, this project was an excellent way to dive into the basic mechanics of neural networks, and I gained a deeper and more intuitive sense of some of their strengths and weaknesses. 