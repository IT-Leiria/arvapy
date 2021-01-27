from .arv360stream import Arv360Stream

NumberOfStreams = 5

ArvApyStreamList = [ Arv360Stream() for i in range(NumberOfStreams)]
n = -1

n += 1
ArvApyStreamList[n].name = "Turtle"
ArvApyStreamList[n].filename = "/datasets/Turtle_3840x1920_30.yuv"
ArvApyStreamList[n].width = 3840
ArvApyStreamList[n].height = 1920
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 1

n += 1
ArvApyStreamList[n].name = "SkateboardTrick"
ArvApyStreamList[n].filename = "/datasets/SkateboardTrick_le_8192x4096.yuv"
ArvApyStreamList[n].width = 8192
ArvApyStreamList[n].height = 4096
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 1

n += 1
ArvApyStreamList[n].name = "Touvet"
ArvApyStreamList[n].filename_list = [    
    "/datasets/Touvet_64Frm_QP37_8bpp.yuv",
    "/datasets/Touvet_64Frm_QP22_8bpp.yuv",
]
ArvApyStreamList[n].resolution_list = [
    (3840,1920),
    (3840,1920)
]
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 2

n += 1
ArvApyStreamList[n].name = "Foreman"
ArvApyStreamList[n].filename = "/datasets/Foreman_CIF.yuv"
ArvApyStreamList[n].width = 352
ArvApyStreamList[n].height = 288
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 1

n += 1
ArvApyStreamList[n].name = "Foreman (Multi-layer)"
ArvApyStreamList[n].filename_list = [    
    "/datasets/Foreman_CIF.yuv",
    "/datasets/Foreman_CIF.yuv",
    "/datasets/Foreman_CIF.yuv",
]
ArvApyStreamList[n].resolution_list = [
    (352,288),
    (352,288),
    (352,288)
]
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 3



def GetListOfAvailableStreams():
    stream_list = []
    for s in ArvApyStreamList:
        stream = [ s.name, s.GetWidth(-1), s.GetHeight(-1), s.bytes_per_pixel, s.num_layers]
        stream_list.append( stream )
    return stream_list
