from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name="signup"),
    path('welcome/',views.welcome,name="welcome"),
    path('signout/',views.signout,name="signout"),
    path('forget/',views.forget,name="forget"),

    path('home/<int:id>/',views.home,name="home"),
    path('profile/<int:id>/',views.profile,name="profile"),
    path('edit_profile/<int:id>/',views.edit_profile,name="edit_profile"),
    path('update_profile/<int:id>/',views.update_profile,name="update_profile"),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


    path('people/<int:id>/',views.people,name="people"),
    path('friend_list/<int:id>/', views.friend_list, name='friend_list'),
    path('friend_requests/<int:id>/',views.friend_requests,name="friend_requests"),   
    path('friend_request_notifications/<int:id>/',views.friend_request_notifications,name="friend_request_notifications"),
    path('accept_friend_request/<int:friend_request_id>/',views.accept_friend_request,name="accept_friend_request"),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('add_friend/<int:sender_id>/<int:receiver_id>/', views.add_friend, name='add_friend'),


    path('show_friends_posts/', views.show_friends_posts, name='show_friends_posts'),
    path('editphoto/<int:id>/',views.editphoto,name="editphoto"),   
    path('editvideo/<int:id>/',views.editvideo,name="editvideo"),          
    path('editaudio/<int:id>/',views.editaudio,name="editaudio"),

    #path('create_post/<int:id>/', views.create_post, name='create_post'),
    path('like_post/<int:id>/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:id>/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('share/', views.share_content, name='share_content'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),


    path('chat/<int:friend_id>/', views.chat, name='chat'),
    path('friend_chat/<int:id>/', views.friend_chat, name='friend_chat'),
    path('chat_view/<int:id>/<int:friend_id>/', views.chat_view, name='chat_view'),
    path('send_message/<int:id>/<int:friend_id>/',views.send_message,name="send_message"),


    path('productdetails',views.productdetails,name="productdetails"),

 # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('subcategory_list/<int:category_id>/', views.subcategory_list, name='subcategory_list'),
    path('propertyfilters/<int:subcategory_id>/<int:category_id>/', views.propertyfilters, name='propertyfilters'),
    path('applyfilters/', views.applyfilters, name='applyfilters  '),
    path('product_list/<int:subcategory_id>/', views.product_list, name='product_list'),
    path('productdetails/<int:product_id>/', views.productdetails, name='productdetails'),

    path('sellproduct/',views.sellproduct,name="sellproduct"),
    path('addproduct/',views.add_product,name="addproduct"),


    path('productchat/<int:user_id>/<int:id>/',views.productchat,name="productchat"),
    path('productcontact/<int:mobile>/',views.productcontact,name="productcontact"),
   
    path('upload_timeline_pic/<int:id>/', views.upload_timeline_pic, name='upload_timeline_pic'),
    path('upload_profile_image/<int:id>/',views.upload_profile_image,name="upload_profile_image"),

    path('myads/<int:id>/',views.myads,name="myads"),
    path('editproduct/<int:product_id>/', views.edit_product, name='edit_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/<int:category_id>/<int:subcategory_id>/', views.show_products, name='show_products'),


    path('add_post/<int:id>/', views.add_post, name='add_post'),

    path('create_story/', views.create_story, name='create_story'),
    path('show_stories/', views.show_stories, name='show_stories'),
   path('show_story/<int:story_id>/', views.show_story, name='show_story'),


    # ...
    path('product_chat/<int:product_id>/', views.product_chat, name='product_chat'),
    path('send_message/<int:product_id>/', views.sendmessage, name='send_message'),

    path('buyerchat/<int:sender_id>/<int:product_id>/', views.buyerchat, name='buyerchat'),
    path('sendmessages/<int:sender_id>/<int:product_id>/', views.sendmessages, name='sendmessages'),
    path('chatlist/<int:id>/',views.chatlist,name="chatlist"),  

 ] 