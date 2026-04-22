from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegistrationView, CurrentUserView, VerifyOTPView, 
    ResendOTPView, AdminStatsView, AdminUserListView, AdminUserToggleActiveView
)

from apps.marketplace.views import (
    AdminMechanicVerificationListView, AdminMechanicVerifyActionView, 
    AdminMechanicDetailView, MechanicOnboardingView
)
from apps.bookings.views import AdminBookingListView, AdminBookingOverrideView
from apps.operations.views import AdminDisputeListView, AdminDisputeActionView, AdminPaymentListView
from apps.core.views import AdminPlatformConfigView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('mechanic/onboarding/', MechanicOnboardingView.as_view(), name='mechanic_onboarding_api'),
    # Admin API - Users
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin/users/<int:pk>/toggle-active/', AdminUserToggleActiveView.as_view(), name='admin_user_toggle_active'),
    
    # Admin API - Marketplace (Mechanics)
    path('admin/mechanics/verifications/', AdminMechanicVerificationListView.as_view(), name='admin_mechanic_verifications'),
    path('admin/mechanics/<int:pk>/verify/', AdminMechanicVerifyActionView.as_view(), name='admin_mechanic_verify'),
    path('admin/mechanics/<int:pk>/', AdminMechanicDetailView.as_view(), name='admin_mechanic_detail'),
    
    # Admin API - Bookings
    path('admin/bookings/', AdminBookingListView.as_view(), name='admin_bookings'),
    path('admin/bookings/<int:pk>/override/', AdminBookingOverrideView.as_view(), name='admin_booking_override'),
    
    # Admin API - Operations
    path('admin/disputes/', AdminDisputeListView.as_view(), name='admin_disputes'),
    path('admin/disputes/<int:pk>/action/', AdminDisputeActionView.as_view(), name='admin_disputes_action'),
    path('admin/payments/', AdminPaymentListView.as_view(), name='admin_payments'),
    
    # Admin API - Core
    path('admin/config/', AdminPlatformConfigView.as_view(), name='admin_config'),
]
