
import json
import logging
from flask import Flask, request
#from flask_basicauth import BasicAuth
from flask_restx import Api, Resource, fields
import requests
import random
from enum import Enum

class status(Enum):
    completed = 1
    ongoing = 2
    cancelled = 3

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

api = Api(app, version='1.0', title='3D model descriptor extraction API',
          description='An API for requesting the descriptors of 3D models to be used for 3D object retrieval')

ns = api.namespace('3D model retrieval', description='List of endpoint for requesting the descriptor extraction')
#app.config['BASIC_AUTH_USERNAME'] = 'xreco_admin'
#app.config['BASIC_AUTH_PASSWORD'] = 'xreco_@dmin_2023'

#basic_auth = BasicAuth(app)

""" Model for inserting a new show into a database """
insert_show_data = ns.model('Data to be processed from min.io',{
    "data" : fields.String(description="The min.io URL of the object to be processed", required=True),
    "start" : fields.Float(description="The start time of the segment to be processed", required=False),
    "end" : fields.Float(description="The end time of the segment to be processed", required=False),
    "last" : fields.Boolean(description="Optional parameter indicating that the segment represents the last frame", required=False),
                            
})

id=[]

@ns.route('/extract/<featureName>')
@ns.expect(insert_show_data)
@ns.doc(responses={200: "Successful response", 404: 'Not Found', 500: 'Internal Server Error',503: 'Service Unavailable'})
class resultsApi(Resource):
    def post(self,featureName: str):
        global id
        json_data = request.json
        print(json_data)
        print(featureName)
        #args = upload_parser.parse_args()
        file_url = json_data['data']
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                # Assuming the file is downloaded successfully
                with open(featureName+'.gltf', 'wb') as file:
                    file.write(response.content)
                    print("File downloaded successfully")
                    # You can further process the downloaded file here
                    new_id=random.sample(range(0, 10000), 1)
                    
                    id.append(new_id[0])
                    #id2=[new_id[0],b]
                    #TO add feature extraction part

            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request exception: {str(e)}")
        
        #Check if on the fly transformation
        """
        
        
        if('gltf' in file.filename):
            with open(os.path.splitext("C:/Users/sstamatis/Desktop/server/3Dmodels/"+file.filename)[0]+'.gltf', 'wb') as f:
                f.write(file.read())
            return json.dumps({"descriptors":b})
        if('obj' in file.filename):
            with open(os.path.splitext("C:/Users/sstamatis/Desktop/server/3Dmodels/"+file.filename)[0]+'.obj', 'wb') as f:
                f.write(file.read())
            return json.dumps({"descriptors":b})
        else:
            return json.dumps({"response":"File not supported"})
        """
        return json.dumps({"jobId":str(new_id[0])})
        

@ns.route('/extract/<featureName>/<jobId>')
#@ns.expect(insert_show_data) @Maria latest changes 
@ns.doc(responses={200: "Successful response", 404: 'Not Found', 500: 'Internal Server Error',503: 'Service Unavailable'})
class resultsApi2(Resource):
    def get(self,featureName: str, jobId: str): #@Maria latest changes from post to get
        global id
        print(featureName)
        print(jobId)
        
        print(id)
        b = [ 
                1.0, 
                1.0, 
                1.0, 
                1.0, 
                0.0, 
                1.0, 
                1.0, 
                1.0, 
                0.0, 
                1.0, 
                0.0, 
                1.0, 
                0.0, 
                0.0, 
                1.0, 
                1.0, 
                0.0, 
                1.0, 
                1.0, 
                1.0, 
                0.0, 
                0.0, 
                0.0, 
                1.0, 
                1.0, 
                0.0, 
                0.0, 
                1.0, 
                1.0, 
                0.0, 
                1.0, 
                1.0
            ]
        
        if (int(jobId) in id):
            if (len(b)==0):
                return json.dumps({"status":status.ongoing.name})
            else:
                return json.dumps({"status":status.completed.name, "result":b})
        else:
            return json.dumps({"status":status.cancelled.name})

def run_server_api():
    app.run(host='0.0.0.0', port=5000) #to add IP of server
  

  
if __name__ == "__main__":     
    run_server_api()
