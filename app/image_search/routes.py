from flask import render_template
from app import db
from app.image_search import bp
from flask import current_app

from threading import Thread
from PIL import Image
import numpy as np
import base64
import flask
import redis
import uuid
import time
import json
import sys
import io

from torchvision import datasets, transforms

from app.image_search import settings
from app.image_search import helpers 
#from app.image_search import run_pytorch_server


redis_db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# Create preporcessing transform 
data_transform = transforms.Compose([transforms.Resize((224,224)),
                                     transforms.ToTensor(),
                                     transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                          std=[0.229, 0.224, 0.225])
                                    ])

def prepare_image(image):
    image = data_transform(image)
    # keep image as numpy array so it can be serialized in Redis
    # change to torch tensor before feeding into network 
    return image.numpy()


# @bp.before_app_first_request
# def activate_pytorch_server():
#     t = Thread(target=run_pytorch_server.classify_process(redis_db), args=())
#     t.daemon = True
#     t.start()


@bp.route('/predict', methods=["POST"])
def predict():
 # initialize the data dictionary that will be returned from the view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format and prepare it for classification
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image)

            # ensure our NumPy array is C-contiguous as well,
            # otherwise we won't be able to serialize it
            image = image.copy(order="C")

            # generate an ID for the classification then add the
            # classification ID + image to the queue
            k = str(uuid.uuid4())
            d = {"id": k, "image": helpers.base64_encode_image(image)}
            redis_db.rpush(settings.IMAGE_QUEUE, json.dumps(d))

            # keep looping until our model server returns the output
            # predictions
            while True:
                # attempt to grab the output predictions (similar image paths)
                output = redis_db.get(k)

                # check to see if our model has classified the input image
                if output is not None:
                     # add the output predictions to our data
                     # dictionary so we can return it to the client
                    output = output.decode("utf-8")
                    data["paths"] = json.loads(output)

                    # delete the result from the database and break from the polling loop
                    redis_db.delete(k)
                    break

                # sleep for a small amount to give the model a chance
                # to classify the input image
                time.sleep(settings.CLIENT_SLEEP)

            # indicate that the request was a success
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)