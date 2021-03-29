from django.contrib.sites.models import Site


def run():
    Site.objects.get_or_create(name="example", domain="example.com")
    print("Site created.")
