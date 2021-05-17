from .arv360stream import Arv360Stream

NumberOfStreams = 6

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
ArvApyStreamList[n].name = "Touvet (2 Quality Layers)"
ArvApyStreamList[n].filename_list = [
    "/datasets/Touvet_64Frm_QP22_8bpp_UP.yuv",
    "/datasets/Touvet_64Frm_QP22_8bpp.yuv",
]
ArvApyStreamList[n].resolution_list = [
    (3840,1920),
    (3840,1920)
]
ArvApyStreamList[n].quality_list = [
    "Low",
    "High"
]
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 2


n += 1
ArvApyStreamList[n].name = "Touvet (3 Spatial Layers)"
ArvApyStreamList[n].filename_list = [
    "/datasets/Touvet_64Frm_QP22_8bpp_960.yuv",
    "/datasets/Touvet_64Frm_QP22_8bpp_1920.yuv",
    "/datasets/Touvet_64Frm_QP22_8bpp.yuv",
]
ArvApyStreamList[n].resolution_list = [
    (960,480),
    (1920,960),
    (3840,1920)
]
ArvApyStreamList[n].quality_list = [
    "Low",
    "Medium",
    "High"
]
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 3


n += 1
ArvApyStreamList[n].name = "Plan Energy Bio Lab  (Single layer)"
ArvApyStreamList[n].filename_list = [
    "/datasets/Finish_res_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PlanEnergyBioLab_64Frm_ExtConv_Ref_qp_27/stream_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PlanEnergyBioLab_64Frm_ExtConv_Ref_qp_27.yuv",
]
ArvApyStreamList[n].resolution_list = [
    (3840,1920)
]
ArvApyStreamList[n].quality_list = [
    "High"
]
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 1
ArvApyStreamList[n].summary_info_file = "/datasets/Finish_res_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PlanEnergyBioLab_64Frm_ExtConv_Ref_qp_27/summary_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PlanEnergyBioLab_64Frm_ExtConv_Ref_qp_27"


n += 1
ArvApyStreamList[n].name = "Porto River Side  (Single layer)"
ArvApyStreamList[n].filename_list = [
    "/datasets/Finish_res_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PortoRiverside_64Frm_ExtConv_Ref_qp_27/stream_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PortoRiverside_64Frm_ExtConv_Ref_qp_27.yuv",
]
ArvApyStreamList[n].resolution_list = [
    (3840,1920)
]
ArvApyStreamList[n].quality_list = [
    "High"
]
ArvApyStreamList[n].projection = 0
ArvApyStreamList[n].bytes_per_pixel = 1
ArvApyStreamList[n].num_layers = 1
ArvApyStreamList[n].summary_info_file = "/datasets/Finish_res_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PortoRiverside_64Frm_ExtConv_Ref_qp_27/summary_EncoderSVVC360_VTM-91-360Lib-101_ScalableRandomAccessAuto_360_ERP_4K_PortoRiverside_64Frm_ExtConv_Ref_qp_27"

def GetListOfAvailableStreams():
    stream_list = []
    for s in ArvApyStreamList:
        stream = [ s.name, s.GetWidth(-1), s.GetHeight(-1), s.bytes_per_pixel, s.num_layers]
        stream_list.append( stream )
    return stream_list
