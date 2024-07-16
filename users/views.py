from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime, timedelta
import base64, qrcode
from io import BytesIO

from users.models import CustomUser
from .forms import UserRegisterForm, CustomUserChangeForm, CustomPasswordChangeForm, PasswordResetRequestForm, PasswordResetForm

# When new user is registered, send email to staff with new user name, email and joined date
def _send_new_user_notification(username, email, date_joined):

    formatted_date_joined = date_joined.strftime('%Y-%m-%d %H:%M:%S')

    User = get_user_model()
    staff_users = User.objects.filter(is_staff=True)
    
    subject = f'A new user {username} has registered. Please allocate configurations promptly.'
    message = f'New user registration information\n\nUsername: {username}\nEmail: {email}\nRegistration Time: {formatted_date_joined}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in staff_users]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


# When new user is registered, send email to welcome the new user name
def _send_new_user_welcome_notification(username, email, date_joined):
    
    formatted_date_joined = date_joined.strftime('%Y-%m-%d %H:%M:%S')

    subject = 'Welcome to our website!'
    message = (
        f'Dear {username},\n\n'
        f'Thank you for registering on our website! We are delighted to have you join our network.\n'
        f'Here are your registration details:\n\n'
        f'Username: {username}\n'
        f'Email: {email}\n'
        f'Registration Time: {formatted_date_joined}\n\n'
        f'Next, please return to our website to complete the device network configuration. You can find relevant instructions under "Configuration."\n'
        f'You can also view the assigned configuration link under "Profile."\n'
        f'Please note: After initial registration, please allow our operations team some time to assign customized configuration details.\n\n'
        f'If you have any questions or need assistance, feel free to contact us.\n\n'
        f'Best regards,\n'
        f'Our Product Team'
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def register(request):

    username = request.POST.get('username', '')
    email = request.POST.get('email', '')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, 'Registration successful! Redirecting to home page...')

                # When new user is registered, send email to staff with new user name, email and joined date
                # notify the staff with email and date joined
                email = form.cleaned_data.get('email')
                date_joined = user.date_joined
                _send_new_user_notification(username, email, date_joined)
                _send_new_user_welcome_notification(username, email, date_joined)
                return redirect('users:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {
        'form': form,
        'username': username,
        'email': email,
    })

def login_view(request):
    error_message = None
    username = request.POST.get('username', '')  # Get the username from POST data

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                error_message = "Username or Password is Incorrect."
        else:
            error_message = "Username or Password is Incorrect."
    else:
        form = AuthenticationForm()

    # Pass 'username' to the template to keep it populated in the input field
    return render(request, 'users/login.html', {
        'form': form,
        'error_message': error_message,
        'username': username  # Pass the username to the template
    })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')  # use name space 'users'

def _format_flow(data_flow):
    if data_flow / 1024 < 1024:
        return f'{data_flow / 1024:.2f} Kb'
    elif data_flow / 1024 / 1024 < 1024:
        return f'{data_flow / 1024 / 1024:.2f} Mb'
    elif data_flow / 1024 / 1024 / 1024 < 1024:
        return f'{data_flow / 1024 / 1024 / 1024:.2f} Gb'
    else:
        return data_flow

def _format_timestamp(data_flow):
    if data_flow == 0:
        return f'-'
    else:
        data_flow //= 1000
        dt_obj = datetime.fromtimestamp(data_flow)
        return f'{dt_obj}'

def _get_qr_src(protocal):

    # make qr code
    qr = qrcode.QRCode(
        box_size=4,
        border=2
    )
    qr.add_data(protocal)
    qr.make(fit=True)

    # save qr code image to memory
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)

    # image decode as Base64, encoding utf-8
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"


def home(request):
    return render(request, 'users/home.html')

@login_required
def profile(request):
    # request current session user
    user = request.user


    if user.is_authenticated:
        # get current user joined ProtocolConfig object
        protocol_config = request.user.protocol_config

        # if protocol_config is optional, need to deal with null situation
        if protocol_config:

            context = {
                'joined_date': user.date_joined,
                'email': user.email,
                'status_set': True,
                'up': _format_flow(protocol_config.up),
                'down': _format_flow(protocol_config.down),
                'total': _format_flow(protocol_config.total),
                'expiry_time': _format_timestamp(protocol_config.expiry_time),
                'config_url': protocol_config.config_url,
                'qr_src': _get_qr_src(protocol_config.config_url),
            }
        else:
            context = {
                'joined_date': user.date_joined,
                'email': user.email,
                'status_set': False,
            }
    else:
        context = {}
    # print(context)
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.POST)

        if not user_form.has_changed() and not password_form.has_changed():
            return redirect('users:home')

        user_form_valid = user_form.is_valid()
        password_form_valid = password_form.is_valid()

        if user_form_valid:
            user_form.save()

        if password_form_valid and password_form.cleaned_data.get('new_password1'):
            user = password_form.save(request.user)
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change

        if user_form_valid or (password_form_valid and password_form.cleaned_data.get('new_password1')):
            return redirect('users:home')  # Redirect to user profile page
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm()

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
        'user_name': user.username,
    })


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # 获取表单中的用户名
            username = form.cleaned_data['username']

            # 查询用户是否存在
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return render(request, 'users/password_reset_request.html', {'form': form, 'error_message': 'User not exists'})

            # 生成随机令牌
            token = get_random_string(length=32)

            # 设置令牌的有效期为10分钟
            token_expiry = timezone.now() + timedelta(minutes=10)

            # 将令牌和过期时间保存到用户模型中（假设有一个字段叫做reset_token和reset_token_expiry）
            user.reset_token = token
            user.reset_token_expiry = token_expiry
            user.save()

            # 生成重置密码链接并发送邮件
            domain = request.META['HTTP_HOST']
            protocol = 'https' if request.is_secure() else 'http'
            reset_url = f"{protocol}://{domain}/reset_password/{username}/{token}/"

            send_mail(
                'Password Reset',
                f'Please click the link to reset your password: {reset_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return render(request, 'users/password_reset_request.html', {'form': form, 'success_message': 'The reset link has been sent to your email. Please check your inbox.'})

    else:
        form = PasswordResetRequestForm()

    return render(request, 'users/password_reset_request.html', {'form': form})


def reset_password(request, username, token):
    try:
        user = CustomUser.objects.get(username=username, reset_token=token)
    except CustomUser.DoesNotExist:
        return render(request, 'users/reset_password_expired.html')

    # 检查令牌是否过期
    if user.reset_token_expiry < timezone.now():
        return render(request, 'users/reset_password_expired.html')

    if request.method == 'POST':
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.reset_token = None
            user.reset_token_expiry = None
            user.save()

            # 自动登录用户
            user = authenticate(request, username=user.username, password=new_password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')  # 重定向到用户的个人资料页面

        else:
            # 打印表单错误以进行调试
            print(form.errors)
    else:
        form = PasswordResetForm(user)

    return render(request, 'users/reset_password.html', {'form': form})

def ios_guide(request):
    return render(request, 'users/guide/ios_guide.html')

def android_guide(request):
    return render(request, 'users/guide/android_guide.html')

def mac_guide(request):
    return render(request, 'users/guide/mac_guide.html')

def windows_guide(request):
    return render(request, 'users/guide/windows_guide.html')

def price(request):
    return render(request, 'users/components/price.html')

def service(request):
    return render(request, 'users/components/service.html')

