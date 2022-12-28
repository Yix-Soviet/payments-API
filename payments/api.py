from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Payments
from .serializers import PaymentSerializer
from .pagination import StandardResultsSetPagination

class PaymentsViewSet(viewsets.ModelViewSet):
   queryset = Payments.objects.get_queryset().order_by('id')
   serializer_class = PaymentSerializer
   pagination_class = StandardResultsSetPagination
   filter_backends = [filters.SearchFilter]
   permission_classes = [IsAuthenticated]

   search_fields = ['users_id', 'payment_date', 'service']
   throttle_classes = 'payment'