
from .models import Post, DR


def draft(request):
    context = {
        "draft_post":Post.objects.filter(status=DR).count()
    }
    return context