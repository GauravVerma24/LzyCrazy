from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Userprofile,FriendRequests,Friends,Posts,Likes,Productchats,FilterCategorys, FilterOption,Comments,Share,Chat,Category, Subcategory,Product,Categorybanners,Subcategorybanners,TimelineImage,ProfileImage,Story
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404 
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse 
from django.db.models import Q
from django.core.files.storage import default_storage
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = Userprofile.objects.get(email=email)
            password = user.password  # Assuming the password field in UserProfile model is named 'password'
            recipient_email = user.email
            send_mail(
                'Password Recovery',
                f'Your password is: {password}',
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            return render(request,'forgetpasswordmessage.html')
        except Userprofile.DoesNotExist:
            messages.error(request, 'No user account exists with the provided email.')
        return redirect('forget')
    return render(request, 'forget.html')





def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        # Create a new Userprofile object
        userprofile = Userprofile.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            mobile=mobile,
            password=password,
            dob=dob,
            gender=gender,
            city=city
        )
        return redirect('welcome')
    
    return render(request, 'signup.html')


def welcome(request):
    return render(request, 'welcome.html')



def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Userprofile.objects.get(email=email, password=password)
            request.session['uid'] = user.id
            # Update is_online to True
            user.is_online = True
            user.save()
            return redirect(reverse('show_friends_posts'))
        except Userprofile.DoesNotExist:
            message = "Invalid email or password"
            return render(request, 'signin.html', {'message': message})
    return render(request, 'signin.html')



def signout(request):
    id=request.session.get('uid')
    user_profile=Userprofile.objects.get(id=id)    
    user_profile.is_online = False
    user_profile.save()
    logout(request)
    return redirect('signin')


def profile(request,id):
    user = Userprofile.objects.filter(id=id)
    posts = Posts.objects.filter(user=id)
    try:
        timeline_image = TimelineImage.objects.get(user_id=id)  # Replace 11 with the appropriate ID
    except ObjectDoesNotExist:
        timeline_image = None 
    try:    
        profile_image = ProfileImage.objects.get(user_id=id)
    except ObjectDoesNotExist:
        profile_image = None     
    current_user = request.session.get('uid')
    friend_request_count = FriendRequests.objects.filter(receiver=current_user).count()
    return render(request, 'profile.html', {'user':user,'posts':posts,'timeline_image':timeline_image,'profile_image':profile_image,'friend_request_count':friend_request_count})



def home(request,id):
    current_user = id
    friend_request_count = FriendRequests.objects.filter(receiver=current_user).count()
    context = {
        'friend_request_count': friend_request_count,
    }
    return render(request, 'home.html',context) 


def friend_list(request):
    return render(request, 'friend_list.html') 

def edit_profile(request,id):
    user = Userprofile.objects.get(id=id)
    if request.method == 'POST':
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.city = request.POST.get('city')
        user.gender = request.POST.get('gender')
        user.mobile = request.POST.get('mobile')
        user.save()
    context = {'user': user}
    return render(request, 'edit_profile.html', context)

def update_profile(request,id):
    try:
        user = Userprofile.objects.get(id=id)
    except Userprofile.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('profile')  
    if request.method == 'POST':
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        user.email = request.POST.get('email')
        user.city = request.POST.get('city')
        user.gender = request.POST.get('gender')
        user.mobile = request.POST.get('mobile')
        user.save()
        return redirect(reverse('profile', kwargs={'id': id}))  
    context = {'user': user}
    return render(request,'profile.html',context)



def delete_user(request, user_id):
    try:
        user = Userprofile.objects.get(pk=user_id)
        user.delete()
        messages.success(request, "User and related data deleted successfully.")
        return redirect('signin')  # Replace 'signin' with the actual URL name of your sign-in page
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('signin')

def upload_timeline_pic(request, id):
    if request.method == 'POST':
        user_profile = Userprofile.objects.get(id=id)
        image = request.FILES['timeline_image']
        try:
            timeline_image = TimelineImage.objects.get(user=user_profile)
            timeline_image.image = image  # Update the existing image
        except TimelineImage.DoesNotExist:
            timeline_image = TimelineImage(user=user_profile, image=image)
        timeline_image.save()
        return redirect(reverse('profile', args=[id]))  
    return redirect(reverse('profile', args=[id]))

def upload_profile_image(request, id):
    if request.method == 'POST':
        user_profile = get_object_or_404(Userprofile, id=id)
        image = request.FILES['profile_pic']
        try:
            profile_image = ProfileImage.objects.get(user=user_profile)
            profile_image.image = image  # Update the existing image
        except ProfileImage.DoesNotExist:
            profile_image = ProfileImage(user=user_profile, image=image)
        profile_image.save()
        return redirect(reverse('profile', args=[id]))  
    return redirect(reverse('profile', args=[id]))



def people(request, id):
    friend_requests = FriendRequests.objects.filter(sender=id).values_list('receiver', flat=True)
    friends = Friends.objects.filter(user_id=id).values_list('friend_id', flat=True)
    users = Userprofile.objects.exclude(pk=id).exclude(id__in=friend_requests).exclude(id__in=friends)
    current_user = request.session.get('uid')
    friend_request_count = FriendRequests.objects.filter(receiver=current_user).count()
    return render(request, 'people.html', {'users': users,'friend_request_count':friend_request_count})


def friend_requests(request,id):
    user = get_object_or_404(Userprofile, id=id)
    friend_requests = FriendRequests.objects.filter(receiver=user)
    return render(request, 'friend_requests.html', {'friend_requests': friend_requests})
                  

def add_friend(request,sender_id, receiver_id):
    FriendRequests.objects.create(sender_id=sender_id, receiver_id=receiver_id)
    return render(request,'people.html')

def friend_request_notifications(request, id):
    user = get_object_or_404(Userprofile, id=id)
    friend_requests = FriendRequests.objects.filter(receiver=user)
    current_user = request.session.get('uid')
    friend_request_count = FriendRequests.objects.filter(receiver=current_user).count()
    return render(request, 'friend_requests.html', {'friend_requests': friend_requests,'friend_request_count':friend_request_count})



User = get_user_model()
def accept_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequests.objects.get(id=friend_request_id)
        print(friend_request)
        sender_id = friend_request.sender_id
        receiver_id = friend_request.receiver_id
        Friends.objects.create(user_id=sender_id, friend_id=receiver_id)
        Friends.objects.create(user_id=receiver_id, friend_id=sender_id)
        friend_request.delete()
        return render(request,'friend_list.html',{'receiver_id':receiver_id})
    except ObjectDoesNotExist:
        return render(request,'friend_list.html')
    
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequests, id=request_id)
    if request.method == 'POST':
        friend_request.delete()
        return redirect('friend_request_notifications', id=request.user.id)
    return render(request, 'home.html', {'friend_request': friend_request})

def friend_list(request,id):
    user = id
    print(user)
    friends = Friends.objects.filter(user=user)
    current_user = request.session.get('uid')
    friend_request_count = FriendRequests.objects.filter(receiver=current_user).count()
    return render(request, 'friend_list.html', {'friends': friends,'friend_request_count':friend_request_count})


def editphoto(request, id):
     return render(request, 'editphoto.html', {'post_id':id})

def editvideo(request, id):
     return render(request, 'editvideo.html', {'post_id':id})

def editaudio(request, id):
     return render(request, 'editaudio.html', {'post_id':id})


def show_posts(request):
    posts = Posts.objects.filter(user=request.user)
    return render(request, 'profile.html', {'posts': posts})

def like_post(request, id, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Posts, id=post_id)
        userprofile = get_object_or_404(Userprofile, id=id)
        if Likes.objects.filter(post=post, user=userprofile).exists():
            return redirect(reverse('profile', args=[id]))
        like = Likes(post=post,user=userprofile)
        like.save()
    return redirect(reverse('profile', args=[id]))


def delete_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.delete()
    id=request.session.get('uid')
    return redirect(reverse('profile',args=[id]))  # Replace 'home' with the relevant URL name of the home page

def add_comment(request,id, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Posts, id=post_id)
        user = get_object_or_404(Userprofile, id=id)
        content = request.POST['content']
        comment = Comments(user=user, post=post, content=content)
        comment.save()
    return redirect(reverse('profile', args=[id]),{'comment':comment})

def comment(request, post_id):
    return render(request,'comment.html', {'post_id':post_id})


def share_content(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        share = Share(user=request.user, content=content)
        share.save()
        return redirect('home')
    return render(request, 'home.html')

def friend_chat(request, id):
    friend = Userprofile.objects.get(id=id)
    return render(request, 'friend_chat.html', {'friend':friend})
   
def chat(request):
    return render(request,'chat.html')    


def chat_view(request,id, friend_id):
    friend = Userprofile.objects.get(id=friend_id)
    current_user = get_object_or_404(Userprofile, id=friend_id)
    messages = Chat.objects.filter(Q(sender=current_user) | Q(receiver=current_user)).order_by('timestamp')
    return render(request, 'friend_chat.html', {'friend':friend,'messages': messages, 'current_user': current_user})

def send_message(request,id,friend_id):
    if request.method == 'POST':
        sender = Userprofile.objects.get(id=id)
        receiver = Userprofile.objects.get(id=friend_id)
        message = request.POST.get('message')
        msg=Chat(sender=sender, receiver=receiver, message=message)
        msg.save()
        return redirect('chat_view',id=id, friend_id=friend_id)
    return render(request, 'sendmessage.html')



def show_friends_posts(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        try:
            user = Userprofile.objects.get(id=user_id)
            # Get all friends
            friends = Friends.objects.filter(user=user)
            friend_profiles = Userprofile.objects.filter(id__in=friends.filter(friend__is_online=True).values_list('friend', flat=True))
            friend_ids = friends.values_list('friend_id', flat=True)  # Get friend IDs
            friends_posts = Posts.objects.filter(user_id__in=friend_ids).order_by('-created_at')
            friend_request_count = FriendRequests.objects.filter(receiver=user).count()
            stories = Story.objects.filter(user_id__in=friend_ids).order_by('-time')
            
            storiess = Story.objects.all()
            for story in storiess:
                expiry_time = story.time + timedelta(days=1)
                expiry_time=expiry_time.day
                current_time=timezone.now().day
                if current_time >= expiry_time:
                    story.delete()

            context = {
                'friends_posts': friends_posts,
                'user': user,
                'friend_profiles': friend_profiles,
                'friend_request_count': friend_request_count,
                'stories': stories
            }
            return render(request, 'home.html', context)
        except Userprofile.DoesNotExist:
            pass
    return render(request, 'signin.html')



def productdetails(request):
    return render(request,'productdetails.html')

def category_list(request):
    categories = Category.objects.all()
    banners = Categorybanners.objects.all()
    return render(request, 'category_list.html', {'categories': categories,'banners':banners})

def subcategory_list(request, category_id):
    category = Category.objects.get(id=category_id)
    category_name = category.name
    subcategories = category.subcategory_set.all()
    subbanners = Subcategorybanners.objects.filter(categoryid=category_id)
    return render(request, 'subcategory_list.html', {'category': category, 'category_name': category_name, 'subcategories': subcategories,'subbanners':subbanners})



def propertyfilters(request,subcategory_id, category_id):
    category = Category.objects.get(id=category_id)
    category_name = category.name
    subcategories = category.subcategory_set.all()
    subbanners = Subcategorybanners.objects.filter(categoryid=category_id)

    if category_name == 'Property':
        filters = []
        categories = FilterCategorys.objects.filter(subcategory_id=subcategory_id)
        print(categories)
        for category in categories:
            options = FilterOption.objects.filter(category=category)
            filter_data = {
                'name': category.name,
                'options': options
            }
            filters.append(filter_data)
        
        context = {
            'category_name': category_name,
            'subcategories': subcategories,
            'subbanners': subbanners,
            'filters': filters
        }
        return render(request, 'propertyfilters.html', context)
    else:
        return HttpResponse('<h3>Unauthorized</h3>', status=401)



def applyfilters(request):
    user = request.session.get('uid')
    selected_options = request.POST.getlist('selectedOptions[]')
    print(selected_options)
    filtered_products = Product.objects.exclude(user=user).filter(productname__in=selected_options)
    print(filtered_products)
    filtered_data = []
    print(filtered_products)
    for product in filtered_products:
        filtered_data.append({
            'id': product.id,
            'name': product.name,
            'productname': product.productname,
            'image': product.image.url,
            'price': str(product.price),
            'description': product.description,
            'mobile': str(product.mobile),
            'city': str(product.city)
        })
    return render(request, 'productlist.html', {'filtered_data': filtered_data})

    




def productchat(request,user_id,id):
    friend = Userprofile.objects.get(id=id)
    current_user = get_object_or_404(Userprofile, id=user_id)
    print(current_user,friend)
    messages = Productchats.objects.filter(Q(sender=current_user) | Q(receiver=current_user)).order_by('timestamp')
    print(messages)
    return render(request,'productchat.html',{'friend':friend,'messages': messages, 'current_user': current_user})





def product_chat(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.session.get('uid')  # Assuming you are using Django's built-in authentication system
    chat_messages = Productchats.objects.filter(
        Q(sender=product.user, receiver=user) | Q(sender=user, receiver=product.user)
    ).order_by('timestamp')
    print(chat_messages)
    context = {
        'product': product,
        'chat_messages': chat_messages
    }
    return render(request, 'productchat.html', context)

def sendmessage(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        userid = request.session.get('uid')
        user_profile = get_object_or_404(Userprofile, id=userid)
        receiver_profile = get_object_or_404(Userprofile, id=product.user_id)
        message = request.POST.get('message')
        chat_message = Productchats(sender=user_profile, receiver=receiver_profile, product=product, message=message)
        chat_message.save()
        return redirect('product_chat', product_id=product_id)
    return redirect('product_detail', product_id=product_id)


def chatlist(request, id):
    senders = Productchats.objects.filter(product_id=id)
    sender_list = [sender.sender for sender in senders]
    print(senders,sender_list,id)
    context = {
        'sender_list': sender_list,
        'id':id
    }
    return render(request, 'chatlist.html', context)


def buyerchat(request,sender_id, product_id):
    product = Product.objects.get(id=product_id)
    user = sender_id  # Assuming you are using Django's built-in authentication system
    messages = Productchats.objects.filter(
        Q(sender=product.user, receiver=user) | Q(sender=user, receiver=product.user)
    ).order_by('timestamp')
    print(messages)
    context = {
        'product': product,
        'messages': messages,
        'sender_id':sender_id,
        'product_id':product_id
    }
    return render(request, 'buyerchat.html', context)


def sendmessages(request, sender_id, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        sender = product.user
        receiver =get_object_or_404(Userprofile, id=sender_id)  
        message = request.POST.get('message')
        if message:  # Ensure that the message is not empty
            chat_message = Productchats(sender=sender, receiver=receiver, product=product, message=message)
            chat_message.save()            
        return redirect(reverse('buyerchat', args=[sender_id, product_id]))
    return render(request, 'buyerchat.html')




def productcontact(request,mobile):
    context = {'mobile': mobile}
    return render(request,'productcontact.html',context)


def product_list(request, subcategory_id):
    subcategory = Subcategory.objects.get(id=subcategory_id)
    products = subcategory.product_set.all()
    return render(request, 'product_list.html', {'subcategory': subcategory, 'products': products})

def productdetails(request, product_id):
    product = Product.objects.get(id=product_id)
    image = product.image  # Assuming the Product model has an image field
    user_id = product.user_id  # Fetch the user_id from the Product model
    context = {
        'product': product,
        'image': image,
        'user_id': user_id,

    }
    return render(request, 'productdetails.html', context)

def sellproduct(request):
    return render(request, 'sellproduct.html')




def add_product(request):
    subcategories = Subcategory.objects.all()
    subcategorynames = [subcategory.name for subcategory in subcategories]
    id=request.session.get('uid')
    user_profile = Userprofile.objects.get(id=id)
    firstname = user_profile.firstname
    if request.method == 'POST':
        user_id = request.session.get('uid')
        subcategory_name = request.POST.get('subcategoryname')
        subcategory = Subcategory.objects.get(name=subcategory_name)
        subcategory_id = subcategory.id
        name = request.POST.get('name')
        productname = request.POST.get('productname')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        product = Product(user_id=user_id, subcategory_id=subcategory_id, name=name,productname=productname, image=image, price=price,description=description, mobile=mobile,city=city)
        product.save()
        return redirect(reverse('myads',args=[user_id]))
    return render(request, 'addproduct.html',{'subcategorynames':subcategorynames,'firstname':firstname})

def myads(request, id):    
    try:
        product = [entry.product_id for entry in Productchats.objects.all()]
        ads = Product.objects.filter(user_id=id)  
        user = Userprofile.objects.get(id=id)
        fname = user.firstname  
        expiry_time = None  
        days_remaining=0
        for ad in ads:
            expiry_time = ad.date + timedelta(days=31)
            days_remaining = (expiry_time - timezone.now()).days
            if days_remaining <= 0:
                ad.delete()
        return render(request, 'myads.html', {'ads':ads,'product':product,'fname': fname,'days_remaining':days_remaining})
    except ObjectDoesNotExist:
        no_product_message = "No product found."
        user = Userprofile.objects.get(id=id)
        fname = user.firstname
        return render(request, 'myads.html', {'no_product_message': no_product_message, 'fname': fname})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.user_id = request.session.get('uid')
        product.subcategory_id = request.POST.get('subcategory_id')
        product.name = request.POST.get('name')
        product.productname = request.POST.get('productname')
        product.image = request.FILES.get('image')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.mobile = request.POST.get('mobile')
        product.save()
        return redirect('view_product')
    return render(request, 'edit_product.html', {'product': product})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.subcategory_id = request.POST.get('subcategory_id')
        product.name = request.POST.get('name')
        product.productname = request.POST.get('productname')
        product.image = request.FILES.get('image')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.mobile = request.POST.get('mobile')
        product.save()
        id=request.session.get('uid')
        return redirect(reverse('myads',args=[id]))
    return render(request, 'edit_product.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    id=request.session.get('uid')
    return redirect(reverse('myads',args=[id])) 


def show_products(request,category_id,subcategory_id):
    user = request.session.get('uid')
    category = Category.objects.get(id=category_id)
    category_id=category.id
    subcategory = Subcategory.objects.get(category_id=subcategory_id)
    subcategory_id=subcategory.category_id
    if subcategory_id is not None:
        user_profile = Userprofile.objects.exclude(id=user)
        users = user_profile.values_list('id', flat=True)
        products=Product.objects.filter(subcategory_id=subcategory_id, user_id__in=users)
    else:
        products = Product.objects.exclude(user=user)
    return render(request, 'productlist.html', {'products': products})








def add_post(request,id):
    if request.method == 'POST':
        user = Userprofile.objects.get(id=id)
        fname = user.firstname
        content = request.POST.get('content')
        image_file = request.FILES.get('image_file')
        video_file = request.FILES.get('video_file')
        audio_file = request.FILES.get('audio_file')
        post = Posts(user_id=user.id, content=content, image_file=image_file, video_file=video_file, audio_file=audio_file)
        post.save()
        return redirect(reverse('profile',args=[user.id])) 
    else:
         user = Userprofile.objects.get(id=id)
         fname = user.firstname
         return render(request, 'create_post.html', {'firstname': fname}) 





def create_story(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        user_profile = request.session.get('uid')
        story = Story.objects.create(user_id=user_profile, image=image, video=video)
        return redirect(('show_stories'))    
    return render(request, 'create_story.html')


def show_stories(request):
    user_profile = request.session.get('uid')
    friend_ids = Friends.objects.filter(user_id=user_profile).values_list('friend_id', flat=True)
    stories = Story.objects.filter(user__id__in=friend_ids).order_by('-time')
    redirect_url = reverse('show_friends_posts') + '?stories=' + ','.join(str(story.id) for story in stories)
    return redirect(redirect_url)


def show_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    context = {
        'story': story
    }
    return render(request, 'show_story.html', context)
