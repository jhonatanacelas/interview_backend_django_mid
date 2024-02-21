from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q


from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


class OrdersBetweenDatesView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        embargo_date = self.request.query_params.get('embargo_date', None)
        
        if start_date and embargo_date:
            return Order.objects.filter(
                Q(start_date__gte=start_date) &
                Q(embargo_date__lte=embargo_date)
            )
        else:
            return Order.objects.none()  # Return an empty queryset if parameters are missing


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
