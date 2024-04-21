from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

def redirect_blog(request: HttpRequest) -> HttpResponse:
    return redirect('posts_list_url', permanent=True)
