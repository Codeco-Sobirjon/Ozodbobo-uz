from rest_framework import serializers
from apps.blog.models import Categories, Blog, BlogImage, BlogComment
from apps.blog.utils import Util
from config.settings import EMAIL_HOST_USER


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['id', 'name']


class BlogImageListSerialzier(serializers.ModelSerializer):

    class Meta:
        model = BlogImage
        fields = ['image']


class BlogSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'is_seen', 'category', 'images', 'comment', 'video', 'created_at']

    def get_images(self, obj):
        queryset = BlogImage.objects.select_related('blog').filter(blog=obj)
        serializer = BlogImageListSerialzier(queryset, many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_category(self, obj):
        serializer = CategoriesSerializer(obj.category.all(), many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_comment(self, obj):
        queryset = BlogComment.objects.select_related('blog').filter(blog=obj)
        serializer = BlogCommentSerialzier(queryset, many=True, context={'request': self.context.get('request')})
        return serializer.data


class BlogCommentSerialzier(serializers.ModelSerializer):

    class Meta:
        model = BlogComment
        fields = ['id', 'full_name', 'phone', 'comment', 'blog']

    def create(self, validated_data):
        create_commnet = BlogComment(**validated_data)
        self.send_to_email(create_commnet)
        return create_commnet

    def send_to_email(self, create_commnet):
        email_body = (f"{create_commnet.full_name} tominidan,  shu {create_commnet.blog.title} postga murojat qildi. "
                      f"\n Komment: {create_commnet.comment}")
        email_data = {
            "email_body": email_body,
            "to_email": EMAIL_HOST_USER,
            "email_subject": "Qabul qiling",
        }
        Util.send(email_data)