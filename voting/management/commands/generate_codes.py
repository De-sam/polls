from django.core.management.base import BaseCommand
from voting.models import VotingCode

class Command(BaseCommand):
    help = 'Generate unique voting codes'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, help='How many codes to generate')

    def handle(self, *args, **kwargs):
        qty = kwargs['quantity']
        VotingCode.create_codes(qty)
        self.stdout.write(self.style.SUCCESS(f"✅ {qty} codes generated successfully."))
