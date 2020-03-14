FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

ADD vtm_360lib /src/vtm
ADD test_material/Turtle_3840x1920_30.yuv /datasets/Turtle_3840x1920_30.yuv

RUN apt-get update && \
    apt-get install -y build-essential cmake python3-pip python3-flask python3-sphinx && \
    apt-get clean 
    
RUN cd /src/vtm/build && cmake .. && make -j4

EXPOSE 5000

CMD ["python3", "/src/arvapy/launch_flask_api.py"]
