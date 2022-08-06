from flask import render_template
from app.image_search import bp
from flask import current_app

from threading import Thread
from PIL import Image
import numpy as np
import flask
import redis
import uuid
import time
import json
import io

from torchvision import transforms

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


@bp.route('/predict', methods=["GET", "POST"])
def predict():
 # initialize the data dictionary that will be returned from the view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        print("at try", flush=True)
        try:
            print("file posted")
            if "image" in flask.request.files:
            #if flask.request.files.get("file"):
                print("image detected", flush=True)
                # read the image in PIL format and prepare it for classification
                image = flask.request.files["image"].read()
                image = Image.open(io.BytesIO(image))
                image = prepare_image(image)

                # check that image shape is correct 
                print("image shape: {}".format(image.shape), flush=True)
                assert image.shape == (3, 224, 224)

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
            if data["success"] == True:
                # rework paths
                paths = []
                for path in data["paths"]:
                    p = path.split("/")
                    s = p[-3] + "/" + p[-2] + "/" + p[-1]
                    paths.append(s)
                print(paths, flush=True)
                return render_template("predict.html", files=paths, message="Here are the most similar images found!")
            else:
                return render_template("predict.html", files="", message="There was an error!")
        except:
            redis_db.flushall()
            return render_template("predict.html", files="", message="There was an error! RGB images should be uploaded. Anything else (svg, grayscale) will result in an error.")

    elif flask.request.method == "GET":
        return render_template("predict.html", files="")

    

