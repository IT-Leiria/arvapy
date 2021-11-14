from .arv360stream import Arv360StreamInput
from .arv360frame import Arv360Frame
from .arv360convert import Arv360Convert, ConvertProjectionNameToInt, ConvertProjectionList

class ArvApyDisplay:
    def __init__(self):
        self.convert_function_module = Arv360Convert()
        self.viewport_function_module = Arv360Convert()
        self.input_stream = []
        self.min_frame_size = 8

        self.has_buffered_frame = False
        self.buffered_frame = []

        self.last_read_frame = []

    def SetStream(self, stream):
        self.input_stream = stream

    def AdjustDimension(self, dim, direction = 0):
        if direction == 0:
            ret = round(dim/self.min_frame_size,0)*self.min_frame_size
        elif direction == -1:
            ret = int(dim/self.min_frame_size)*self.min_frame_size
        elif direction == 1:
            ret = -1
        if ret == -1:
            raise
        return int(ret)

    def CheckBufferedFrame(self, projection, layer ):
        if self.has_buffered_frame:
            if self.buffered_frame.projection == projection and \
                self.buffered_frame.layer == layer:
                return self.buffered_frame
        return None


    def Get360DegreeProjections(self):
        return ConvertProjectionList()

    def Get360DegreeFrameInfo(self, projection="NA", layer=-1):
        """
        This functions get a new frame in order to extract the information
        but buffers it until next call of Get360DegreeFrame
        """
        layer = int(layer)
        # Always return the highest layer, regardless of the request
        if layer < 0 or layer > self.input_stream.num_layers:
            layer = self.input_stream.num_layers - 1

        frame = self.CheckBufferedFrame( ConvertProjectionNameToInt(projection), layer)
        if not frame == None:
            print("Re-using buffered frame!")
            return frame

        frame = self.Get360DegreeFrame(projection, layer)
        self.buffered_frame = frame
        self.has_buffered_frame = True
        return frame

    def Get360DegreeFrame(self, projection="NA", layer=-1):

        layer = int(layer)
        # Always return the highest layer, regardless of the request
        if layer < 0 or layer > self.input_stream.num_layers:
            layer = self.input_stream.num_layers - 1

        # Convert projection name to number
        projection = ConvertProjectionNameToInt(projection)

        frame = self.CheckBufferedFrame( projection, layer)
        if not frame == None:
            print("Re-using buffered frame!")
            self.has_buffered_frame = False
            return frame

        # Get frame from original stream
        input_frame = Arv360Frame()
        input_frame.width = self.input_stream.GetWidth( layer )
        input_frame.height = self.input_stream.GetHeight( layer )
        input_frame.bytes_per_pixel = self.input_stream.bytes_per_pixel
        input_frame.projection = self.input_stream.projection
        input_frame.data = self.input_stream.ReadFrame( layer )
        input_frame.layer = layer
        input_frame.bitrate = self.input_stream.GetBitrate( layer )

        self.last_read_frame = input_frame

        # Check if projection conversion is needed
        if projection == -1 or projection == self.input_stream.projection:
            return input_frame

        # Configure conversion function
        if self.convert_function_module.convert_to_projection != projection:
            self.convert_function_module.FinishConversion()
            self.convert_function_module.InitConversion(self.input_stream, projection)

        # Return converted frame
        return self.convert_function_module.ConvertFrame(input_frame)

    def Crop360DegreeFrameToFace(self, org_frame, projection, face_id):
        face_id = int( face_id )
        if projection == "CMP":
            face_y = int( face_id / 3)
            face_x = int( face_id - face_y * 3 )

            x_pos = int( org_frame.width / 3 * face_x )
            y_pos = int( org_frame.height / 2 * face_y )
            face_width = int( org_frame.width / 3 )
            face_height = int( org_frame.height / 2 )

            face_frame = org_frame.cropFrame( x_pos, y_pos, face_width, face_height )

            return face_frame

        return org_frame

    def Get360DegreeProjectionFaceInfo(self,  projection, face_id, layer=-1):
        frame = self.Get360DegreeFrameInfo(projection, layer)
        return self.Crop360DegreeFrameToFace(frame, projection, face_id )

    def Get360DegreeProjectionFace(self, projection, face_id, layer=-1):
        # this case if for when we do not want the next frame
        #frame = self.Get360DegreeFrameInfo(projection, layer)
        frame = self.Get360DegreeFrame(projection, layer)
        return self.Crop360DegreeFrameToFace(frame, projection, face_id )


    def Get360DegreeViewportInfo(self, coord_type, x, y, width, height, layer ):
        """
        This functions get a new viewport in order to extract the information
        but buffers it untill next call of Get360DegreeViewport
        """
        layer = int(layer)
        # Always return the highest layer, regardless of the request
        if layer < 0 or layer > self.input_stream.num_layers:
            layer = self.input_stream.num_layers - 1

        frame = self.CheckBufferedFrame( ConvertProjectionNameToInt("RECT"), layer)
        if not frame == None:
            print("Re-using buffered frame!")
            return frame

        frame = self.Get360DegreeViewport(coord_type, x, y, width, height, layer, next_frame=0)
        self.buffered_frame = frame
        self.has_buffered_frame = True
        return frame

    def Get360DegreeViewport(self, coord_type, x, y, width, height, layer, next_frame ):

        layer = int(layer)
        # Always return the highest layer, regardless of the request
        if layer < 0 or layer > self.input_stream.num_layers:
            layer = self.input_stream.num_layers - 1 - 1

        frame = self.CheckBufferedFrame( ConvertProjectionNameToInt("RECT"), layer)
        if not frame == None:
            print("Re-using buffered frame!")
            self.has_buffered_frame = False
            return frame

        x = float( x )
        y = float( y )
        width = float( width )
        height = float( height )

        if coord_type == "pixel":
            # TODO: Fix conversion from x,y to angular coordinates
            viewport_center_x = ( x - self.input_stream.GetWidth() / 2 ) / self.input_stream.GetWidth() * 2 * 180
            viewport_center_y = (  self.input_stream.GetHeight() / 2 - y ) / self.input_stream.GetHeight() * 2 * 90
            angular_width = int( width / self.input_stream.GetWidth() * 360 )
            angular_height = int( height / self.input_stream.GetHeight() * 180 )
        elif coord_type == "polar":
            viewport_center_x = x
            viewport_center_y = y
            angular_width = width
            angular_height = height
        else:
            raise "Invalid coordinate system"

        viewport_ratio = angular_width * angular_height / (360 * 180)

        # Width is estimated from the size of the original stream
        viewport_width = self.AdjustDimension( self.input_stream.GetWidth() * angular_width /  360 )
        viewport_height = self.AdjustDimension( self.input_stream.GetHeight() * angular_height / 180 )

        viewport_settings = str(angular_width) + " " + str(angular_height) + " " + str(viewport_center_x) + " " +  str(viewport_center_y)

        # Rectilinear projection index
        projection = ConvertProjectionNameToInt("RECT")

        # Get frame from original stream
        # input_frame = Arv360Frame()
        # input_frame.width = self.input_stream.width
        # input_frame.height = self.input_stream.height
        # input_frame.bytes_per_pixel = self.input_stream.bytes_per_pixel
        # input_frame.projection = self.input_stream.projection
        # input_frame.data = self.input_stream.ReadFrame()

        if next_frame:
            input_frame = self.Get360DegreeFrame(layer=layer)
        else:
            input_frame = self.last_read_frame

        new_hash = hash( "aw"+str(angular_width)+"ah"+str(angular_height)+"vx"+str(viewport_center_x)+"vy"+str(viewport_center_y))

        # Configure conversion function
        if self.viewport_function_module.convertion_hash != new_hash:
            self.viewport_function_module.FinishConversion()
            self.viewport_function_module.InitConversion(self.input_stream, projection, viewport_width, viewport_height, viewport_settings)
            self.viewport_function_module.convertion_hash = new_hash

        # Return converted frame
        converted_frame = self.viewport_function_module.ConvertFrame(input_frame)
        # Currently make viewport bitrate be proportional to the total bitrate.
        # TODO: improve bitrate calculation
        converted_frame.bitrate = input_frame.bitrate * viewport_ratio
        return converted_frame
