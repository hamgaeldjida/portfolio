from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Contact
from .serializers import ContactSerializer

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(
            {
                'status': 'success',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
