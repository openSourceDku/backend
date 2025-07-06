from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Fixture
from .serializers import FixtureSerializer
from django.http import HttpResponse

# Create your views here.

def index(request) :
    return HttpResponse("hello manager apps")

class FixtureCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  #Authentication required

    def post(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = FixtureSerializer(data=request.data)
        if serializer.is_valid():
            fixture = serializer.save()
            return Response({
                "itemId": fixture.id,
                "name": fixture.name,
                "price": fixture.price,
                "count": fixture.count
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FixtureUpdateView(APIView):    
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, itemId):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            fixture = Fixture.objects.get(id=itemId)
        except Fixture.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FixtureSerializer(fixture, data=request.data, partial=True)
        if serializer.is_valid():
            fixture = serializer.save()
            return Response({
                "itemId": fixture.id,
                "name": fixture.name,
                "price": fixture.price,
                "count": fixture.count
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FixtureDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, itemId):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            fixture = Fixture.objects.get(id=itemId)
        except Fixture.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        fixture.delete()
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
class FixtureListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        page = int(request.GET.get('page',1))   #Retrieve query parameters(page, size)
        size = int(request.GET.get('size',10))
        #Get all data quryset
        queryset = Fixture.objects.all().order_by('id')
        total_count = queryset.count()
        total_page = (total_count + size - 1) // size

        #Apply pagination
        start = (page - 1) * size
        end = start + size
        fixtures = queryset[start:end]

        #Serialize data and convert id to itemId
        data = [
            {
                "itemId":obj.id,
                "name": obj.name,
                "price": obj.price,
                "count": obj.count
            }
            for obj in fixtures
        ]
        return Response({
            "page": page,
            "size": size,
            "totalPage": total_page,
            "totalCount": total_count,
            "data": data
        }, status=status.HTTP_200_OK)
    
    