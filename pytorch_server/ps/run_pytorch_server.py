# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@jemma.png 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py 

# import the necessary packages
from PIL import Image
import numpy as np
import base64
import redis
import uuid
import time
import json
import sys
import io
import os 

import torch 
import torch.nn as nn
import torchvision
import torchvision.models as models
from torchvision import datasets, transforms

# local modules 
import embedding as em 
import helpers
import settings


redis_db = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=0)

def classify_process(redis_db):
    # Load pretrained model 
    print("Loading model...", flush=True)
    net = models.mobilenet_v2(pretrained=True)
    embed_net = nn.Sequential(*list(net.classifier.children())[:-1])
    net.classifier = embed_net
    net.eval() 
    print("Model loaded!", flush=True)
    
    embedding_path = os.path.join(os.getcwd(), "embeddings")
    print("embedding path: {}".format(embedding_path), flush=True)

    # index containing the embeddings of the images in the database 
    image_feature_index = em.load_index(os.path.join(embedding_path, "image_visual_feature_index"), 1280)
    image_embeddings, path_map = em.load_features(os.path.join(embedding_path, "image_visual_features"), os.path.join(embedding_path, "file_map"))
    print("image embedding loaded - length: {} : {}".format(len(image_embeddings), len(path_map)))

    # continually pool for new images to classify
    while True:
        # attempt to grab a batch of images from the database, then
        # initialize the image IDs and batch of images themselves
        queue = redis_db.lrange(settings.IMAGE_QUEUE, 0, settings.BATCH_SIZE - 1)
        imageIDs = []
        batch = None

        # loop over the queue
        for q in queue:
            # deserialize the object and obtain the input image
            q = json.loads(q.decode("utf-8"))
            image = helpers.base64_decode_image(q["image"], settings.IMAGE_DTYPE,(1, settings.IMAGE_CHANS, settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH))

            # convert to torch tensor
            image = torch.FloatTensor(image)

            # check to see if the batch list is None
            if batch is None:
                print("fresh batch", flush=True)
                batch = image

            # otherwise, stack the data
            else:
                batch = torch.stack([batch, image], dim=2)
                print(batch.size())
                batch = batch.view((batch.size(1), 3, 224, 224))
                
            # update the list of image IDs
            imageIDs.append(q["id"])

        # check to see if we need to process the batch
        if len(imageIDs) > 0:
            # classify the batch
            print("* Batch size: {}".format(batch.shape), flush=True)
            embeddings = net(batch)

            results = []
            for vec in embeddings:
                # get similar image embeddings
                similar_images = em.search_index_by_value(vec, image_feature_index, path_map)
                print(similar_images)
                paths = []
                for p in similar_images:
                    paths.append(p[1])
                results.append(paths)
                print(results)

            # loop over the image IDs and their corresponding set of
            # results from our model
            for (imageID, resultSet) in zip(imageIDs, results):
                # initialize the list of output predictions
                output = []

                # loop over the results and add them to the list of
                # output predictions
                for entry in resultSet:
                    #r = {"paths": entry}
                    output.append(entry)

                # store the output predictions in the database, using
                # the image ID as the key so we can fetch the results
                redis_db.set(imageID, json.dumps(output))

            # remove the set of images from our queue
            redis_db.ltrim(settings.IMAGE_QUEUE, len(imageIDs), -1)

        # sleep for a small amount
        time.sleep(settings.SERVER_SLEEP)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    # load the function used to classify input images in a *separate*
    # thread than the one used for main classification
    print("* Starting model service...", flush=True)
    classify_process(redis_db)
    # t = Thread(target=classify_process, args=())
    # t.daemon = True
    # t.start()