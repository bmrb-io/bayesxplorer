#!/usr/bin/python

""" Power the Bayes Explorer server. """

from __future__ import print_function

import os
from uuid import uuid4

# Installed packages
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

# Set up the flask application
application = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
application.config['UPLOAD_FOLDER'] = os.path.join(dir_path, 'uploads')

application.config.update(
    MAIL_SERVER='cowfish',
    MAIL_DEFAULT_SENDER='noreply@nmrfam.wisc.edu'
)
mail = Mail(application)


@application.route('/')
def home_page():
    return render_template('submit.html')


@application.route('/upload', methods=['POST'])
def upload_file():
    # get posted parameters

    csvfile = request.files.get('csv_file')
    zipfile = request.files.get('zip_file')
    email = request.form.get('email')
    field_strength = request.form.get('field_strength', 'unknown')
    sample = request.form.get('sample', 'unknown')
    validate_only = request.form.get('validate_only', 'False')
    if validate_only == 'on':
        validate_only = 'False'

    if not email:
        return render_template('submission_status.html', message='Please provide your email.')
    if not csvfile:
        return render_template('submission_status.html', message='Please provide the CSV file.')

    uuid = str(uuid4())
    entry_dir = os.path.join(application.config['UPLOAD_FOLDER'], uuid)
    os.mkdir(entry_dir)

    if csvfile and (zipfile or validate_only) and email:
        csv_filename = secure_filename(csvfile.filename)
        csvfile.save(os.path.join(entry_dir, csv_filename))
        if zipfile:
            zip_filename = secure_filename(zipfile.filename)
            zipfile.save(os.path.join(entry_dir, zip_filename))
        else:
            zip_filename = 'None'

        submission_info = '''Submission ID: %s
Submission directory: %s
User e-mail: %s
Field strength: %s 
Sample: %s
Validate only: %s
CSV file name: %s
Zip file name: %s
''' % (uuid, entry_dir, email, field_strength, sample, validate_only, csv_filename, zip_filename)

        with open(os.path.join(entry_dir, 'status'), "w") as status_file:
            status_file.write(submission_info)

        confirm_message = Message("Submission made to Bayes Explorer.", recipients=['wedell@bmrb.wisc.edu'])
        confirm_message.body = submission_info
        mail.send(confirm_message)
        return render_template('submission_status.html', message='Submission complete!')

    return render_template('submission_status.html',
                           message='Something was invalid with your submission. Please retry.')


if __name__ == "__main__":
    pass
