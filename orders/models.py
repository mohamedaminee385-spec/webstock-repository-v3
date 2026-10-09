from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    CATEGORY_CHOICES = [
        ('SCANNER', 'Scanner'),
        ('PRINTER', 'Printer'),
        ('DESKTOP', 'Desktop'),
        ('LAPTOP', 'Laptop'),
        ('MONITOR', 'Monitor'),
    ]

    STATUS_PENDING = 'PENDING'
    STATUS_FINALIZED = 'FINALIZED'

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FINALIZED', 'Finalized'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Category-specific details (optional depending on selected category)
    screen_size = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Inches (Monitors/Laptops)")
    processor = models.CharField(max_length=100, null=True, blank=True, help_text="Desktops/Laptops")
    ram_gb = models.PositiveIntegerField(null=True, blank=True, help_text="Desktops/Laptops")
    print_speed_ppm = models.PositiveIntegerField(null=True, blank=True, help_text="Scanners/Printers")

    def __str__(self):
        return f"{self.category} - {self.title} ({self.status})"