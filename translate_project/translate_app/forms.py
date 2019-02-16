from django import forms
from django.contrib.auth.models import User
from translate_app.models import Article

class UserForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'class': 'w3-input w3-border w3-round-large'})

	password = forms.CharField(
    	widget=forms.PasswordInput()
    	)
	password.widget.attrs.update({'class': 'w3-input w3-border w3-round-large'})

	username = forms.CharField(
		widget=forms.TextInput(
			attrs = {'class': 'w3-input w3-border w3-round-large'}
			)
		)

	class Meta:
		model=User
		fields = ('username', 'email', 'password')

class ArticleForm(forms.ModelForm):
	subtitle = forms.CharField(required=False)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model=Article
		exclude =('readers', 'slug')
