import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from quoteapp.models import Author, Quote, Tag


class Command(BaseCommand):
    help = "Import data from JSON files"

    def handle(self, *args, **options):
        self.stdout.write("Importing data from JSON files")

        with open("authors.json", "r") as authors_file:
            authors_data = json.load(authors_file)

            for author_data in authors_data:
                author = Author(
                    fullname=author_data["fullname"],
                    born_date=timezone.make_aware(
                        timezone.datetime.strptime(author_data["born_date"], "%B %d, %Y")
                    ) if author_data["born_date"] else None,
                    born_location=author_data["born_location"],
                    description=author_data["description"]
                )
                author.save()

        with open("quotes.json", "r") as quotes_file:
            quotes_data = json.load(quotes_file)

            # Імпортуємо дані про цитати
            for quote_data in quotes_data:
                author_name = quote_data["author"]
                author = Author.objects.get(fullname=author_name)

                tags = [Tag.objects.get_or_create(name=tag)[0] for tag in quote_data["tags"]]
                quote = Quote(
                    quote=quote_data["quote"],
                    author=author
                )
                quote.save()
                quote.tags.set(tags)

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
