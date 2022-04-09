from django.urls import path
from . import views
from . import parse_lines

urlpatterns = [
    path('create', views.CreateGraph.as_view()),
    path('dump-lines', parse_lines.collect_all_graphs),
    path('update/<int:pk>', views.UpdateGraph.as_view()),
    path('<int:pk>', views.DetailGraph.as_view()),
    path('<int:pk>/', views.DetailGraph.as_view()),
    path('upload-home', views.UploadHome.as_view(), name='home'),
    path('upload', views.file_upload, name='upload-file'),
    path('', views.ListGraph.as_view()),
]
