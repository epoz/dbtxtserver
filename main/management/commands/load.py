from django.core.management.base import BaseCommand
import os
import logging
from optparse import make_option
from main import models
from django.contrib.auth.models import User
import textbase
import uuid
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    
class Command(BaseCommand):
    help = "Load the file specified on the command line into the database"

    option_list = BaseCommand.option_list + (
        make_option('--collection',
            action='store',
            dest='collection',
            help='Specify the Collection pk to use'),
        make_option('--user',
            action='store',
            dest='user',
            help='Specify the User pk to use'),
        )
    
    def handle(self, *args, **options):
        collection = models.Collection.objects.get(pk=options['collection'])
        user = User.objects.get(pk=options['user'])

        for f in args:
            if not os.path.exists(f):
                logging.exception('File %s does not exist', f)
                continue
            
            dbtxtfile = textbase.TextBase(f)
            models.Record.objects.bulk_create([models.Record(collection=collection, uid=uuid.uuid4().hex,
                              user=user, data=textbase.dumpdict(d)) for d in dbtxtfile])
