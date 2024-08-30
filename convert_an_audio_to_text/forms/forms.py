from django import forms
from ..models.models import AudioToTextModel

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioToTextModel
        fields = ['audio_file', 'description', 'choose_model']