Flask S3 Save Example
=====================

An example Flask app that uses `s3-saver <https://github.com/Jaza/s3-saver>`_, `url-for-s3 <https://github.com/Jaza/url-for-s3>`_, `flask-thumbnails-s3 <https://github.com/Jaza/flask-thumbnails-s3>`_, and `flask-admin-s3-upload <https://github.com/Jaza/flask-admin-s3-upload>`_ to store and retrieve files on Amazon S3.

This app lets you upload, re-upload, and delete a single image. By changing a few lines of config, the image will be stored either locally, or in a S3 bucket of your choice.


Usage
-----

1.  Make sure you have installed:

    - SQLite (3.8+ recommended)
    - Python 2.7+ (and virtualenv)
    - Pillow (Python image library)

2.  Clone the flask-s3-save-example repo:
    ::

        git clone git@github.com:Jaza/flask-s3-save-example.git
        cd flask-s3-save-example

3.  Set up a (Python 2.7) virtualenv (recommended to use with ``--system-site-packages`` option) and activate it, e.g:
    ::

        mkdir env; cd env
        virtualenv --system-site-packages .
        source bin/activate
        cd ..

4.  Install dependencies:
    ::

        pip install -r requirements.txt

5.  Create writable uploads / cache directory:
    ::

        mkdir static
        mkdir static/uploads
        chmod 777 static/uploads
        mkdir static/cache
        chmod 777 static/cache

6.  Sync the database (and create a DB and DB user if necessary):
    ::

        ./project/manage.py db upgrade

7.  Create a super user to log in to the app:
    ::

        ./project/manage.py createsuperuser

8.  Run the development server (defaults to port 5000):
    ::

        ./project/manage.py runserver -dr

9.  Access the web front-end:
    ::

        http://localhost:5000/

10. Access the admin by loging in:
    ::

        http://localhost:5000/login/?next=/admin/


Configuration
-------------

In ``project/settings.py``, change ``USE_S3`` to ``False`` to store the image locally. If using S3, you'll need to set ``S3_BUCKET_NAME``, ``AWS_ACCESS_KEY_ID``, and ``AWS_SECRET_ACCESS_KEY`` to point to a bucket that the given AWS credentials can read / write to.
