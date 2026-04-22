from django.db import models
from django.conf import settings


class MechanicProfile(models.Model):
    """Extended profile for mechanics with verification and performance data."""

    VERIFICATION_STATUS = (
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mechanic_profile',
        limit_choices_to={'role': 'mechanic'},
    )

    # Verification
    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_STATUS, default='PENDING'
    )
    license_doc = models.FileField(upload_to='mechanic_docs/licenses/', blank=True, null=True)
    id_doc = models.FileField(upload_to='mechanic_docs/ids/', blank=True, null=True)
    internal_notes = models.TextField(
        blank=True, default='',
        help_text='Admin-only notes (e.g., suspicious docs, follow-up needed)',
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='verified_mechanics',
    )

    # Location & Service
    address = models.TextField(blank=True, default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, default='', help_text="Short location name or city")
    service_radius_km = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)

    # Performance Metrics (updated periodically)
    total_jobs = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    reliability_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    rejection_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"MechanicProfile: {self.user.name} ({self.verification_status})"
