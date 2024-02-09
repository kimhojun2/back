from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import location, route
from accounts.models import User
from .serializers import LocationSerializer, RouteSerializer, HistorySerializer
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from A202.settings import message_queue

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def ball_location(request, loca_seq):
    loca = get_object_or_404(location, pk=loca_seq)
    serializer = LocationSerializer(loca)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quizball(request, quiz_num):
    quiz_data = get_list_or_404(location, is_quiz=1)
    quiz = quiz_data[quiz_num]
    serializer = LocationSerializer(quiz)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def quiz_answer(request, quiz_num):
    quiz_data = get_list_or_404(location, is_quiz=1)

    if 0 <= quiz_num < len(quiz_data):
        target = quiz_data[quiz_num]
        print(target.id)
        quiz_answer_data = get_list_or_404(route, loca_seq=target)[0]
        print(quiz_answer_data)
        serializer = RouteSerializer(quiz_answer_data)
        return Response(serializer.data)
    
    else:
        return Response({'message': 'No Quiz'}, status=404)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def my_history_route(request, username):
    user = get_object_or_404(User, username=username)
    user_id = user.pk
    # histry_data = get_list_or_404(route, user_seq=user_id)
    histry_data = route.objects.filter(user_seq=user_id).order_by('-created_at')[:10]
    serializer = HistorySerializer(histry_data, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def ball_to_device(request):
    print(request.data)
    if 'sign' in request.data:
        sign_data = request.data['sign']
        if sign_data == '0':
            print('녹화 시작')
            message_queue.put('0큐에서 전송 성공')
            return JsonResponse({"message": "Received sign data successfully."})
        else:
            print('사용 종료')
            return JsonResponse({"message": "Received sign data successfully."})
    elif 'route_seq' in request.data:
        print(f'기기에 경로 다시보기 좌표 전송')
        return JsonResponse({"message": "Received route_seq successfully."})
    elif 'loca_seq' in request.data:
        print('기기에 공 좌표 전송')
        seq = int(request.data['loca_seq'])
        loca_info = get_object_or_404(location, pk=seq)
        message_queue.put(f'0{loca_info.loca_file}')
        return JsonResponse({"message": "Received ball_seq successfully."})
    