from django import forms

class TwoTextFieldsForName(forms.MultiWidget):
    def __init__(self, attrs=None):
        self.widgets = [
            forms.TextInput(attrs={'placeholder': "First name"}),
            forms.TextInput(attrs={'placeholder': "Last name"})
        ]
        super().__init__(self.widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(' ')
        return [None, None]

class NameMultiField(forms.MultiValueField):
    widget = TwoTextFieldsForName()

    def __init__(self):
        label = "Name"
        fields = (
            forms.CharField(),
            forms.CharField()
        )
        super(NameMultiField, self).__init__(
            fields=fields,
            label=label
        )

    def compress(self, data_list):
        return ' '.join(data_list)

class ContactForm(forms.Form):
    sender_name = NameMultiField()
    sender_email = forms.EmailField(label="Email")
    subject = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)

    sender_name.group = 1
    sender_email.group = 1

    def group1(self):
        return filter(lambda x: x.group == 1, self.fields.values())
