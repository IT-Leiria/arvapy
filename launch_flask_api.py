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
    [name, width, height, bytes per pixel, number of layers]

    Returns
    -------
    list
        list of arrays with the following information:
          [name, width, height, bytes per pixel, number of layers]

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

@app.route('/get_projection_list')
def GetProjectionList():
    """
    REST API Get list of projections

    This function returns the list of available planar projection formats

    Returns:
        json object: pair of projection initial and name
    """
    return json.dumps(arvapy.display_module.Get360DegreeProjections())

@app.route('/get_number_faces')
def GetNumberOfFaces():
    """
        REST API Get Number of Faces/Sides

        This function returns the number of faces/sides of
        a given projection of 360-degree video frame.

        Args:
            projection (string): initials of the planar projection format of the output
            (default means cube-map projection)

        Returns:
            int: number of faces/sides
    """
    p = request.args.get("projection", "NA")
    return json.dumps(str(6))

@app.route('/get_layer_info')
def GetLayerInfo():
    """
    REST API Get Layer Info

    This function returns the information regarding the available layer of a given stream

    Args:
         idx (integer): index of the video stream in the array
                     returned by Get360StreamList

    Returns:
        json object: list of pairs (layer idx, layer description)
    """
    idx = request.args.get("idx", 0)
    return json.dumps(arvapy.GetLayerInfo(idx))

@app.route('/get_frame_info')
def GetFrameInfo():
    """
    REST API Get Frame Info

    This function returns the information regarding a frame

    Args:
        projection (string): initials of the planar projection format of the output
        layer (integer): layer to return (default means highest layer)

    Returns:
        json object: width, height and bytes/pixel of the frame in a given projection
    """
    p = request.args.get("projection", "NA")
    l = request.args.get("layer", "-1")
    frame = arvapy.display_module.Get360DegreeFrameInfo(projection=p, layer=l)
    frame_info = {}
    frame_info['width'] = frame.width
    frame_info['height'] = frame.height
    frame_info['Bpp'] = frame.bytes_per_pixel
    frame_info['byte_length'] = len( frame.rawData() )
    frame_info['bitrate'] = frame.bitrate
    return json.dumps(frame_info)

@app.route('/get_frame_raw')
def GetFrameRaw():
    """
    REST API Get Frame Raw

    This function returns a new raw frame (no signalling) on every call

    Args:
        projection (string): initials of the planar projection format of the output
        layer (integer): layer to return (default means highest layer)

    Returns:
        byte array: new frame in raw format
    """
    p = request.args.get("projection", "NA")
    l = request.args.get("layer", "-1")
    frame = arvapy.display_module.Get360DegreeFrame(projection=p, layer=l)
    return frame.rawData()

@app.route('/get_frame')
def GetFrame():
    """
    REST API Get Frame

    This function returns a new frame on every call
    At the beginning of the byte stream a sequence of ASCII chars are sent:
      [width]x[height]\n
      [bytes per pixel (Bpp)]\n
      ( width * height * Bpp ) pixels bytes

    Args:
        projection (string): initials of the planar projection format of the output
        (default means original projection)

        layer (integer): layer to return (default means highest layer)

    Returns:
        header + byte array: new frame
    """
    p = request.args.get("projection", "NA")
    l = request.args.get("layer", "-1")
    frame = arvapy.display_module.Get360DegreeFrame(projection=p, layer=l)
    return frame.formatedData()

@app.route('/get_projection_face_info')
def GetProejctionFaceInfo():
    """
    REST API Get Proejction Face Info

    This function returns part of the 360-degree video frame.
    For example it returns a face of a polyhedron-based projection.

    Currently, it will always return a face of the cube-map projection.
    In future it will return a frame from each projection selected.

    Args:
        projection (string): initials of the planar projection format of the output
        (default means cube-map projection)

        face (integer): the number of the face

        layer (integer): layer to return (default means highest layer)

    Returns:
        json object: width, height and bytes/pixel of the frame containingthe a face of a given projection
    """
    p = request.args.get("projection", "CMP")
    f = request.args.get("face")
    l = request.args.get("layer", "-1")
    frame = arvapy.display_module.Get360DegreeProjectionFaceInfo(projection=p, face_id=f, layer=l)
    frame_info = {}
    frame_info['width'] = frame.width
    frame_info['height'] = frame.height
    frame_info['Bpp'] = frame.bytes_per_pixel
    frame_info['byte_length'] = len( frame.rawData() )
    frame_info['bitrate'] = frame.bitrate
    return json.dumps(frame_info)


@app.route('/get_projection_face_raw')
def GetProjectionFaceRaW():
    """
    REST API Get Projection Face Raw

    This function returns part of the 360-degree video frame.
    For example it returns a face of a polyhedron-based projection.

    Currently, it will always return a face of the cube-map projection.
    In future it will return a frame from each projection selected.

    Args:
        projection (string): initials of the planar projection format of the output
        (default means cube-map projection)

        face (integer): the number of the face

        layer (integer): layer to return (default means highest layer)

    Returns:
        byte array: new frame in raw format
    """
    p = request.args.get("projection", "CMP")
    f = request.args.get("face")
    l = request.args.get("layer", "-1")
    frame = arvapy.display_module.Get360DegreeProjectionFace(projection=p, face_id=f, layer=l)
    return frame.rawData()


@app.route('/get_projection_face')
def GetProjectionFace():
    """
    REST API Get Projection Face

    This function returns part of the 360-degree video frame.
    For example it returns a face of a polyhedron-based projection.

    Currently, it will always return a face of the cube-map projection.
    In future it will return a frame from each projection selected.

    At the beginning of the byte stream a sequence of ASCII chars are sent:
      [width]x[height]\n
      [bytes per pixel (Bpp)]\n
      ( width * height * Bpp ) pixels bytes

    Args:
        projection (string): initials of the planar projection format of the output
        (default means cube-map projection)

        face (integer): the number of the face

        layer (integer): layer to return (default means highest layer)

    Returns:
        header + byte array: new frame
    """
    p = request.args.get("projection", "CMP")
    f = request.args.get("face")
    l = request.args.get("layer", "-1")
    frame = arvapy.display_module.Get360DegreeProjectionFace(projection=p, face_id=f, layer=l)
    return frame.formatedData()

@app.route('/get_viewport_info')
def GetViewportInfo():
    """
    REST API Get Viewport Info

    This function returns the information regaring a viewport

    Args:
        coord (str): coordinate system (pixel, polar)
        x (integer): viewport horizontal center position in degrees
        y (integer): viewport vertical center position in degrees
        width (integer): width of the viewport in degree
        height (integer): height of the viewport in degrees
        layer (integer): layer to return (default means highest layer)

    Returns:
        json object: width and height of the viewport
    """
    coordinates = request.args.get("coord", "pixel")
    viewport_x = request.args.get("x", 0)
    viewport_y = request.args.get("y", 0)
    viewport_width = request.args.get("width", 90)
    viewport_height = request.args.get("height", 90)
    layer = request.args.get("layer", -1)
    viewport = arvapy.display_module.Get360DegreeViewportInfo(coordinates, viewport_x, viewport_y, viewport_width, viewport_height, layer)
    viewport_info = {}
    viewport_info['width'] = viewport.width
    viewport_info['height'] = viewport.height
    viewport_info['Bpp'] = viewport.bytes_per_pixel
    viewport_info['byte_length'] = len( viewport.rawData() )
    viewport_info['bitrate'] = viewport.bitrate
    return json.dumps(viewport_info)

@app.route('/get_viewport_raw')
def GetViewportRaw():
    """
    REST API Get Viewport Raw

    This function returns a viewport of the current frame

    Args:
        coord (str): coordinate system (pixel, polar)
        x (integer): viewport horizontal center position (pixel or degree)
        y (integer): viewport vertical center position (pixel or degree)
        width (integer): width of the viewport (pixel or degree)
        height (integer): height of the viewport (pixel or degree)
        layer (integer): layer to return (default means highest layer)

    Returns:
        byte array: generated viewport
    """
    coordinates = request.args.get("coord", "pixel")
    viewport_x = request.args.get("x", 0)
    viewport_y = request.args.get("y", 0)
    viewport_width = request.args.get("width", 90)
    viewport_height = request.args.get("height", 90)
    layer = request.args.get("layer", -1)
    next_frame = request.args.get("next_frame", 0)

    viewport = arvapy.display_module.Get360DegreeViewport(coordinates, viewport_x, viewport_y, viewport_width, viewport_height, layer, next_frame)
    return viewport.rawData()

@app.route('/get_viewport')
def GetViewport():
    """
    REST API Get Viewport

    This function returns a new frame with the desired viewport on every call
    At the beginning of the byte stream a sequence of ASCII chars are sent:
      [width]x[height]\n
      [bytes per pixel (Bpp)]\n
      ( width * height * Bpp ) pixels bytes


    Args:
        coord (str): coordinate system (pixel, polar)
        x (integer): viewport horizontal center position in degrees
        y (integer): viewport vertical center position in degrees
        width (integer): width of the viewport in degree
        height (integer): height of the viewport in degrees
        layer (integer): layer to return (default means highest layer)

    Returns:
        header + byte array: generated viewport
    """
    coordinates = request.args.get("coord", "pixel")
    viewport_x = request.args.get("x", 0)
    viewport_y = request.args.get("y", 0)
    viewport_width = request.args.get("width", 90)
    viewport_height = request.args.get("height", 90)
    layer = request.args.get("layer", -1)
    viewport = arvapy.display_module.Get360DegreeViewport(coordinates, viewport_x, viewport_y, viewport_width, viewport_height, layer)
    return viewport.formatedData()


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
    arvapy.encoding_module.SetCodingParameters(orig_yuv_path, rec_yuv_path, out_bin_path, cfg_files, qp)

@app.route('/lauch_enc_proc')
def LaunchEncodingProcess():
    """
    REST API Get Viewport

    This function lauches the encoding precesses defined by SetEncodingParams

    """
    arvapy.encoding_module.GenEncodingCommand()
    arvapy.encoding_module.PrintEncodigCommand()
    arvapy.encoding_module.EncodeSequence()

# Start point
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
