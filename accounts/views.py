from django.views.generic.edit import CreateView
from .forms import CustomSignupForm
from blog.models import Author


class SignUp(CreateView):
    model = Author
    form_class = CustomSignupForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'
