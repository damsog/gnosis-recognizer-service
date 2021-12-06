import json
import os
import time
import insightface
from videoAnalytics.encoder import encoderExtractor
from flask import Flask, Request, Response
from uuid import uuid4
from flask.globals import request
from dotenv import load_dotenv, find_dotenv


def main():
    #initializations
    load_dotenv(find_dotenv())

    # Some definitions
    NET = None
    METADATA = None
    MAX_SIMULTANEOUS_PROCESSES = 1
    NUM_SESSIONS = 0
    HOST = os.environ.get("SERVER_IP")
    PORT = os.environ.get("SERVER_PORT")


    # Creating our server
    app = Flask(__name__)

    #loading the face detection model. 0 means to work with GPU. -1 is for CPU.
    detector = insightface.model_zoo.get_model('retinaface_r50_v1')
    detector.prepare(ctx_id = 0, nms=0.4)

    #loading the face recognition model. 0 means to work with GPU. -1 is for CPU.
    recognizer = insightface.model_zoo.get_model('arcface_r100_v1')
    recognizer.prepare(ctx_id = 0)

    # Creating our face detection and recognition sistem.
    encoder = encoderExtractor(None, detector, recognizer)

    #======================================================Requests============================================================
    @app.route('/load_models', methods=['GET'])
    def load_models():
        result = "0"
        print("load_models")
        return result

    @app.route('/unload_models', methods=['GET'])
    def unload_models():
        result = "0"
        print("unload_models")
        return result

    @app.route('/encode_images', methods=['POST'])
    def encode_images():
        result = "0"
        print("encode_images")
        encoder.set_input_data( str(request.get_json("imgs")).replace("'",'"') )
        result = encoder.process_data()
        
        return str(result).replace("'",'"')

    @app.route('/compare_to_dataset', methods=['POST'])
    def compare_to_dataset():
        result = "0"
        print("compare_to_dataset")
        return result

    @app.route('/start_live_analytics', methods=['GET'])
    def start_live_analytics():
        result = "0"
        print("start_live_analytics")
        return result

    @app.route('/stop_live_analytics', methods=['GET'])
    def stop_live_analytics():
        result = 0
        print("stop_live_analytics")
        return result

    #======================================================Start the Server====================================================
    app.run(host=HOST, port=PORT)

if __name__=="__main__":
    main()