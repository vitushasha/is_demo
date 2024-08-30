from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms.forms import AudioFileForm
from .utils import convert_audio, check_extention


@main_auth(on_cookies=True)
def start_convert(request):
    form = AudioFileForm()
    response = None
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        response = {'text': None, 'error': None}
        if form.is_valid():
            audio_info = form.save()
            filename = audio_info.audio_file.name
            if not check_extention(filename):
                response['error'] = 'Неверный формат файла'
                return render(request, 'convert_speech_to_text.html', {'form': form, 'response': response, })
            else:
                try:
                    response['text'] = convert_audio(filename, model=audio_info.choose_model)
                except Exception as e:
                    response['error'] = e
                    return render(request, 'convert_speech_to_text.html', {'form': form, 'response': response, })
            audio_info.text_of_file = response
            audio_info.save()

    return render(request, 'convert_speech_to_text.html', {'form': form, 'response': response, })