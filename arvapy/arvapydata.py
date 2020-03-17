from .arv360stream import Arv360StreamInput
from .arv360frame import Arv360Frame
from .arvencode import ArvApyEncode
from .arvdisplay import ArvApyDisplay
from .arv360streamlist import ArvApyStreamList, GetListOfAvailableStreams
from .arv360convert import ConvertProjectionList

class ArvApyData:
    def __init__(self):
        self.display_module = ArvApyDisplay()
        self.encoding_module = ArvApyEncode('/src/vtm/bin/EncoderAppStatic')
        
        self.main_stream = None
        
        # DEBUG PURPOSE - Only work inside the IT cluster
        #self.main_stream = Arv360StreamInput()
        #self.main_stream.name = "/datasets/Turtle_3840x1920_30.yuv"
        ##self.main_stream.name = "/nfs/home/jcarreira.it/AroundVision/API/arvapy/docker/test_material/Turtle_3840x1920_30.yuv"
        #self.main_stream.width = 3840
        #self.main_stream.height = 1920
        #self.main_stream.projection = 0
        #self.main_stream.bytes_per_pixel = 1
        #self.main_stream.OpenStream()
        
    
    @staticmethod
    def Get360DegreeStreams():
        return GetListOfAvailableStreams()
      
  
    """
        Resets the API.

        This function should be call everything that 
        needs to be clean when reseting API.
        For example with stream changes
    """
    def FlushData(self):
      self.display_module.convert_function_module.FinishConversion()
      
      
    def Select360Stream(self, idx):
      
      idx = int(idx)
      if idx >= len( ArvApyStreamList ):
        return 1
      
      self.FlushData()
      self.main_stream = Arv360StreamInput( ArvApyStreamList[idx] )
      self.main_stream.OpenStream()
      
      self.display_module.SetStream(self.main_stream)
      return 0
      




