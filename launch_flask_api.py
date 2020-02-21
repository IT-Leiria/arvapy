from flask import Flask, escape, request
from arvapy import ArvApyData

app = Flask(__name__)

arvapy = ArvApyData()


@app.route('/get_frame')
def GetFrame():
    projection = request.args.get("projection", -1)
    frame = arvapy.Get360DegreeFrame(projection)
    return frame


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
