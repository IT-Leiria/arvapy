""" @package flask_api
    Script used to launch the flask API
"""

import json
from flask import Flask, escape, request
from arvapy import ArvApyData

# Create Flask application
app = Flask(__name__)

# Persistent data of the ArvApy
arvapy = ArvApyData()

@app.route('/get_stream_list')
def Get360StreamList():
    """
    Returns list of available 360-degree streams

    This function returns a list of arrays with the following information:
    [name, width, height, bytes per pixel]

    Returns
    -------
    list
        list of arrays with the information above

    """
    return json.dumps(ArvApyData.Get360DegreeStreams())
  
@app.route('/select_stream')
def Select360Stream():
    """
    This function selects the desired 360-degree stream.

    Args:
        idx (integer): index of the video stream in the array 
                     returned by Get360StreamList

    Returns:
        int: 0 if succeeded (higher than 0 otherwise)
    """
    idx = request.args.get("idx", 0)
    return str(arvapy.Select360Stream(idx))
  
@app.route('/get_projections')
def GetProjectionList():
    """
    REST API Get list of projections

    This function returns the list of available planar projection formats

    Returns:
        json object: pair of projection initial and name
    """
    return json.dumps(ArvApyData.display_module.Get360DegreeProjections())

@app.route('/get_viewport_info')
def GetViewportInfo():
    """
    REST API Get Viewport Info

    This function returns the information regaring a viewport

    Args:
        x (integer): viewport horizontal center position in degrees
        y (integer): viewport vertical center position in degrees
        width (integer): width of the viewport in degree
        height (integer): height of the viewport in degrees

    Returns:
        json object: width and height of the viewport
    """
    viewport_x = request.args.get("x", 0)
    viewport_y = request.args.get("y", 0)
    viewport_width = request.args.get("width", 90)
    viewport_height = request.args.get("height", 90)
    viewport = arvapy.display_module.Get360DegreeViewPortFrame( viewport_x, viewport_y, viewport_width, viewport_height)
    frame_info = {}
    frame_info['width'] = viewport.width
    frame_info['height'] = viewport.height
    return json.dumps(frame_info)
  
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
    viewport = arvapy.display_module.Get360DegreeViewPortFrame( viewport_x, viewport_y, viewport_width, viewport_height)
    return viewport.data

@app.route('/get_frame_info')
def GetFrameInfo():
    """
    REST API Get Frame Info

    This function returns the information regarding a frame

    Args:
        projection (string): initials of the planar projection format of the output

    Returns:
        json object: width and height of the frame in a given projection
    """
    projection = request.args.get("projection", "NA")
    frame = arvapy.display_module.Get360DegreeFrame(projection)
    frame_info = {}
    frame_info['width'] = frame.width
    frame_info['height'] = frame.height
    return json.dumps(frame_info)
  
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
    frame = arvapy.display_module.Get360DegreeFrame(projection)
    return frame.data
  
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
    return arvapy.encoding_module.GetAvailableConfigFiles()


# Start point
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
