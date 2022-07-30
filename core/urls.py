from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from common.ckeditor_views import browse, upload
from django.contrib.auth.decorators import login_required

import debug_toolbar

urlpatterns = [
    re_path("ckeditor/upload/", login_required(upload), name="ckeditor_upload"),
    re_path(
        "ckeditor/browse/",
        login_required(browse),
        name="ckeditor_browse",
    ),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include("product.urls")),
    path('api/v1/', include("common.urls")),
    path('__debug__/', include(debug_toolbar.urls)),
]

# MEDIA URLS
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
