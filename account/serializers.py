from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .tasks import send_activation_code_celery


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True, write_only=True)
    slug = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    verified_account = serializers.ReadOnlyField()

    user_type = serializers.ChoiceField(
            required=True,
            help_text='Select user type',
            choices=(
                ('Default user', 'Default user (Donations only)'),
                ('User helper', 'User helper (Creating charity programs)'),
                ('Fund', 'Fund (Creating charity programs as organization)')
            )
        )
    
    class Meta:
        model = User
        fields = (
            'slug',
            'first_name', 
            'last_name',
            'username',
            'email',
            'password',
            'password_confirm',
            'user_photo',
            'date_joined',
            'twitter_url',
            'facebook_url',
            'telegram_url',
            'about_user',
            'user_type',
            'verified_account',
            'id'
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password mismatch')
        if attrs.get('user_type') == 'Default user':
            attrs['verified_account'] = True
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user
    
    def validate_twitter_url(self, twitter_url):
        if not twitter_url.startswith('https://twitter.com/'):
            raise serializers.ValidationError('Uncorrect twitter link. Example: "https://twitter.com/Username"')
        return twitter_url

    def validate_facebook_url(self, facebook_url):
        if not facebook_url.startswith('https://www.facebook.com/'):
            raise serializers.ValidationError('Uncorrect facebook link. Example: "https://www.facebook.com/Username"')
        return facebook_url
    
    def validate_telegram_url(self, facebook_url):
        if not facebook_url.startswith('https://t.me/'):
            raise serializers.ValidationError('Uncorrect telegram link. Example: "https://t.me/Username"')
        return facebook_url
    


class ChangePasswordSerializer(serializers.ModelSerializer):
    
    old_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password_confirm = serializers.CharField(
        min_length=4, required=True
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password_confirm')

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.pop('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Password mismatch!')
        return attrs

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Uncorrecct password')
        return old_password

    def set_new_password(self):
        user = self.context['request'].user
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User is not found")
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Password recovery',
            f'Your activation code: {user.activation_code}',
            'example@gmail.com',
            [user.email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User is not found or wrong activation code')
        if password1 != password2:
            raise serializers.ValidationError('Password mismatch!')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()
    

class ProfileSerializer(serializers.ModelSerializer):
    verified_account = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'user_photo',
            'telegram_url',
            'twitter_url',
            'date_joined',
            'facebook_url',
            'user_type',
            'about_user',
            'verified_account'
        ]