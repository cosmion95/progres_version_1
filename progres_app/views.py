from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, Codes
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.


@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_user(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


@api_view(['PUT'])
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        operation = user.delete()
        data = {}
        if operation:
            data["success"] = "delete successful!"
        else:
            data["failure"] = "FAIL!"
        return Response(data=data)


@api_view(['POST'])
def register_user(request):
    try:
        User.register(request.data)
        data = {"success": "Registration complete. We've sent an activation code to your email."}
        return Response(data=data, status=status.HTTP_201_CREATED)
    except Exception as e:
        error_msg = str(e).split(' ', 1)[1].split('\n', 1)[0]
        data = {"error": error_msg}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def generate_user_registration_token(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.generate_registration_token()
        data = {"success": "A new token has been generated and sent to the account's email address."}
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_msg = str(e).split(' ', 1)[1].split('\n', 1)[0]
        data = {"error": error_msg}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def validate_user_registration(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.validate_user_registration(request.data["token"])
        data = {"success": "User has been validated. The account is now active."}
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error_msg = str(e).split(' ', 1)[1].split('\n', 1)[0]
        data = {"error": error_msg}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
