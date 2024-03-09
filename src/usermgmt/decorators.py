from functools import wraps
from django.shortcuts import get_object_or_404
from .models import Student

# Check if student or staff has access to a page
def user_has_access(view):
    @wraps(view)

    def wrapper(request, *args, **kwargs):
        kwargs["username"] = username = request.user.username
        kwargs["student"] = student = get_object_or_404(Student, user__username=username)
        return view(request, *args, **kwargs)
        
    return wrapper