from django.shortcuts import render

def forbidden_view(request, exception=None):
    return render(request, "errors/403.html", status=403)