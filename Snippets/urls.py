from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="snipp_add"),
    path('snippets/<int:filter_type>/list', views.snippets_page, name="snipp_list"),
    path('snippets/<int:snippet_id>', views.snippet_detail, name="snippet-detail"),
    path('snippets/<int:snippet_id>/delete', views.delete_snippet, name="delete-snippet"),
    path('snippets/<int:snippet_id>/edit', views.edit_snippet, name="edit-snippet"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
