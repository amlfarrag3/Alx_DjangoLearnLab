from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

class NotificationView(APIView):
    """
    View to handle notifications.
    Currently, this is a placeholder and does not implement any functionality.
    """
    def get(self, request):
        return render(request, 'notifications/notifications.html', {})
