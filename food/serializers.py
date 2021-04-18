from rest_framework import serializers
from .models import *
from .backends import TokenAuthentication
from django.contrib.auth import authenticate

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class MealCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCategories
        fields = ['id', 'name', 'departments']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class ServicePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePercentage
        fields = ['id', 'percentage']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'category', 'price', 'description']


class MealToOrdersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = MealToOrder
        fields = ['id', 'name', 'count']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'waiter', 'table', 'status', 'date', 'meals']

    def create(self, validated_data):
        meals = validated_data.pop('meals')
        instance = Order.objects.create(**validated_data)
        for meal in meals:
            instance.meals.add(meal)

        return instance


class ChecksSerializer(serializers.ModelSerializer):
    # meals = MealToOrdersSerializer(many=True)
    percentage = serializers.CharField(read_only=True, source='percentage.percentage')

    # totalsum = serializers.CharField(source='get_totalsum', read_only=True)

    class Meta:
        model = Check
        fields = ['id', 'order', 'date', 'percentage', 'totalsum']

    def create(self, validated_data):
        check = Check.objects.create(
            percentage=ServicePercentage.objects.all()[0]
        )
        check.save()

        return check



class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'surname', 'phone', 'date', 'email', 'login', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    login = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        login = data.get('login', None)
        password = data.get('password', None)

        if login is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )


        user = authenticate(login=login, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'login': user.login,
            'email': user.email,
            'token': user.token
        }


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Old password is not correct'})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
