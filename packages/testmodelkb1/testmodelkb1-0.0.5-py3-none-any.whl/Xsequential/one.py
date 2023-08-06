import os, json
dir_path = os.getcwd()
# our xFit and XMODEL class will be defined here
from Xsequential.app import sendData, activate, make_tree


def xFit():
    # sample data to be sent to View

    model_name = 'Gharib'
    metadata = {'epochs': 20, 'Hidden Layers': 2}

    #dirs = json.dumps(make_tree(dir_path + "/rawdata/"), indent=2, sort_keys=True)
    dirs = make_tree(dir_path + "/rawdata/")
    # pass data to FLask
    sendData(model_name, metadata, dirs)

    # run the app -Flask
    activate()


xFit()