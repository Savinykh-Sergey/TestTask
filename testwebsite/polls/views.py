from django.shortcuts import get_object_or_404
from polls.models import Product, Group, Lesson, UserProductAccess, User
from django.utils import timezone

from rest_framework import generics
from .serializers import ProductSerializer, LessonSerializer


def distribute_user_to_groups(user, product):
    if product.start_date_time <= timezone.now():
        groups = Group.objects.filter(product=product)
        users_in_groups = {group.id: group.members.count() for group in groups}
        min_group_id = min(users_in_groups, key=users_in_groups.get)
        if users_in_groups[min_group_id] < product.max_users:
            group = get_object_or_404(Group, id=min_group_id)
            group.members.add(user)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductLessonsAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        if UserProductAccess.objects.filter(user=user, product_id=product_id).exists():
            return Lesson.objects.filter(product_id=product_id)
        else:
            return Lesson.objects.none()


product1 = Product.objects.create(creator=User.objects.first(), name='Курс по Django', start_date_time=timezone.now(), cost=20000.00)
product2 = Product.objects.create(creator=User.objects.first(), name='Курс по React', start_date_time=timezone.now(), cost=19000.00)

lesson1 = Lesson.objects.create(product=product1, title='Введение в Django', video_link='https://example.com/django_intro')
lesson2 = Lesson.objects.create(product=product1, title='Модели в Django', video_link='https://example.com/django_models')
lesson3 = Lesson.objects.create(product=product2, title='Введение в React', video_link='https://example.com/react_intro')

group1 = Group.objects.create(product=product1, name='Группа 1', min_users=1, max_users=5)
group2 = Group.objects.create(product=product1, name='Группа 2', min_users=2, max_users=5)
group3 = Group.objects.create(product=product2, name='Группа 3', min_users=1, max_users=3)

user2 = User.objects.create_user(username='user2', password='password2')
user3 = User.objects.create_user(username='user3', password='password3')

group1.members.add(User.objects.first())
group1.members.add(User.objects.get(username='user2'))
group2.members.add(User.objects.get(username='user3'))
group3.members.add(User.objects.first())

UserProductAccess.objects.create(user=User.objects.first(), product=product1)
UserProductAccess.objects.create(user=User.objects.get(username='user2'), product=product1)
UserProductAccess.objects.create(user=User.objects.get(username='user3'), product=product2)


