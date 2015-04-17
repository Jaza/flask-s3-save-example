from datetime import datetime
from os import path
from werkzeug import secure_filename


def prefix_file_utcnow(model, file_data):
    parts = path.splitext(file_data.filename)
    return secure_filename('%s%s' % (datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S'), parts[1]))
