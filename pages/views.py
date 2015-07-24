from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    """
    Returns index page.
    """

    response = {}
    if request.user.is_authenticated():
        response.update({
            'user': request.user
        })

    return render(request, 'pages/index.html', response)


def signin(request):
    """
    Returns signin page.
    GET loads the signin form.
    POST logins the user.
    """

    response = {}
    response.update(csrf(request))

    if request.method == 'GET':
        return render(request, 'pages/signin.html', {})

    if request.method == 'POST':

        # Validate containing error messages.
        errors = []

        # validate the form
        if 'username' in request.POST and request.POST['username']:
            username = request.POST['username']
        else:
            errors.append('Username is required')

        if 'password' in request.POST and request.POST['password']:
            password = request.POST['password']
        else:
            errors.append('Password is required')

        # If there are errors, update the response and send it back
        if errors:
            response.update({
                'errors': errors
            })
            return render(request, 'pages/signin.html', response)

        # Try logging in the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # The user is logged in. Redirect her to dashboard.
            return redirect('/')
        else:
            # Invalid username/password
            # Return an 'invalid login' error message.
            errors.append('You have entered an invalid username/password')
            response.update({
                'errors': errors
            })
            return render(request, 'pages/signin.html', response)


def signup(request):
    """
    Returns signup page.
    GET loads the signup form.
    POST creates the user.
    """

    response = {}
    response.update(csrf(request))

    if request.method == 'GET':
        return render(request, 'pages/signup.html', response)

    if request.method == 'POST':

        # Variable containing error messages.
        errors = []

        # Validate the form
        if 'username' in request.POST and request.POST['username']:
            username = request.POST['username']
        else:
            errors.append('Username is required')

        if 'email' in request.POST and request.POST['email']:
            email = request.POST['email']
        else:
            errors.append('Email is required')

        if 'password' in request.POST and request.POST['password']:
            password = request.POST['password']
        else:
            errors.append('Password is required')

        if 'repeat-password' in request.POST and\
                request.POST['repeat-password']:
            repeat_password = request.POST['repeat-password']
        else:
            errors.append('Repeat password is required')

        # If there are errors, update the response and send it back
        if errors:
            response.update({
                'errors': errors
            })
            return render(request, 'pages/signup.html', response)

        # Check whether the two passwords match or not.
        if password != repeat_password:
            errors.append('Passwords do not match')
            response.update({
                'errors': errors
            })
            return render(request, 'pages/signup.html', response)

        # Check whether the username exists or not.
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            # String formatting
            errors.append('Username %s already exists' % (username,))
            response.update({
                'errors': errors
            })
            return render(request, 'pages/signup.html', response)

        # There are no more errors now. So create the user.
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        response.update({
            'success': True
        })
        return render(request, 'pages/signup.html', response)
