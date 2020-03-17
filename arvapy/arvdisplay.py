from .arv360stream import Arv360StreamInput
from .arv360frame import Arv360Frame
from .arv360convert import Arv360Convert, ConvertProjectionNameToInt, ConvertProjectionList

class ArvApyDisplay:
    def __init__(self):
        self.convert_function_module = Arv360Convert()
        self.input_stream = []
        self.min_frame_size = 8
      
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
    

    def Get360DegreeProjections():
        return ConvertProjectionList()
    
    def Get360DegreeFrame(self, projection="NA"):

        # Convert projection name to number
        
        projection = ConvertProjectionNameToInt(projection)

        # Get frame from original stream
        input_frame = Arv360Frame()
        input_frame.width = self.input_stream.width
        input_frame.height = self.input_stream.height
        input_frame.bytes_per_pixel = self.input_stream.bytes_per_pixel
        input_frame.projection = self.input_stream.projection
        input_frame.data = self.input_stream.ReadFrame()

        # Check if projection conversion is needed
        if projection == -1 or projection == self.input_stream.projection:
            return input_frame

        # Configure conversion function
        if self.convert_function_module.convert_to_projection != projection:
            self.convert_function_module.FinishConversion()
            self.convert_function_module.InitConversion(self.input_stream, projection)

        # Return converted frame
        return self.convert_function_module.ConvertFrame(input_frame.data)
      
    def Get360DegreeViewPortFrame(self, x, y, width, height ):

        viewport_center_x = int( x )
        viewport_center_y = int( y )
        width = int( width )
        height = int( height )
        
        viewport_width = self.AdjustDimension( self.input_stream.width * width /  360 )
        viewport_height = self.AdjustDimension( self.input_stream.height * height / 180 )
        
        viewport_settings = str(width) + " " + str(width) + " " + str(viewport_center_x) + " " +  str(viewport_center_y)
        
        # Rectilinear projection index
        projection = ConvertProjectionNameToInt("RECT")

        # Get frame from original stream
        input_frame = Arv360Frame()
        input_frame.width = self.input_stream.width
        input_frame.height = self.input_stream.height
        input_frame.bytes_per_pixel = self.input_stream.bytes_per_pixel
        input_frame.projection = self.input_stream.projection
        input_frame.data = self.input_stream.ReadFrame()

        # Check if projection conversion is needed
        if projection == -1 or projection == self.input_stream.projection:
            return input_frame

        # Configure conversion function
        if self.convert_function_module.convert_to_projection != projection:
            self.convert_function_module.FinishConversion()
            can_convert = self.convert_function_module.InitConversion(self.input_stream, projection, viewport_width, viewport_height, viewport_settings)
            if not can_convert:
                return input_frame

        # Return converted frame
        converted_frame = self.convert_function_module.ConvertFrame(input_frame.data)
        
        return converted_frame
