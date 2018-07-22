import annoy 
from annoy import AnnoyIndex
import json 
import pickle 
import os 
import numpy as np


def save_features(features_filename, features, mapping_filename, file_mapping):
    """
    Save feature array and file_item mapping to disk
    :param features_filename: path to save features to
    :param features: array of features
    :param mapping_filename: path to save mapping to
    :param file_mapping: mapping from array_index to file_path/plaintext_word
    """
    with open('%s.p' % features_filename, 'wb') as fp:
        pickle.dump(features, fp, protocol=pickle.HIGHEST_PROTOCOL)
    #np.save('%s.npy' % features_filename, features)
    with open('%s.json' % mapping_filename, 'w') as index_file:
        json.dump(file_mapping, index_file)


def load_features(features_filename, mapping_filename):
    """
    Loads features and file_item mapping from disk
    :param features_filename: path to load features from
    :param mapping_filename: path to load mapping from
    :return: feature array and file_item mapping to disk
    """
    with open('%s.p' % features_filename, 'rb') as fp:
        image_features = pickle.load(fp)

    with open('%s.json' % mapping_filename) as f:
        index_str = json.load(f)
        file_index = {int(k): str(v) for k, v in index_str.items()}
    return image_features, file_index


def save_index(index, filename):
    index.save("{0}.ann".format(filename))
    print("Index saved!")


def load_index(filename, vector_size):
    index = AnnoyIndex(vector_size, metric="angular")
    index.load("{0}.ann".format(filename))
    return index 


def index_features(features, n_trees=1000, dims=4096):
    """
    Use Annoy to index our features to be able to query them rapidly
    :param features: array of item features
    :param n_trees: number of trees to use for Annoy. Higher is more precise but slower.
    :param dims: dimension of our features
    :return: an Annoy tree of indexed features
    """
    feature_index = AnnoyIndex(dims, metric='angular')
    for k, v in features.items():
        feature_index.add_item(k, v)
    feature_index.build(n_trees)
    return feature_index


def search_index_by_key(key, feature_index, item_mapping, top_n=10):
    """
    Search an Annoy index by key, return n nearest items
    :param key: the index of our item in our array of features
    :param feature_index: an Annoy tree of indexed features
    :param item_mapping: mapping from indices to paths/names
    :param top_n: how many items to return
    :return: an array of [index, item, distance] of size top_n
    """
    distances = feature_index.get_nns_by_item(key, top_n, include_distances=True)
    return [[a, item_mapping[a], distances[1][i]] for i, a in enumerate(distances[0])]


def search_index_by_value(vector, feature_index, item_mapping, top_n=10):
    """
    Search an Annoy index by value, return n nearest items
    :param vector: the index of our item in our array of features
    :param feature_index: an Annoy tree of indexed features
    :param item_mapping: mapping from indices to paths/names
    :param top_n: how many items to return
    :return: an array of [index, item, distance] of size top_n
    """
    distances = feature_index.get_nns_by_vector(vector, top_n, include_distances=True)
    return [[a, item_mapping[a], distances[1][i]] for i, a in enumerate(distances[0])]


def load_glove_vectors(glove_dir, glove_name='glove.6B.300d.txt'):
    """
    Mostly from keras docs here https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html
    Download GloVe vectors here http://nlp.stanford.edu/data/glove.6B.zip
    :param glove_name: name of pre-trained file
    :param glove_dir: directory in witch the glove file is located
    :return:
    """
    f = open(os.path.join(glove_dir, glove_name))
    embeddings_index = {}
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    print('Found %s word vectors.' % len(embeddings_index))
    return embeddings_index