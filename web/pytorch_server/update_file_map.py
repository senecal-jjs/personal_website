import os 
import argparse
import embedding as em 

def update_file_map(image_path):
    image_embeddings, path_map = em.load_features(os.path.join(os.getcwd(), "embeddings/image_visual_features"),
                                                  os.path.join(os.getcwd(), "embeddings/file_map"))

    new_path_map = {}
    for i, file in path_map.items():
        paths = file.split("/")
        p = os.path.join(image_path, paths[-2], paths[-1])
        new_path_map[i] = p 

    em.save_features("embeddings/image_visual_features", image_embeddings, "embeddings/file_map", new_path_map)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filepath", required=True, help="path to image folder")
    args = vars(ap.parse_args())

    update_file_map(args["filepath"])