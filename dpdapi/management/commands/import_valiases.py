from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import os

from dpdapi.models import Alias, Domain


class Command(BaseCommand):
    help = 'Import aliases for a single domain at a time, which is the domain of the first source address.'

    def handle(self, *args, **options):
        if len(args) == 1:
            if os.path.exists(args[0]):
                self.import_file(args[0])
            else:
                self.stdout.write("{} does not exist".format(args[0]))
        else:
            self.stdout.write("Missing argument")

    def import_file(self, filename):
        new_aliases = []
        counts = {'imported': 0, 'existing': 0}
        # Open file
        with open(filename) as f:
            # Parse
            for l in f:
                if l.startswith('*: '):
                    continue  # Skip catch all

                source, destinations = l.strip().split(': ')
                for destination in destinations.split(','):
                    if destination.startswith('"|') or '-admin@' in destination:
                        continue  # Skip mailman-aliases
                    new_aliases.append(Alias(source=source, destination=destination))

        if len(new_aliases) == 0:
            self.stdout.write('No aliases found')
            return

        # Lookup domain
        domain_name = new_aliases[0].source.split('@')[1]  # Assumes that every alias is in the same domain
        d, created = Domain.objects.get_or_create(name=domain_name)
        if created:
            self.stdout.write('Created domain {}.'.format(d.name))

        # Try to create, log if exists. Slow but works
        for a in new_aliases:
            a.domain = d
            try:
                a.save()
                counts['imported'] += 1  # Woop!
            except IntegrityError:
                counts['existing'] += 1  # Exists
                self.stdout.write('Could not import \'{}={}\', already exists.'.format(a.source, a.destination))

        # Print num imported, existing, total
        self.stdout.write('Imported {}, skipped {} existing, total {}'.format(
            counts['imported'],
            counts['existing'],
            len(new_aliases)))