

# load required libraries
from sklearn.externals import joblib
import subprocess

def push_models():
    """
    Pushes models from current project
    """
    sp = subprocess.Popen(["/bin/bash", "-i", "-c", "mlm push models"])
    sp.communicate()

def pull_models():
    """
    Pulls models from current project
    :return:
    """

def load_model(path, version=None):
    """
    Load a model from disk
    :param path: location of the model
    :param version: defines requested version(None == latest)
    :return: model
    """
    return 3

def save_model(model, path):
    """
    Saves a model to disk
    :param model_name: model
    :param path: save location
    """
    x = 3