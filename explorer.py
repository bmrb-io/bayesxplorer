#!/usr/bin/python

""" Power the gateway server. """

from __future__ import print_function

import os
from uuid import uuid4

# Installed packages
from flask import Flask, request, jsonify, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

# Set up the flask application
application = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
application.config['UPLOAD_FOLDER'] = os.path.join(dir_path, 'uploads')

application.config.update(
    MAIL_SERVER='cowfish',
    MAIL_DEFAULT_SENDER='noreply@bmrb.wisc.edu'
)
mail = Mail(application)


@application.route('/')
def home_page():
    return render_template('submit.html')


@application.route('/upload', methods=['POST'])
def upload_file():
    # get posted parameters

    csvfile = request.files['csv_file']
    zipfile = request.files['zip_file']
    email = request.form.get('email', None)
    uuid = str(uuid4())
    entry_dir = os.path.join(application.config['UPLOAD_FOLDER'], uuid)
    os.mkdir(entry_dir)
    print(csvfile, zipfile, email, request.form)
    if csvfile and zipfile and email:
        csv_filename = secure_filename(csvfile.filename)
        zip_filename = secure_filename(zipfile.filename)
        csvfile.save(os.path.join(entry_dir, csv_filename))
        csvfile.save(os.path.join(entry_dir, zip_filename))
        with open(os.path.join(entry_dir, 'email'), "w") as email_file:
            email_file.write(email)

        confirm_message = Message("Submission made to Bayes Explorer.", recipients=['wedell@bmrb.wisc.edu'])
        confirm_message.body = 'Submission ID: %s\nSubmission directory: %s\nUser e-mail: %s\nCSV file name:%s\n'\
                               'Zip file name: %s' % (uuid, entry_dir, email, csv_filename, zip_filename)
        mail.send(confirm_message)
        return render_template('submission_status.html', message='Submission complete!')

    return render_template('submission_status.html',
                           message='Something was invalid with your submission. Please retry.')


if __name__ == "__main__":
    pass
