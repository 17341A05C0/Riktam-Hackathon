from django import forms

class IssueForm(forms.Form):
	# name = forms.CharField()
	image_field = forms.ImageField()