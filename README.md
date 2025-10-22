# WP3-T3.2-3D-model-descriptors-extraction

This component does the 3D model descriptor extraction task for XRECO Project. XRECO is an HorizonEurope Innovation Project co-financed by the EC under Grant Agreement ID: 101070250.

It implements an analysis service to extract descriptors for 3D models. Once a request job has been created, the results can be polled via a job status query.

### Installation 
The docker and python code have been tested in Ubuntu 20.04 and python 3.10.

To build the docker type the following command
```code
docker build -t multimodal_image .
```
And to run the docker type the following command
```code
docker run -ti --rm --gpus all --network host -p 8000:8000 multimodal_image
```
### Service API 
The service API can be seen on http://localhost:8000/3D model retrieval/

#### Extracting descriptors for a 3D model
For extracting the descriptors of a 3D model only the file path (accessible by the server), minIO, or S3 URL ("data") of the 3D model has to  be specified. Please note as of v1.0.0 of the service only GLTF files are supported.
```code
curl -X 'POST' \
  'http://localhost:8000/3D model retrieval/extract/airplane_0627' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "https://xreco-nmr.s3.eu-west-1.amazonaws.com/test/airplane_0627.gltf",
  "start": 0,
  "end": 0,
  "last": true
}'
```
#####  Result JSON data:
```json
[
"{\"jobId\": \"741\"}"
]
```
#####  Get the descriptor of the 3D model
You can then get the extracted descriptor by calling the 2nd endpoint of the API using the feature name and job ID:
```code
curl -X 'GET' \
  'http://localhost:8000/3D model retrieval/extract/airplane_0627/741' \
  -H 'accept: application/json'
```
#####  Result JSON data:
```json
[
"{\"status\": \"completed\", \"result\": [0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0]}"
]
```
## Authors
Maria Pegia
Email: mpegia@iti.gr
Stamatis Samaras 
Email: sstamatis@iti.gr


## Licence 

Licence description or link to the licence.  
