from django.urls import path
from .views import classroom_list, create_classroom_and_class, class_detail

urlpatterns = [
    path('classrooms/', classroom_list, name='classroom_list'), #반, 할 일 생성
    # path('', create_classroom_and_class, name='create_classroom_and_class'),
    # path('<int:class_id>', class_detail, name='class_detail'),
] 