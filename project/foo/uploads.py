from flask.ext.uploads import UploadSet, IMAGES


upload_sets = []


thingy_image = UploadSet(
    'fooimage',
    IMAGES,
    default_dest=lambda app: '%s%s' % (
        app.config['UPLOADS_FOLDER'],
        app.config['THINGY_IMAGE_RELATIVE_PATH']))

upload_sets.append(thingy_image)
