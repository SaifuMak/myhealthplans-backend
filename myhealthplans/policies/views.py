from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Policy
from .serializers import PolicySerializer,PolicyEditSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from authentication.views import JWTAuthentication
from .pagination import PolicyPagination
from django.shortcuts import get_object_or_404
from  trash.models import FilePendingDelete
from django.db import transaction

class PolicyActions(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Policy added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        query = request.query_params.get('query')
        policies = Policy.objects.all().order_by("-created_at")
        if query:
             policies =  policies.filter(name__icontains = query)
        paginator = PolicyPagination()
        result_page = paginator.paginate_queryset(policies, request)

        serializer = PolicySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class PolicyDetailView(APIView):
  
    def get(self, request, pk):
        policy = get_object_or_404(Policy, pk=pk)
        serializer = PolicySerializer(policy)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def patch(self, request, pk):
        policy = get_object_or_404(Policy, pk=pk)

        #  If user uploads a new file, store the old file name for cleanup later
        for field in ["aadhar", "pan", "document"]:
            if field in request.FILES:
                old_file = getattr(policy, field)
                if old_file:
                    FilePendingDelete.objects.create(file_path = old_file)

        serializer = PolicySerializer(policy, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        policy = get_object_or_404(Policy, pk=pk)

        for field in ["aadhar", "pan", "document"]:
            old_file = getattr(policy, field)
            if old_file:
                FilePendingDelete.objects.create(file_path=old_file)

        policy.delete()
        return Response(
            {"message": "Policy deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
