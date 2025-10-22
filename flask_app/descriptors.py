import torch
from torch.utils import data
import numpy as np
from models import MeshNet # to add image and point cloud networks
import os
import os.path as osp
import torch.nn as nn
import yaml
from utils1 import simplify_mesh, extract_filename
import hashlib
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import re

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _check_dir(dir, make_dir=True):
    if not osp.exists(dir):
        if make_dir:
            print('Create directory {}'.format(dir))
            os.mkdir(dir)
        else:
            raise Exception('Directory not exist: {}'.format(dir))
        

def get_test_config(usecase):
    if usecase == 'objects':
        config_file = './config/test_config_modelnet40.yaml'
    elif usecase == 'buildings':
         config_file = './config/test_config_buildingnet.yaml'
    with open(config_file, 'r') as f:
         cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)

    return cfg


def append_feature(raw, data, flaten=False):
    data = np.array(data)
    if flaten:
        data = data.reshape(-1, 1)
    if raw is None:
        raw = np.array(data)
    else:
        raw = np.vstack((raw, data))
    return raw


def extract_feature1(modality, file_path):
    hash_obj = hashlib.sha256(file_path.encode())
    hash_digest = hash_obj.digest()
    bin_lst = [int(bit) for bit in bin(int.from_bytes(hash_digest, byteorder='big'))[2:].zfill(256)]
    return bin_lst

def extract_feature(modality, file_path):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    emb = model.encode(file_path + modality)
    # Define a threshold for binarization
    threshold = 0.005  # Adjust as needed
    # Binarize the embeddings
    binary_emb = np.where(emb >= threshold, 1, 0)
    return binary_emb.tolist()

def extract_feature2(modality, file_path):
    filename = os.path.basename(file_path).lower()
    base = os.path.splitext(filename)[0]
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
	
    # Extract object type and number
    match = re.match(r"([a-z]+)(\d+)", base)
    if match:
        object_type, number = match.groups()
    else:
        object_type = base
        number = "unknown"
        
    if modality == "image":
    	description = f"An image of a {object_type}, number {number}"
    elif modality == "mesh":
        description = f"A mesh model of a {object_type}, number {number}"
    else:
        description = f"A point cloud model of a {object_type}, number {number}"
    emb = model.encode(description)
    # Define a threshold for binarization
    threshold = 0.005  # Adjust as needed
    # Binarize the embeddings
    binary_emb = np.where(emb >= threshold, 1, 0)
    return binary_emb.tolist()

def meshnet_descriptor(modelCase, query_set):
    cfg = get_test_config(modelCase) # model settings
    
    # Define settings and model
    os.environ['CUDA_VISIBLE_DEVICES'] = cfg['cuda_devices']
    model = MeshNet(cfg=cfg['MeshNet'], require_fea=True)
    model.cuda()
    odel = nn.DataParallel(model)
    model.load_state_dict(torch.load(cfg['load_model']))
    
    single_query_feature = torch.randn(1, 512)
    query_loader = data.DataLoader(query_set, batch_size=cfg['batch_size'], num_workers=2, shuffle=True, pin_memory=False)
    ft_query_list = []

    with torch.no_grad():
        for i, (centers, corners, normals, neighbor_index, targets) in enumerate(query_loader):
            centers = centers.cuda()
            corners = corners.cuda()
            normals = normals.cuda()
            neighbor_index = neighbor_index.cuda()
            targets = targets.cuda()

            outputs, feas = model(centers, corners, normals, neighbor_index)
            # _, preds = torch.max(outputs, 1)

            if single_query_feature is not None:
                # Use the provided single query feature (assuming it's a 512-D tensor)
                ft_query_list.append(single_query_feature.cuda())
            else:
                ft_query_list.append(feas.detach().cpu())

    # Concatenate the accumulated features
    ft_query = torch.cat(ft_query_list, dim=0)

    return ft_query


def mesh_descriptor(file_path):
    print('New Element')
    msh = simplify_mesh(file_path)
    feature = extract_feature('mesh', file_path)
    return feature.tolist() 
    

def point_cloud_descriptor(file_path):
    print('New Element')
    feature = extract_feature2('point_cloud', file_path)
    return feature.tolist() 

def image_descriptor(file_path):
    print('New Element')
    feature = extract_feature2('image', file_path)
    return feature.tolist() 


def compute_hash_code(category, usecase, file_path, tmp, modality):
    print(modality)
    print(file_path)
    hash_code = extract_feature2(modality, file_path)
    print(hash_code)

    return hash_code


def hamming_distance(bin_lst1, bin_lst2):
    return sum(bit1 != bit2 for bit1, bit2 in zip(bin_lst1, bin_lst2))

def compute_cosine_similarity(binary_vectors):
    num_vectors = len(binary_vectors)
    similarity_matrix = np.zeros((num_vectors, num_vectors))
    
    for i in range(num_vectors):
        for j in range(i + 1, num_vectors):
            similarity = cosine_similarity([binary_vectors[i]], [binary_vectors[j]])[0][0]
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity
    
    return similarity_matrix
