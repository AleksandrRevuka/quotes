import connect_mongo

from django.core.management.base import BaseCommand
from django.utils import timezone

from models_mongo import AuthorM, QuoteM
from quoteapp.models import Author, Tag, Quote


class Command(BaseCommand):
    help = "Import data from MongoDB"

    def handle(self, *args, **options):
        self.stdout.write("Connected to MongoDB")
        authors_mongo = AuthorM.objects()
        quotes_mongo = QuoteM.objects()

        for author_mongo in authors_mongo:
            if author_mongo.fullname:
                author = Author(
                    fullname=author_mongo.fullname,
                    born_date=timezone.make_aware(author_mongo.born_date, timezone=timezone.get_current_timezone()),
                    born_location=author_mongo.born_location,
                    description=author_mongo.description,
                )
                author.save()

        for quote_mongo in quotes_mongo:
            if quote_mongo.author and quote_mongo.author.fullname:
                author = Author.objects.get(fullname=quote_mongo.author.fullname)

                tags = [Tag.objects.get_or_create(name=tag)[0] for tag in quote_mongo.tags]
                quote = Quote(
                    quote=quote_mongo.content,
                    author=author,
                )
                quote.save()
                quote.tags.set(tags)

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
