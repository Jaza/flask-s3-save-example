from __future__ import print_function

from flask import url_for
from url_for_s3 import url_for_s3

from project import db


class Thingy(db.Model):
    """Sample model for flask-s3-save-example."""

    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(255), default='')
    image_storage_type = db.Column(db.String(255), default='')
    image_storage_bucket_name = db.Column(db.String(255), default='')

    def __repr__(self):
        return 'A thingy'

    @property
    def image_url(self):
        from flask import current_app as app
        return self.image and '%s%s' % (app.config['UPLOADS_RELATIVE_PATH'], self.image) or None

    @property
    def image_url_storageaware(self):
        if not self.image:
            return None

        if not (self.image_storage_type and self.image_storage_bucket_name):
            return url_for('static', filename=self.image_url, _external=True)

        if self.image_storage_type != 's3':
            raise ValueError('Storage type "%s" is invalid, the only supported storage type (apart from default local storage) is s3.' % self.image_storage_type)

        return url_for_s3('static', bucket_name=self.image_storage_bucket_name, filename=self.image_url)
