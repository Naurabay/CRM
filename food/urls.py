from django.urls import path
from django.urls import path
from django.conf.urls import url

from .views import *
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'food'
urlpatterns = [

    path('tables/', TableList.as_view()),
    path('tables/<int:pk>/', TableDetail.as_view()),
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
    path('mealToOrder/<int:pk>', MealToOrderList.as_view()),
    path('mealCategories/', MealCategoryList.as_view()),
    path('mealCategories/<int:pk>/', MealCategoryDetail.as_view()),
    path('departments/', DepartmentList.as_view()),
    path('departments/<int:pk>/', DepartmentDetail.as_view()),
    path('meals/', MealList.as_view()),
    path('meals/<int:pk>/', MealDetail.as_view()),
    path('mealCategoriesByDepartment/<int:pk>/', MealCategoriesByDepartment.as_view()),
    path('statuses/', StatusList.as_view()),
    path('statuses/<int:pk>/', StatusDetail.as_view()),
    path('servicePercentage/', ServicePercentageList.as_view()),
    path('servicePercentage/<int:pk>/', ServicePercentageDetail.as_view()),
    path('checks/', CheckList.as_view()),
    path('checks/<int:pk>', CheckDetail.as_view()),
    path('users/reg/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('roles/', RoleList.as_view()),
    path('roles/<int:pk>/', RoleDetail.as_view()),
    path('users/update/',  PasswordChangeView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
