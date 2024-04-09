import connect_mongo
from django.core.management.base import BaseCommand
from django.utils import timezone
from models_mongo import AuthorM, QuoteM
from quoteapp.models import Author, Quote, Tag


class Command(BaseCommand):
    help = "Import data from MongoDB"

    def handle(self, *args, **options):
        """
        The handle function is the main function of a command. It takes two arguments:
            args - A list of positional arguments passed to the command.
            options - A dictionary of named options passed to the command.
        
        :param self: Access the class attributes and methods
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **options: Pass in options to the command
        :return: None
        :doc-author: Trelent
        """
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
