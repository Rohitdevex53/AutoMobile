from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.views import IsAdmin
from .models import MechanicProfile
from .serializers import MechanicProfileSerializer

class AdminMechanicVerificationListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = MechanicProfileSerializer

    def get_queryset(self):
        queryset = MechanicProfile.objects.all().order_by('-created_at')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(verification_status=status)
        return queryset

class AdminMechanicVerifyActionView(generics.GenericAPIView):
    permission_classes = (IsAdmin,)

    def post(self, request, pk):
        try:
            profile = MechanicProfile.objects.get(pk=pk)
            action_type = request.data.get('action') # 'APPROVE' or 'REJECT'
            notes = request.data.get('notes', '')

            if action_type == 'APPROVE':
                profile.verification_status = 'VERIFIED'
            elif action_type == 'REJECT':
                profile.verification_status = 'REJECTED'
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

            profile.internal_notes = notes
            profile.verified_by = request.user
            from django.utils import timezone
            profile.verified_at = timezone.now()
            profile.save()

            return Response({'message': f'Mechanic {action_type.lower()}ed successfully'})
        except MechanicProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminMechanicDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = MechanicProfileSerializer
    queryset = MechanicProfile.objects.all()

class MechanicOnboardingView(generics.RetrieveUpdateAPIView):
    """
    View for mechanics to submit their profile details and documents during onboarding.
    Requires authentication.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MechanicProfileSerializer

    def get_object(self):
        # Create profile if it doesn't exist
        profile, created = MechanicProfile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer):
        # When mechanic updates profile, ensure status is PENDING for review
        serializer.save(verification_status='PENDING')
