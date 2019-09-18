def get_model():
    from .models import BlogComment
    return BlogComment


def get_form():
    from .forms import BlogCommentForm
    return BlogCommentForm
