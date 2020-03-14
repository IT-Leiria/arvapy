from .arv360stream import Arv360StreamInput
from .arvencode import ArvApyEncode
from .arv360convert import Arv360Convert, ConvertProjectionNameToInt, ConvertProjectionList


class ArvApyData:
    def __init__(self):
        self.convert_function_module = Arv360Convert()
        self.encoding_module = ArvApyEncode('path_to_vvc/EncApp')
        
        self.main_stream = None
        self.min_frame_size = 8
        
        # DEBUG PURPOSE - Only work inside the IT cluster
        self.main_stream = Arv360StreamInput()
        self.main_stream.name = "/nfs/data/share/datasets/Salient360/Videos/Stimuli/16_Turtle_3840x1920_30fps.yuv"
        self.main_stream.width = 3840
        self.main_stream.height = 1920
        self.main_stream.projection = 0
        self.main_stream.bytes_per_pixel = 1
        self.main_stream.OpenStream()
        
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
      
    @staticmethod
    def Get360DegreeProjections():
        return ConvertProjectionList()
      
    def GetAvailableConfigFiles(self):
      return self.encoding_module.GetAvailableConfigFiles()

    def Get360DegreeFrame(self, projection="NA"):

        # Convert projection name to number
        projection = ConvertProjectionNameToInt(projection)

        # Get frame from original stream
        frame = self.main_stream.ReadFrame()

        # Check if projection conversion is needed
        if projection == -1 or projection == self.main_stream.projection:
            return frame

        # Configure conversion function
        if self.convert_function_module.convert_to_projection != projection:
            self.convert_function_module.FinishConversion()
            self.convert_function_module.InitConversion(self.main_stream, projection)

        # Return converted frame
        return self.convert_function_module.ConvertFrame(frame)
    
    def Get360DegreeViewPortFrame(self, x, y, width, height ):

        viewport_center_x = int( x )
        viewport_center_y = int( y )
        width = int( width )
        height = int( height )
        
        viewport_width = self.AdjustDimension( self.main_stream.width * width /  360 )
        viewport_height = self.AdjustDimension( self.main_stream.height * height / 180 )
        
        viewport_settings = str(width) + " " + str(width) + " " + str(viewport_center_x) + " " +  str(viewport_center_y)
        
        # Rectilinear projection index
        projection = 4

        # Get frame from original stream
        frame = self.main_stream.ReadFrame()

        # Check if projection conversion is needed
        if projection == -1 or projection == self.main_stream.projection:
            return frame

        # Configure conversion function
        if self.convert_function_module.convert_to_projection != projection:
            self.convert_function_module.FinishConversion()
            self.convert_function_module.InitConversion(self.main_stream, projection, viewport_width, viewport_height, viewport_settings)

        # Return converted frame
        return self.convert_function_module.ConvertFrame(frame)




