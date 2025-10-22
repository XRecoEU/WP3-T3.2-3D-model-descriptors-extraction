import pymeshlab
import os
import imghdr


categories = {
    'buildings': {'house': 1, 'mosque': 1, 'hotel_building': 1, 'cathedral': 1, 'monastery': 1, 'church': 1, 'villa': 1, 'city_hall': 1, 'school_building': 1, 'museum': 1, 'temple': 1, 'office_building': 1, 'palace': 1, 'factory': 1, 'castle': 1},
    'objects': {'airplane': 1, 'bathtub': 1, 'bed': 1, 'bench': 1, 'bookshelf': 1, 'bottle': 1, 'bowl': 1, 'car': 1, 'chair': 1, 'cone': 1, 'cup': 1, 'curtain': 1, 'desk': 1, 'door': 1, 'dresser': 1, 'flower_pot': 1, 'glass_box': 1, 'guitar': 1, 'keyboard': 1, 'lamp': 1, 'laptop': 1, 'mantel': 1, 'monitor': 1, 'night_stand': 1, 'person': 1, 'piano': 1, 'plant': 1, 'radio': 1, 'range_hood': 1, 'sink': 1, 'sofa': 1, 'stairs': 1, 'stool': 1, 'table': 1, 'tent': 1, 'toilet': 1, 'tv_stand': 1, 'vase': 1, 'wardrobe': 1, 'xbox': 1, 'phone': 1}
}


class UnknownFileTypeError(Exception):
    pass


def get_file_type(file_path):
    try:
        image_extensions = {'.jpeg', '.jpg', '.png'}
        mesh_extensions = {'.obj', '.gltf'}
        point_cloud_extensions = {'.ply'}

        ext = os.path.splitext(file_path)[1].lower()
        # print('Extension: ' + str(ext))
        if ext in mesh_extensions:
            return "mesh"
        elif ext in image_extensions:
            return "image"
        elif ext in point_cloud_extensions:
            return "point_cloud"
        else:
            raise UnknownFileTypeError("Unknown file type")
    except Exception as e:
        return f"error: {str(e)}"


def create_folder_if_not_exist(pth):
    if not os.path.exists(pth):
        print(f'Creating directory: {pth}')
        os.makedirs(pth)
    else:
        print(pth)  
        #print('not created')


def read_file_as_list(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def save_to_file(data, outputfile):
    with open(outputfile, 'w') as f:
        for val in data:
            f.write(val + '\n')


def UsecaseNotFoundError(Exception):
    pass


def configure_usecase(string_to_check):
    for category_name, items in categories.items():
        for key in items:
            if key in string_to_check:
                return key, category_name
    #raise UsecaseNotFoundError(f"FeatureName '{string_to_check}' not supported from the API.")
    return 'None', 'dummy'
    

def key_exists(dictionary, key):
    return key in dictionary


def simplify_mesh(input_path, target_faces=500):
    ms = pymeshlab.MeshSet()
    ms.clear()

    try:
        # Load the input mesh
        ms.load_new_mesh(input_path)
        mesh = ms.current_mesh()

        # Perform quadric edge collapse decimation for simplification
        ms.simplification_quadric_edge_collapse_decimation(targetfacenum=target_faces, preservenormal=True)
        simplified_mesh = ms.current_mesh()

        # Save the simplified mesh
        output_dir = os.path.join(os.path.dirname(input_path), 'Modified')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(input_path))
        ms.save_current_mesh(output_path)
        
        simplified_content = simplified_mesh.get_mesh_raw()
        return simplified_content

    except Exception as e:
        print(f"Error simplifying mesh: {e}")


def extract_filename(full_path):
    filename_with_extension = os.path.basename(full_path)
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    return filename_without_extension
