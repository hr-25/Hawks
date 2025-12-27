from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import date

from .models import MaintenanceRequest, Equipment
from django.contrib.auth.models import User

def dashboard(request):
    from django.utils.timezone import now

    # Critical equipment = expired warranty
    critical_equipment_count = Equipment.objects.filter(
        warranty_end__lt=now().date()
    ).count()

    # Technician load
    technician_count = User.objects.filter(
        groups__name='Technicians'
    ).count()

    assigned_requests = MaintenanceRequest.objects.filter(
       technician__isnull=False,
        status__in=['new', 'in_progress']
    ).count()

    technician_load = 0
    if technician_count > 0:
        technician_load = int((assigned_requests / technician_count) * 100)

    # Open requests
    pending_requests = MaintenanceRequest.objects.filter(
        status='new'
    ).count()

    overdue_requests = MaintenanceRequest.objects.filter(
        scheduled_date__lt=now().date(),
        status__in=['new', 'in_progress']
    ).count()

    requests = MaintenanceRequest.objects.all().order_by('-created_at')[:10]

    context = {
        'critical_equipment_count': critical_equipment_count,
        'technician_load': technician_load,
        'pending_requests': pending_requests,
        'overdue_requests': overdue_requests,
        'requests': requests,
    }

    return render(request, 'maintenance/dashboard.html', context)



def kanban_board(request):
    requests = MaintenanceRequest.objects.all()
    return render(request, 'maintenance/kanban.html', {'requests': requests})


def calendar_view(request):
    return render(request, 'maintenance/calendar.html')


def calendar_events(request):
    events = []

    requests = MaintenanceRequest.objects.filter(
        request_type='preventive',
        scheduled_date__isnull=False
    )

    for req in requests:
        events.append({
            'title': f"{req.subject} ({req.equipment.name})",
            'start': req.scheduled_date.isoformat(),
        })

    return JsonResponse(events, safe=False)
