"""
    Django command to pause execution until database is available
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg import OperationalError as PsycopgOperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (PsycopgOperationalError, OperationalError):
                self.stdout.write("Database unavailable, waiting for 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
