from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Create a superuser, including the name field'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--name',
            dest='name',
            default=None,
            help='Specifies the full name for the superuser',
        )

    def handle(self, *args, **options):
        name = options.get('name')

        # If no name provided, prompt interactively
        if not name:
            name = input("Name: ").strip()
            if not name:
                raise CommandError("You must provide a name.")

        options['name'] = name

        super().handle(*args, **options)