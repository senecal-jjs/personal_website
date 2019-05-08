[![CircleCI](https://circleci.com/bb/jsene/website_v3/tree/master.svg?style=svg)](https://circleci.com/bb/jsene/website_v3/tree/master)

## Personal Website

This website is primarily built using Flask. The application is organized into four different microservices each of which run inside a docker container. The flask application itself is run in the "web" microservice. A Redis database is run in the "redisdb" microservice. A machine learning model built using PyTorch is run in the "pytorch_server" microservice, and the Nginx web server is used as a reverse proxy in the "nginx" microservice. 

The containers are connected together and provisioned using docker-compose. "web" provides the application endpoints. "redisdb" is used to store uploaded user images that are then processed by the "pytorch_server" machine learning model, and "nginx" forwards incoming requests to a gunicorn web server that is serving the flask application. "certs.sh" is a bash script that automates the acquisition of SSL certificates from Let's Encrypt. 

Continuous integration / continuous deployment is accomplished using Circle CI. 