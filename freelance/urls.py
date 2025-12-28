from django.contrib import admin
from django.urls import path

import freelance.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", freelance.views.home),
    path("posts/", freelance.views.post_list),
    path("posts/<int:post_id>/", freelance.views.post_detail),
]

