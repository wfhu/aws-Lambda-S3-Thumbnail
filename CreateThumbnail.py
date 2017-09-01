from __future__ import print_function
import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
     
s3_client = boto3.client('s3')
     
def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)
     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
	print("Log bucket name:", bucket)
        key = record['s3']['object']['key'] 
	print("Log key name:", key)
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
	print("Log download_path name:", download_path)
        upload_path = '/tmp/resized-{}'.format(key)
	print("Log upload_path name:", upload_path)
        
	# create source directory
	directory = os.path.dirname(download_path)
	print("Log directory name :", directory)

	if not os.path.exists(directory):
		os.makedirs(directory)

	#create target directory
	targetdirectory = os.path.dirname(upload_path)
	print("Log targetdirectory name :", targetdirectory)

	if not os.path.exists(targetdirectory):
		os.makedirs(targetdirectory)

	with open(download_path, 'wb') as data:
	        s3_client.download_fileobj(bucket, key, data)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)

