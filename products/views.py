from rest_framework import generics, permissions
from .models import Lesson, Product, User
from django.db.models import Count, Sum
from .serializers import ProductStatisticSerializer, LessonSerializer


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


def get_queryset(self):
    user = self.request.user
    products = user.product_set.all()
    return Lesson.objects.filter(products__in=products)


class LessonByProductListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        product = user.product_set.get(id=product_id)
        return product.lesson_set.all()


class LessonByProductDetail(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        product = user.product_set.get(id=product_id)
        return product.lesson_set.all()


class ProductStatisticView(generics.ListAPIView):
    serializer_class = ProductStatisticSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.annotate(
            num_views=Count('lesson__view', distinct=True),
            total_time=Sum('lesson__view__watched_time'),
            num_users=Count('owner', distinct=True),
            acquisition_percentage=Count('productaccess') / User.objects.count() * 100)


