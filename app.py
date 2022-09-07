from flask import Flask,Response,render_template
import cv2

app=Flask(__name__)
camera=cv2.VideoCapture(0) #videocapture object to trigger the camera!and  read the first image/frame of the video.We can either provide the path of the video file or use numbers to specify the use of local webcam. To trigger the webcam we pass ‘0’ as the argument.

@app.route("/")
def welcome():
    return render_template('index.html')
 
#adding window and generating frame for the camera
def genrate_frame():
    while True:
        sucess,frame=camera.read()  
        # sucess takes the boolean ,returns true when python -vediocapture() is able to read.#frame  - a numpy array represents the first image that vedio captures
        if sucess != True:
            break
        else:
            ret,buffer = cv2.imencode('.jpg',frame) #1st parameter which format have to change,
            frame=buffer.tobytes()
            #yield keyword lets execution to continue and keeps on generating frame until alive.
            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')# concat frame one by one and show result


@app.route("/vedio")
def vedio():
    return Response(genrate_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

        

if __name__=='__main__':
    app.run(debug=True)