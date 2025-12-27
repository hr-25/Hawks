from django.urls import path
from .views import kanban_board, calendar_view, calendar_events
from .views import dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('kanban/', kanban_board, name='kanban'),
    path('calendar/', calendar_view, name='calendar'),
    path('calendar/events/', calendar_events, name='calendar_events'),
]
