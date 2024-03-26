from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from authapp.serializers import LeadSerializer, UserSerializer
from django.contrib.auth import authenticate
from authapp.models import CustomUser, Lead
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response({"message": "This is the signup page."})

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user = CustomUser.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except CustomUser.DoesNotExist:
                pass

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username / email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        return Response({"message": "This is the login page."})

class UpdateViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['put'])
    def update_profile(self, request, pk=None):
        username = pk
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteViewSet(viewsets.ViewSet):    
    @action(detail=True, methods=['delete'])
    def destroy_profile(self, request, pk=None):
        username = pk
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Lead.objects.filter(status=status)
        return Lead.objects.all()

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get('name')
        try:
            lead = Lead.objects.get(name=name)
            serializer = self.get_serializer(lead)
            return Response(serializer.data)
        except Lead.DoesNotExist:
            return Response({'error': 'Lead does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'Lead has been successfully added.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'message': 'Lead has been successfully updated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'message': 'Lead has been partially updated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Lead has been successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)