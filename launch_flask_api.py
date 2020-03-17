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
encoder = ArvApyEncode('/src/vtm/bin/EncoderAppStatic')

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
    return encoder.GetAvailableConfigFiles()

@app.route('/get_qps')
def GetQPs():
    """
    REST API Get list of projections

    This function returns the list of usable QP values

    Returns:
        list: list with usable QPs
    """
    return encoder.GetQPValues()

@app.route('/set_encoder_params')
def SetEncodingParams(orig_yuv_path, rec_yuv_path, out_bin_path, cfg_files, qp):
    """
    REST API Get Viewport

    This function sets the necessary parameters for generating a valid encoding command

    Args:
        string orig_yuv_path: path to the sequence to be encoded
        string rec_yuv_pat: path where the reconstructed sequence after enconding is to be stored
        string out_bin_path: path where the compressed sequence is to be stored
        list cfg_files: list of strings containing the paths for the cofiguration files (as given by GetCfgFiles) to be used
        list qp: list of integers, containing the QP values to be used
    """
    encoder.SetCodingParameters(orig_yuv_path, rec_yuv_path, out_bin_path, cfg_files, qp)

@app.route('/lauch_enc_proc')
def LaunchEncodingProcess():
    """
    REST API Get Viewport

    This function lauches the encoding precesses defined by SetEncodingParams

    """
    encoder.GenEncodingCommand()
    encoder.PrintEncodigCommand()
    encoder.EncodeSequence()

@app.route('/get_projections')
def GetProjectionList():
    """
    REST API Get list of projections

    This function returns the list of available planar projection formats

    Returns:
        json object: pair of projection initial and name
    """
    return json.dumps(ArvApyData.Get360DegreeProjections())

@app.route('/get_viewport_info')
def GetViewportInfo():
    """
    REST API Get Viewport

    This function returns a viewport of the current frame

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
    viewport = arvapy.Get360DegreeViewPortFrame( viewport_x, viewport_y, viewport_width, viewport_height)
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
    viewport = arvapy.Get360DegreeViewPortFrame( viewport_x, viewport_y, viewport_width, viewport_height)
    return viewport.data

@app.route('/get_frame_info')
def GetFrameInfo():
    """
    REST API Get Frame

    This function returns a new frame on every call

    Args:
        projection (string): initials of the planar projection format of the output

    Returns:
        json object: width and height of the frame in a given projection
    """
    projection = request.args.get("projection", "NA")
    frame = arvapy.Get360DegreeFrame(projection)
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
    frame = arvapy.Get360DegreeFrame(projection)
    return frame.data


# Start point
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
