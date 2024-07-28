from flask import Flask, render_template, Response, request, flash
from face_recog import generate_frames, encode_image
import os
from db import insert_face


app = Flask(__name__)

app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = './uploaded_images/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    
    return render_template("index.html")


def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed_route():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/add_student", methods=['POST', 'GET'])
def add_student():
    
    if request.method == "POST":
        
        name = request.form['s_name']
        index_num = request.form['s_index']
        course = request.form['s_course']
        s_pic = request.files['s_pic']
        
        
        if not (name or index_num or course or s_pic):
            flash('Missing Required Fields', 'danger')
        
        # print("Uploaded Pic", s_pic.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], s_pic.filename)
        # print(image_path)
        s_pic.save(image_path)
        
        img_encoding = encode_image(image_path)
        
        print("Encoded Image", img_encoding)
        save = insert_face(name, index_num, course, img_encoding)

        if save:
            flash('Student added successfully', 'success')
        else:
            flash('Error adding student', 'danger')
            

    return render_template("add_student.html")


if __name__ == '__main__':
    # create_table()
    app.run(debug=True)