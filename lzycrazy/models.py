from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Userprofile(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)


class Posts(models.Model):
    user= models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='posts/', blank=True, null=True)
    video_file = models.FileField(upload_to='posts/', blank=True, null=True)
    audio_file = models.FileField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post by {self.user.firstname} {self.user.lastname}"
    
    
class Comments(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.firstname} {self.user.lastname} on Post {self.post.id}"


class Likes(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} likes Post {self.post.id}"


class Share(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shared by {self.user.firstname} {self.user.lastname} at {self.created_at}"



User = get_user_model()

class FriendRequests(models.Model):
    id = models.AutoField(primary_key=True)    
    sender = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['sender', 'receiver']


class Friends(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='friend_friends')
        
    class Meta:
        unique_together = ['user', 'friend']


class Chat(models.Model):
    sender = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='chat_sender')
    receiver = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='chat_receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Categorybanners(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='banners/')


class Subcategorybanners(models.Model):
    id = models.AutoField(primary_key=True)
    categoryid = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='subbanners/')


class TimelineImage(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='timeline_images/')


class ProfileImage(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    mobile = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)


  
class FilterCategorys(models.Model):
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FilterOption(models.Model):
    category = models.ForeignKey(FilterCategorys, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Story(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)
    video = models.FileField(upload_to='story_videos/', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)



class Productchats(models.Model):
    sender = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='productchat_sender')
    receiver = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='productchat_receiver')
    message = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product')
    timestamp = models.DateTimeField(auto_now_add=True)

