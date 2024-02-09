from django.shortcuts import render
from balls.models import route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Device
from balls.serializers import LocationSerializer, RouteSerializer, HistorySerializer
from .serializers import DeviceInfoSerializer
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@api_view(['GET'])
def device_history_routes(request, device_seq):
    print('device app // device_histiory_routes : ON')
    histry_data = route.objects.filter().order_by('-created_at')[:5]
    # print(histry_data)
    serializer = HistorySerializer(histry_data, many=True)
    # print(serializer)
    return Response(serializer.data)


@api_view(['POST'])
def device_check(request):
    serialnum = request.data.get('serial_num')
    device_info = get_object_or_404(Device, serial_num=serialnum)
    # print(device_info)
    serializer = DeviceInfoSerializer(device_info)
    return Response(serializer.data)
