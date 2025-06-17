from django.db import models
from django.utils import timezone
import uuid

class VotingCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    telegram_user_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  # ✅ This handles Telegram voters
    
    def mark_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save()

    def __str__(self):
        return self.code
    
    def __str__(self):
        return self.code

    @classmethod
    def create_codes(cls, quantity=100):
        created = 0
        codes = []
        while created < quantity:
            new_code = uuid.uuid4().hex[:8].upper()
            if not cls.objects.filter(code=new_code).exists():
                codes.append(cls(code=new_code))
                created += 1
        cls.objects.bulk_create(codes)
        return codes

class IPVote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address
