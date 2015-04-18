from io import BytesIO
from os import path

from flask import current_app as app
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from s3_saver import S3Saver

from project import db
from library.prefix_file_utcnow import prefix_file_utcnow
from foo.forms import ThingySaveForm
from foo.models import Thingy


mod = Blueprint('foo', __name__)


@mod.route('/', methods=['GET', 'POST'])
def home():
    """Displays the Flask S3 Save Example home page."""

    model = Thingy.query.first() or Thingy()

    form = ThingySaveForm(obj=model)

    if form.validate_on_submit():
        image_orig = model.image
        image_storage_type_orig = model.image_storage_type
        image_bucket_name_orig = model.image_storage_bucket_name

        # Initialise s3-saver.
        image_saver = S3Saver(
            storage_type=app.config['USE_S3'] and 's3' or None,
            bucket_name=app.config['S3_BUCKET_NAME'],
            access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            access_key_secret=app.config['AWS_SECRET_ACCESS_KEY'],
            field_name='image',
            storage_type_field='image_storage_type',
            bucket_name_field='image_storage_bucket_name',
            base_path=app.config['UPLOADS_FOLDER'],
            static_root_parent=path.abspath(
                path.join(app.config['PROJECT_ROOT'], '..')))

        form.populate_obj(model)

        if form.image.data:
            filename = prefix_file_utcnow(model, form.image.data)

            filepath = path.abspath(
                path.join(
                    path.join(
                        app.config['UPLOADS_FOLDER'],
                        app.config['THINGY_IMAGE_RELATIVE_PATH']),
                    filename))

            # Best to pass in a BytesIO to S3Saver, containing the
            # contents of the file to save. A file from any source
            # (e.g. in a Flask form submission, a
            # werkzeug.datastructures.FileStorage object; or if
            # reading in a local file in a shell script, perhaps a
            # Python file object) can be easily converted to BytesIO.
            # This way, S3Saver isn't coupled to a Werkzeug POST
            # request or to anything else. It just wants the file.
            temp_file = BytesIO()
            form.image.data.save(temp_file)

            # Save the file. Depending on how S3Saver was initialised,
            # could get saved to local filesystem or to S3.
            image_saver.save(
                temp_file,
                app.config['THINGY_IMAGE_RELATIVE_PATH'] + filename,
                model)

            # If updating an existing image,
            # delete old original and thumbnails.
            if image_orig:
                if image_orig != model.image:
                    filepath = path.join(
                        app.config['UPLOADS_FOLDER'],
                        image_orig)

                    image_saver.delete(filepath,
                        storage_type=image_storage_type_orig,
                        bucket_name=image_bucket_name_orig)

                glob_filepath_split = path.splitext(path.join(
                    app.config['MEDIA_THUMBNAIL_FOLDER'],
                    image_orig))
                glob_filepath = glob_filepath_split[0]
                glob_matches = image_saver.find_by_path(
                    glob_filepath,
                    storage_type=image_storage_type_orig,
                    bucket_name=image_bucket_name_orig)

                for filepath in glob_matches:
                    image_saver.delete(
                        filepath,
                        storage_type=image_storage_type_orig,
                        bucket_name=image_bucket_name_orig)
        else:
            model.image = image_orig

        # Handle image deletion
        if form.image_delete.data and image_orig:
            filepath = path.join(
                app.config['UPLOADS_FOLDER'], image_orig)

            # Delete the file. In this case, we have to pass in
            # arguments specifying whether to delete locally or on
            # S3, as this should depend on where the file was
            # originally saved, rather than on how S3Saver was
            # initialised.
            image_saver.delete(filepath,
                storage_type=image_storage_type_orig,
                bucket_name=image_bucket_name_orig)

            # Also delete thumbnails
            glob_filepath_split = path.splitext(path.join(
                app.config['MEDIA_THUMBNAIL_FOLDER'],
                image_orig))
            glob_filepath = glob_filepath_split[0]

            # S3Saver can search for files too. When searching locally,
            # it uses glob(); when searching on S3, it uses key
            # prefixes.
            glob_matches = image_saver.find_by_path(
                glob_filepath,
                storage_type=image_storage_type_orig,
                bucket_name=image_bucket_name_orig)

            for filepath in glob_matches:
                image_saver.delete(filepath,
                                   storage_type=image_storage_type_orig,
                                   bucket_name=image_bucket_name_orig)

            model.image = ''
            model.image_storage_type = ''
            model.image_storage_bucket_name = ''

        if form.image.data or form.image_delete.data:
            db.session.add(model)
            db.session.commit()
            flash('Thingy %s' % (
                      form.image_delete.data and 'deleted' or 'saved'),
                  'success')
        else:
            flash(
                'Please upload a new thingy or delete the ' +
                    'existing thingy',
                'warning')

        return redirect(url_for('foo.home'))

    return render_template('home.html',
                           form=form,
                           model=model)
