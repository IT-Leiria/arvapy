from flask import Flask, escape, request
from arvapy import ArvApyData
from arvapy import ArvApyEncode

app = Flask(__name__)

arvapy = ArvApyData()

@app.route('/get_cfg_paths')
def GetCfgFiles():
    """
    Returns list of configuration files

    This function returns a list with the paths for
    all configuration (*.cfg) files found in the
    search path.

    Returns
    -------
    list
        list of paths to cfg files

    """
    enc = ArvApyEncode('path_to_vvc/EncApp')
    return enc.GetAvailableConfigFiles()

@app.route('/get_frame')
def GetFrame():
    projection = request.args.get("projection", -1)
    frame = arvapy.Get360DegreeFrame(projection)
    return frame


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
