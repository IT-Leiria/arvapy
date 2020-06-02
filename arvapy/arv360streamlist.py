from .arv360stream import Arv360Stream

NumberOfStreams = 3

ArvApyStreamList = [ Arv360Stream() for i in range(NumberOfStreams)]

ArvApyStreamList[0].name = "/datasets/Turtle_3840x1920_30.yuv"
ArvApyStreamList[0].width = 3840
ArvApyStreamList[0].height = 1920
ArvApyStreamList[0].projection = 0
ArvApyStreamList[0].bytes_per_pixel = 1
ArvApyStreamList[0].num_layers = 1

ArvApyStreamList[1].name = "/datasets/SkateboardTrick_le_8192x4096.yuv"
ArvApyStreamList[1].width = 8192
ArvApyStreamList[1].height = 4096
ArvApyStreamList[1].projection = 0
ArvApyStreamList[1].bytes_per_pixel = 1
ArvApyStreamList[1].num_layers = 1

ArvApyStreamList[2].name = "/datasets/Foreman_CIF.yuv"
ArvApyStreamList[2].width = 352
ArvApyStreamList[2].height = 288
ArvApyStreamList[2].projection = 0
ArvApyStreamList[2].bytes_per_pixel = 1
ArvApyStreamList[2].num_layers = 1



def GetListOfAvailableStreams():
    stream_list = []
    for s in ArvApyStreamList:
        stream = [ s.name, s.width, s.height, s.bytes_per_pixel, s.num_layers]
        stream_list.append( stream )
    return stream_list
