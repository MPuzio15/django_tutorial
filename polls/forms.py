from django import forms


class QuestionForm(forms.Form):
    question_text = forms.CharField(label="Tresc pytania", max_length=100)
    pub_date = forms.DateTimeField(label="Data publikacji")
