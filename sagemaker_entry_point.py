print("print test 000")
import argparse
import json

import torch
from modules.train import train
from modules.MLparamaters import getMLParamaters
from modules.infer import getProcessedImage


import os
import sys
import cv2
import numpy as np

import logging


print("print test 000")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

paramaters = getMLParamaters()
IMAGE_CONTENT_TYPE = 'application/x-image'


def input_fn(request_body, content_type=IMAGE_CONTENT_TYPE):
    try:
        """入力データの形式変換."""
        print("print test 1")
        logger.info('START input_fn')
        logger.info(f'content_type: {content_type}')
        logger.info(f'type: {type(request_body)}')

        logger.info('Deserializing the input data.')
        
        # process an image uploaded to the endpoint
        if content_type == IMAGE_CONTENT_TYPE: 
            input_data = cv2.imdecode(np.frombuffer(request_body, dtype='uint8'), cv2.IMREAD_UNCHANGED)
            logger.info(f'type: {type(input_data)}')
        else:
            logger.info("CONTENT ELSE")
            # TODO: content_typeに応じてデータ型変換
            logger.error(f"content_type invalid: {content_type}")
            input_data = {"errors": [f"content_type invalid: {content_type}"]}
        logger.info('END   input_fn')
        return input_data
    except Exception as e:
        print(e)
        return json.dumps(str(e)), request_body, content_type

def predict_fn(input_data, model):
    try:
        """推論."""
        print("print test 2")
        logger.info('START predict_fn')
        logger.info(f'type: {type(input_data)}')
        return getProcessedImage(input_data,model)
    except Exception as e:
        print(e)
        return json.dumps(str(e)), input_data, model

JSON_CONTENT_TYPE = 'application/json'

def output_fn(prediction, accept=JSON_CONTENT_TYPE):
    try:
        """出力データの形式変換."""
        print("print test 3")
        logger.info('START output_fn')
        logger.info(f"accept: {accept}")
        
        content_type = JSON_CONTENT_TYPE
        
        return prediction, content_type
    except Exception as e:
        print(e)
        return json.dumps(str(e)), prediction,accept

def _train(args):
    print("args is",args)
    # train()

def model_fn(model_path):
    print("model_path is",model_path)
    try:
        print("print test 4")
        device = paramaters.device
        use_model=torch.load(model_path)
        return use_model.to(device)
    except Exception as e:
        print(e)
        return json.dumps(str(e)), model_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Data and model checkpoints directories
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                        help='SGD momentum (default: 0.5)')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=100, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--backend', type=str, default=None,
                        help='backend for distributed training (tcp, gloo on cpu and gloo, nccl on gpu)')

    # Container environment
    parser.add_argument('--hosts', type=list,
                        default=json.loads(os.environ['SM_HOSTS']))
    parser.add_argument('--current-host', type=str,
                        default=os.environ['SM_CURRENT_HOST'])
    parser.add_argument('--model-dir', type=str,
                        default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str,
                        default=os.environ['SM_CHANNEL_TRAINING'])
    parser.add_argument('--num-gpus', type=int,
                        default=os.environ['SM_NUM_GPUS'])

    _train(parser.parse_args())