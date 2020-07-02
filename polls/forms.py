from django import forms
from .models import Choice


class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Tresc pytania", max_length=100)
    pub_date = forms.DateTimeField(label="Data publikacji")

# nie musimy pisac sami pol


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
