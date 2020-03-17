from .arv360stream import Arv360Stream

NumberOfStreams = 1

ArvApyStreamList = [ Arv360Stream() for i in range(NumberOfStreams)]

ArvApyStreamList[0].name = "/datasets/Turtle_3840x1920_30.yuv"
ArvApyStreamList[0].width = 3840
ArvApyStreamList[0].height = 1920
ArvApyStreamList[0].projection = 0
ArvApyStreamList[0].bytes_per_pixel = 1




def GetListOfAvailableStreams():
    stream_list = []
    for s in ArvApyStreamList:
        stream = [ s.name, s.width, s.height, s.bytes_per_pixel]
        stream_list.append( stream )
    return stream_list
