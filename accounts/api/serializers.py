from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class ClientForManagerSerializer(serializers.ModelSerializer):
    """ Serializer for Manager to see and update Client """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active', 'is_closed')

        read_only_fields = ('id', 'first_name', 'last_name', 'email', )


class ClientRegisterSerializer(serializers.ModelSerializer):
    """ Serializer for register clients """

    token = serializers.CharField(read_only=True)
    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            passport_number=validated_data['passport_number'],
            is_active=False
        )


        user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'passport_number', 'token')


class UserLoginSerializer(serializers.ModelSerializer):
    """ Serializer for login users """

    email = serializers.EmailField()
    token = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'token')

        write_only_fields = ('email', 'password')

    def validate(self, data):

        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('This email is not valid')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorect credentials try again')
        data['token'] = user.token
        return data


class ClientProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Client to see and update profile """


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'passport_number', 'balance', 'is_active', 'is_closed')

        read_only_fields = ('id', 'balance', )



class ClientProvidePINSerilizer(serializers.ModelSerializer):
    """ Serializer for Client to provide PIN """

    password1 = serializers.CharField(label='Verify PIN', write_only=True)
    class Meta:
        model = User
        fields = ('password', 'password1')

        extra_kwargs = {
            'password': {'label': 'PIN'},
        }

    def validate_password1(self, value):
        data = self.get_initial()
        pin1 = data.get('password')
        pin2 = data.get('password1')

        if pin1 != pin2:
            raise serializers.ValidationError("PINs don't match", code="pins_dont_match")

