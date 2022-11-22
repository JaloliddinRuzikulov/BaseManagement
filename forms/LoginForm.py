
class LoginForm(forms.Form):
    username = forms.CharField(label='',
                                widget=forms.TextInput(
                                    attrs = {
                                       'placeholder': 'username or email',
                                       }
                               ))

    password = forms.CharField(label='', 
                                widget=forms.PasswordInput(
                                    attrs = {
                                        'placeholder': 'password'
                                    }
                                ))