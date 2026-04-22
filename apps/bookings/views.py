from rest_framework import generics, status
from rest_framework.response import Response
from apps.users.views import IsAdmin
from .models import Booking
from .serializers import BookingSerializer

class AdminBookingListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all().order_by('-created_at')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class AdminBookingOverrideView(generics.GenericAPIView):
    permission_classes = (IsAdmin,)

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            new_status = request.data.get('status')
            
            if new_status not in dict(Booking.STATUS_CHOICES).keys():
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
                
            booking.status = new_status
            booking.save()
            return Response({'message': f'Booking status updated to {new_status}'})
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
