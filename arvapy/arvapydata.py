from .arv360stream import Arv360StreamInput
from .arv360convert import Arv360Convert, ConvertProjectionNameToInt, ConvertProjectionList


class ArvApyData:
    def __init__(self):
        self.convert_function_module = Arv360Convert()
        self.main_stream = None

        # DEBUG PURPOSE - Only work inside the IT cluster
        self.main_stream = Arv360StreamInput()
        self.main_stream.name = "/nfs/data/share/datasets/Salient360/Videos/Stimuli/16_Turtle_3840x1920_30fps.yuv"
        self.main_stream.width = 3840
        self.main_stream.height = 1920
        self.main_stream.projection = 0
        self.main_stream.bytes_per_pixel = 1
        self.main_stream.OpenStream()

    @staticmethod
    def Get360DegreeProjections():
        return ConvertProjectionList()

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
