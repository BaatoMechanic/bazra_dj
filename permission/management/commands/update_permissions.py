from django.core.management import BaseCommand
from permission.utils import update_permissions


class Command(BaseCommand):

    def handle(self, **options):
        update_permissions()
