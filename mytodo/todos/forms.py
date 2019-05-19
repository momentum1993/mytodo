from django import forms

class TodoForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.Textarea)
    priority = forms.IntegerField()
    due_date = forms.DateTimeField(input_formats = ["%Y-%m-%dT%H:%M"],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'))
    sub_todos = forms.CharField(widget=forms.Textarea)

