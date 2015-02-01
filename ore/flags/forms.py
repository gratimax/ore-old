from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from ore.flags.models import Flag



class FlagForm(forms.ModelForm):
    REASON_CHOICES = (
        ('inappropriate', 'Inappropriate'),
        ('spam', 'Spam')
    )
    flag_type = forms.ChoiceField(choices=REASON_CHOICES, label='Reason')
    extra_comments = forms.CharField(label='Comments', widget=forms.Textarea(attrs={'rows': '6', 'placeholder': 'Anything typed here is visible to the author of the content that you are flagging.'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(FlagForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Flag Content'))

    class Meta:
        model = Flag
        fields = ['flag_type', 'extra_comments']
