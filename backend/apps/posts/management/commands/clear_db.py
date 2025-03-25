from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Check the database backend (SQLite or PostgreSQL)
        with connection.cursor() as cursor:
            db_backend = connection.vendor  # Get the database vendor (PostgreSQL or SQLite)

            if db_backend == 'sqlite':
                self.stdout.write(self.style.WARNING(f"Dropping all tables for SQLite"))

                try:
                    # Disable foreign key checks for SQLite
                    cursor.execute("PRAGMA foreign_keys = OFF;")

                    # SQLite specific: Get all table names and drop them
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()

                    for table in tables:
                        table_name = table[0]
                        try:
                            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}";')
                            self.stdout.write(self.style.WARNING(f'Dropped table {table_name}'))
                        except OperationalError as e:
                            self.stdout.write(self.style.ERROR(f"Error dropping table {table_name}: {e}"))

                    # Re-enable foreign key checks for SQLite
                    cursor.execute("PRAGMA foreign_keys = ON;")

                except OperationalError as e:
                    self.stdout.write(self.style.ERROR(f"Error fetching tables: {e}"))

            elif db_backend == 'postgresql':
                self.stdout.write(self.style.WARNING(f"Dropping all tables for PostgreSQL"))

                try:
                    # PostgreSQL specific: Get all table names and drop them
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                    tables = cursor.fetchall()

                    for table in tables:
                        table_name = table[0]
                        try:
                            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
                            self.stdout.write(self.style.WARNING(f'Dropped table {table_name}'))
                        except OperationalError as e:
                            self.stdout.write(self.style.ERROR(f"Error dropping table {table_name}: {e}"))

                except OperationalError as e:
                    self.stdout.write(self.style.ERROR(f"Error fetching tables: {e}"))

            self.stdout.write(self.style.SUCCESS('Successfully dropped all tables'))
