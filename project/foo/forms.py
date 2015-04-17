import wtforms.validators
from flask_wtf_alchemy_utils import ModelForm
from flask_wtf.file import FileField, FileAllowed

from foo.models import Thingy
from foo.uploads import thingy_image


class ThingySaveForm(ModelForm):
    class Meta:
        model = Thingy
        only = ('image',)

    image = FileField(validators=[FileAllowed(thingy_image, 'Only image files (gif, jpg, png) can be uploaded for this field')])
    image_delete = wtforms.BooleanField(label='Delete this image')
