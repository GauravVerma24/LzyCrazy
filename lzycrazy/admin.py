from django.contrib import admin
from .models import Posts,Category,Product,Subcategory,FilterCategorys, FilterOption,Categorybanners,Subcategorybanners,TimelineImage,ProfileImage

# Register your models here.

admin.site.register(Posts)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Categorybanners)
admin.site.register(Subcategorybanners) 
admin.site.register(TimelineImage) 
admin.site.register(ProfileImage) 
admin.site.register(Product) 
admin.site.register(FilterCategorys)
admin.site.register(FilterOption)