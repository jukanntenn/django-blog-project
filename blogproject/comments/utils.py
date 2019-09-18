from django.utils.crypto import salted_hmac


def generate_security_hash(content_type, object_pk, timestamp):
    info = (content_type, object_pk, timestamp)
    key_salt = "django.contrib.forms.CommentSecurityForm"
    value = "-".join(info)
    return salted_hmac(key_salt, value).hexdigest()
