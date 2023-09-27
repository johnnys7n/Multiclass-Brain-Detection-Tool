from app import app
from app.contours import GettingContours
from app.histogram import GetHist
from flask import request, render_template, session, make_response
import os
import imutils
from skimage.metrics import structural_similarity
import cv2 as cv
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import base64
from io import BytesIO
import tempfile

# Adding path to config
app.config['UPLOADED'] = 'app/static/uploads'
app.config['GENERATED'] = 'app/static/generated'
app.config['GRAPHS'] = 'app/static/graphs'

# Route to home page


@app.route("/")
def home():
    return render_template('home.html')

# Route to contours page


@app.route("/contours", methods=["GET", "POST"])
def contours():
    if request.method == "POST":  # execute if req is post
        # Get uploaded image
        file_upload1 = request.files['file_upload1']
        filename1 = file_upload1.filename

        file_upload2 = request.files['file_upload2']
        filename2 = file_upload1.filename

        if file_upload2 and file_upload1:
            # Resize and save the uploaded image
            uploaded_image1 = Image.open(file_upload1).resize((250, 160))
            uploaded_image1.save(os.path.join(
                app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = Image.open(file_upload2).resize((250, 160))
            uploaded_image2.save(os.path.join(
                app.config['UPLOADED'], 'image2.png'))

            # Read uploaded and original image as array
            uploaded_image1 = cv.imread(os.path.join(
                app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = cv.imread(os.path.join(
                app.config['UPLOADED'], 'image2.png'))

            # Convert image into grayscale
            image1_gray = cv.cvtColor(uploaded_image1, cv.COLOR_BGR2GRAY)
            image2_gray = cv.cvtColor(uploaded_image2, cv.COLOR_BGR2GRAY)

            # Calculate structural similarity
            (score, diff) = structural_similarity(
                image1_gray, image2_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Calculate threshold and contours
            thresh = cv.threshold(
                diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
            cnts = cv.findContours(
                thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Draw contours on image
            for c in cnts:
                (x, y, w, h) = cv.boundingRect(c)
                cv.rectangle(uploaded_image1, (x, y),
                             (x + w, y + h), (0, 0, 255), 2)
                cv.rectangle(uploaded_image2, (x, y),
                             (x + w, y + h), (0, 0, 255), 2)

            # Save all output images (if requestuired)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_1.png'), uploaded_image1)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_2.png'), uploaded_image2)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_diff.png'), diff)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_thresh.png'), thresh)
            return render_template('contours.html', pred='Structural Similarity: ' + str(round(score*100, 2)) + '%')

        else:
            return render_template('contours.html', pred=str('Please Input Both Images'))
    else:
        return render_template('contours.html')


@app.route('/contours_show_image')
def displayImage():
    # Getting uploaded file path from session
    diff = os.path.join(app.config['GENERATED'], 'image_diff.png')
    return render_template('contours_show_image.html')

# Routes to the histogram page


@app.route('/histogram', methods=['GET', 'POST'])
def hist():
    if request.method == 'POST':  # executes when the req is post
        output = 0

        file_upload = request.files['file_upload']
        filename = file_upload.filename

        # if the image is imported
        if file_upload:
            # uploading and saving file:
            uploaded_file = Image.open(file_upload)
            uploaded_file.save(os.path.join(app.config['UPLOADED'], 'plt.png'))

            # change to numpy array
            img1 = cv.imread(os.path.join(app.config['UPLOADED'], 'plt.png'))

            # reading into cv and converting to hist plt
            hist = cv.calcHist([img1], [0], None, [256], [0, 256])

            # creating a graph of the histogram output
            fig = Figure()
            canvas = FigureCanvas(fig)
            axes = fig.add_subplot()
            axes.set_title(f'Histogram for Pixel Intensity: {filename}')
            axes.set_ylabel('No of Pixels')
            axes.set_xlabel('Pixel Values')

            # plot the data
            axes.plot(hist)

            # saving plotted image into a new folder as png then decoding
            buf = BytesIO()
            fig.savefig(buf, format='png')
            data = base64.b64encode(buf.getbuffer())
            img_plt = Image.open(BytesIO(base64.b64decode(data)))
            img_plt.save(os.path.join(app.config['GRAPHS'], 'plt_pic.png'))
            return render_template('histogram.html', output=1)
        else:  # if the image is not imported and the check button is clicked
            return render_template('histogram.html', output=str('Please Input an Image'))
    else:
        return render_template('histogram.html')

    # Main function
if __name__ == '__main__':
    app.run(debug=True)
