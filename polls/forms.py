from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class AddQuestionForm(forms.Form):
    question_text = forms.CharField(max_length=200)
    choice_1 = forms.CharField(max_length=200)
    choice_2 = forms.CharField(max_length=200)
    choice_3 = forms.CharField(max_length=200)
    choice_4 = forms.CharField(max_length=200)
    choice_5 = forms.CharField(max_length=200)