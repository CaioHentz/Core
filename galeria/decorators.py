from django.shortcuts import redirect
from django.contrib import messages

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if 'account_id' not in request.session:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('authenticate_account_view')
        return view_func(request, *args, **kwargs)
    return wrapper