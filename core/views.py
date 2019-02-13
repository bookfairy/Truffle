from django.shortcuts import render


def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'core/feed.html')
    else:
        return render(request, 'core/index.html')
