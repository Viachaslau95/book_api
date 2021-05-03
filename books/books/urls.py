from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, auth, UserBooksRelationView

router = SimpleRouter()
router.register(r'book_relation',UserBooksRelationView)

router.register(r'book', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth)
]

urlpatterns += router.urls
