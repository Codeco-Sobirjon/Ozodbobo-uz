from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categories, Blog
from apps.blog.serializers.serializers import CategoriesSerializer, BlogSerializer, BlogCommentSerialzier
from apps.blog.pagination import BlogPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoriesListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a list of categories",
        responses={200: CategoriesSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesDetailAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a single category by its ID",
        responses={200: CategoriesSerializer()}
    )
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Categories, id=kwargs.get('pk'))
        serializer = CategoriesSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a single blog post by its ID",
        responses={200: BlogSerializer()}
    )
    def get(self, request, *args, **kwargs):
        queryset = get_object_or_404(Blog, id=kwargs.get('pk'))

        queryset.is_seen += 1
        queryset.save()

        serializer = BlogSerializer(queryset, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class CarouselBlogListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a list of blog posts for a specific category",
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Categories, id=kwargs.get('pk'))
        queryset = Blog.objects.prefetch_related('category').filter(category=category)[:4]
        serializer = BlogSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularBlogListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve the top 3 most seen blog posts for a specific category",
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Categories, id=kwargs.get('pk'))
        queryset = Blog.objects.prefetch_related('category').filter(category=category).annotate(
            seen_count=F("is_seen")
        ).order_by('-seen_count')[:3]

        serializer = BlogSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of blog posts for a specific category",
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Categories, id=kwargs.get('pk'))
        queryset = Blog.objects.prefetch_related('category').filter(category=category).order_by('-is_seen')

        paginator = BlogPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = BlogSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = BlogSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogCommentCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new blog comment",
        request_body=BlogCommentSerialzier,
        responses={201: BlogCommentSerialzier()}
    )
    def post(self, request, *args, **kwargs):
        serializer = BlogCommentSerialzier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

