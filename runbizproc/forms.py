from django import forms
from .models.models import BizProcModel


class BPForm(forms.ModelForm):
    class Meta:
        model = BizProcModel
        fields = []


    bp = forms.ModelChoiceField(
        queryset=BizProcModel.objects.all(),
        to_field_name='process_id',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='БП',
    )