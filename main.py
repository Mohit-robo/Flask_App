from flask import Flask,render_template,Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture('./video/cars.mp4')

def generate_frame():
    while True: 
        succes,frame = camera.read()
        frame = cv2.resize(frame,(1280,720))
        if not succes:
            break 
        else:
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
