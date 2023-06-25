from rest_framework import viewsets, serializers, status, views,generics
from .models import Scheduler
from .serializers import ScheduleSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from datetime import date, timedelta
from django.db.models import Sum, ExpressionWrapper, F, DurationField
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import LoginSerializer


# Create your views here.

# class LoginView(views.APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return Response({'token': user.auth_token.key})
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SchedulerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Scheduler.objects.all()
    serializer_class = ScheduleSerializer
    
    def validate_event_overlap(self, start_date, end_date):
        overlapping_events = Scheduler.objects.filter(
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        return overlapping_events.exists()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        if start_date >= end_date:
            return Response({'error': 'End date must be greater than start date.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if self.validate_event_overlap(start_date, end_date):
            raise serializers.ValidationError("Overlapping events are not allowed.")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.get('start_date', instance.start_date)
        end_date = serializer.validated_data.get('end_date', instance.end_date)

        if self.validate_event_overlap(start_date, end_date):
            raise serializers.ValidationError("Overlapping events are not allowed.")

        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False)
    def analytics(self, request):
        thirty_days_ago = date.today() - timedelta(days=30)
        analytics = Scheduler.objects.filter(
            start_date__gte=thirty_days_ago
        ).values('event_name', 'start_date').annotate(
            duration=Sum(ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField()))
        )
        return Response(analytics)