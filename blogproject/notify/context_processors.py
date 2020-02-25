def notification_count(request):
    user = request.user

    if user.is_anonymous:
        unread_count = None
    else:
        unread_count = user.notifications.unread().count()

    return {"unread_count": unread_count}
