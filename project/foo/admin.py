from os import path

from flask_admin_s3_upload import S3ImageUploadField

from project import admin, app, db
from foo.models import Thingy
from library.admin_utils import ProtectedModelView
from library.prefix_file_utcnow import prefix_file_utcnow


class ThingyView(ProtectedModelView):
    column_list = ('image',)
    form_excluded_columns = ('image_storage_type',
                             'image_storage_bucket_name')

    form_overrides = dict(
        image=S3ImageUploadField)

    form_args = dict(
        image=dict(
            base_path=app.config['UPLOADS_FOLDER'],
            relative_path=app.config['THINGY_IMAGE_RELATIVE_PATH'],
            url_relative_path=app.config['UPLOADS_RELATIVE_PATH'],
            namegen=prefix_file_utcnow,
            storage_type_field='image_storage_type',
            bucket_name_field='image_storage_bucket_name',
        ))

    def scaffold_form(self):
        form_class = super(ThingyView, self).scaffold_form()
        static_root_parent = path.abspath(
            path.join(app.config['PROJECT_ROOT'], '..'))

        if app.config['USE_S3']:
            form_class.image.kwargs['storage_type'] = 's3'

        form_class.image.kwargs['bucket_name'] = \
            app.config['S3_BUCKET_NAME']
        form_class.image.kwargs['access_key_id'] = \
            app.config['AWS_ACCESS_KEY_ID']
        form_class.image.kwargs['access_key_secret'] = \
            app.config['AWS_SECRET_ACCESS_KEY']
        form_class.image.kwargs['static_root_parent'] = \
            static_root_parent

        return form_class


admin.add_view(ThingyView(Thingy, db.session, name='Thingies'))
