import io
import json
import logging
import os
import json
import random
from enum import Enum
import boto3
from urllib.parse import urlparse
import requests
from flask import Flask, request
from flask_basicauth import BasicAuth
from flask_restx import Api, Resource, reqparse, fields
from werkzeug.datastructures import FileStorage
from pygltflib import GLTF2

from utils1 import configure_usecase, create_folder_if_not_exist, get_file_type
import descriptors


class status(Enum):
    completed = 1
    ongoing = 2
    cancelled = 3

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
api = Api(app, version='1.0', title='3D model descriptor extraction API',
          description='An API for requesting the descriptors of 3D models to be used for 3D object retrieval')
ns = api.namespace('3D model retrieval', description='List of endpoint for requesting the descriptor extraction')

""" Model for inserting a new show into a database """
insert_show_data = ns.model('Data to be processed from min.io',{
    "data" : fields.String(description="The min.io URL of the object to be processed", required=True),
    "start" : fields.Float(description="The start time of the segment to be processed", required=False),
    "end" : fields.Float(description="The end time of the segment to be processed", required=False),
    "last" : fields.Boolean(description="Optional parameter indicating that the segment represents the last frame", required=False),                        
})

id=[]
g_dict = {}
#@ns.route('/extract/<featureName>')
@ns.route('/extract/')
@ns.expect(insert_show_data)
@ns.doc(responses={200: "Successful response", 404: 'Not Found', 500: 'Internal Server Error', 503: 'Service Unavailable'})
class resultsApi(Resource):
    def post(self): #def post(self, featureName: str): 
        global id
        global g_dict
        json_data = request.json
        #featureName = featureName.split('.')[0]
        #args = upload_parser.parse_args()
        file_url = json_data['data']
        filename_with_extension = os.path.basename(file_url)
        featureName = filename_with_extension.split('.')[0]
        new_id = random.sample(range(0, 10000), 1)
        print(file_url)
        print(new_id)
        try:
            response = requests.get(file_url)

            if response.status_code == 200:
                # Function that checks the usecase based on the featureName value
                # Type of dataset related to "News Media" or "Tourism & Automotive"
                category, usecase = configure_usecase(featureName) #'name.gltf'
                print(usecase)
                # Assuming the file is downloaded successfully. Works only for the case of mesh modality and GLTF file
                pth =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DATA')
                create_folder_if_not_exist(pth)
                file_type = get_file_type(filename_with_extension)
                file1 = os.path.join(pth, filename_with_extension)
                with open(file1, 'wb') as file:
                    file.write(response.content) # directory
                    print("File downloaded successfully")
                    # You can further process the downloaded file here
                    # id.append(new_id[0])
                    # check if element exist in db. If exist return the value of field. otherwise extract the feature.
                    feature = descriptors.compute_hash_code(category, usecase, featureName, file1, file_type)
                    print(type(feature))
                    g_dict[str(new_id[0])] = feature
                    id.append(new_id[0])
            else:
                session = boto3.Session(aws_access_key_id='AKIAQFATZO2MKRGOETZE',aws_secret_access_key='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')
                s3 = session.resource('s3')
                s3_client = boto3.client('s3')
               
                first_str, file_name_remote = file_url.split('.com/')
                bucket_name = first_str.split('/')[2].split('.')[0]

                o = urlparse(file_url, allow_fragments=False)
                # s3_client.download_file('xreco-nmr', 'test/1.png', '1.png')
                file_name_local_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DATA')
                create_folder_if_not_exist(file_name_local_dir)
                #file_name_local_dir = 'DATA'
                #create_folder_if_not_exist('DATA')
                # print(file_name_local_dir)
                # print('I am in')
                print(file_name_remote)
                print(file_name_local_dir)
                filename = os.path.basename(file_name_remote)
                file_name_local = os.path.join(file_name_local_dir, filename)
                s3_client.download_file(bucket_name, file_name_remote, file_name_local)
                print('Finish download')

                #featureName = filename.split('.')[0]

                category, usecase = configure_usecase(featureName) #'name.gltf'
                file_type = get_file_type(filename_with_extension)
                feature = descriptors.compute_hash_code(category, usecase, featureName, file_name_local, file_type)
                # print(type(feature))
                g_dict[str(new_id[0])] = feature
                id.append(new_id[0])
                # Check response value later to include an elif
                # print(f"Failed to download file. Status code: {response.status_code}")
                # g_dict[str(new_id[0])] = -1
                if os.path.exists(file_name_local):
                    os.remove(file_name_local)
                    print('File deleted')
        except requests.RequestException as e:
            print(f"Request exception: {str(e)}")
            g_dict[str(new_id[0])] = -1

        return json.dumps({"jobId":str(new_id[0])})


#@ns.route('/extract/<featureName>/<jobId>')
@ns.route('/extract/<jobId>')
# @ns.expect(insert_show_data)
@ns.doc(responses={200: "Successful response", 404: 'Not Found', 500: 'Internal Server Error',503: 'Service Unavailable'})
class resultsApi2(Resource):
    def get(self, jobId: str): #post def get(self,featureName: str, jobId: str): #post
        global id
        global g_dict

        exist_jobId = int(jobId) in id 
        preprocess_jobId = jobId in g_dict

        print(jobId)
        print(id)
        print(g_dict)

        if exist_jobId and preprocess_jobId:
            if preprocess_jobId:
                preproccesed_feature = g_dict[jobId]
                if preproccesed_feature == -1:
                    return json.dumps({"status": status.cancelled.name})
                else:
                    return json.dumps({"status": status.completed.name, "result": preproccesed_feature})
        elif exist_jobId and not preprocess_jobId:
            return json.dumps({"status": status.ongoing.name})


def run_server_api():
    app.run(host='0.0.0.0', port=8000)  # Here we change IP to run locally (to any PC)


if __name__ == "__main__":
    run_server_api()
