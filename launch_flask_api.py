""" @package flask_api
    Script used to launch the flask API
"""

import json
from flask import Flask, escape, request
from arvapy import ArvApyData
from arvapy import ArvApyEncode

# Create Flask application
app = Flask(__name__)

# Persistent data of the ArvApy
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

@app.route('/get_projections')
def GetProjectionList():
    """
    REST API Get list of projections

    This function returns the list of available planar projection formats

    Returns:
        json object: pair of projection initial and name
    """
    return json.dumps(ArvApyData.Get360DegreeProjections())

@app.route('/get_viewport')
def GetViewport():
    """
    REST API Get Viewport

    This function returns a viewport of the current frame

    Args:
        x (integer): viewport horizontal center position in degrees
        y (integer): viewport vertical center position in degrees
        width (integer): width of the viewport in degree
        height (integer): height of the viewport in degrees

    Returns:
        byte array: generated viewport
    """
    viewport_x = request.args.get("x", 0)
    viewport_y = request.args.get("y", 0)
    viewport_width = request.args.get("width", 90)
    viewport_height = request.args.get("height", 90)
    viewport = arvapy.Get360DegreeViewPortFrame( viewport_x, viewport_y, viewport_width, viewport_height)
    return viewport

@app.route('/get_frame')
def GetFrame():
    """
    REST API Get Frame

    This function returns a new frame on every call

    Args:
        projection (string): initials of the planar projection format of the output

    Returns:
        byte array: new frame in raw format
    """
    projection = request.args.get("projection", "NA")
    frame = arvapy.Get360DegreeFrame(projection)
    return frame


# Start point
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
