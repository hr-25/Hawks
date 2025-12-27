from django.db import models
from django.contrib.auth.models import User


# 1️⃣ Maintenance Team (DEFINE FIRST)
class MaintenanceTeam(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


# 2️⃣ Equipment (USES MaintenanceTeam)
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    purchase_date = models.DateField()
    warranty_end = models.DateField()
    location = models.CharField(max_length=100)

    department = models.CharField(max_length=100)
    assigned_employee = models.CharField(max_length=100)

    maintenance_team = models.ForeignKey(
        MaintenanceTeam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# 3️⃣ Maintenance Request
class MaintenanceRequest(models.Model):

    REQUEST_FOR_CHOICES = [
        ('equipment', 'Equipment'),
        ('workcenter', 'Work Center'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrap', 'Scrap'),
    ]

    MAINTENANCE_TYPE = [
        ('corrective', 'Corrective'),
        ('preventive', 'Preventive'),
    ]

    subject = models.CharField(max_length=200)

    request_for = models.CharField(
        max_length=20,
        choices=REQUEST_FOR_CHOICES,
        default='equipment'
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    work_center = models.ForeignKey(
        WorkCenter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    team = models.ForeignKey(
        MaintenanceTeam,
        on_delete=models.SET_NULL,
        null=True
    )

    technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    maintenance_type = models.CharField(
        max_length=20,
        choices=MAINTENANCE_TYPE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    scheduled_date = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    notes = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

       class WorkCenter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


