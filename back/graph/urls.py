from django.urls import path
from . import views
from .suggest import parse_lines

urlpatterns = [
    path('create', views.CreateGraph.as_view()),
    path('dump-lines', parse_lines.calc_suggest_data),
    path('update/<int:pk>', views.UpdateGraph.as_view()),
    path('<int:pk>', views.DetailGraph.as_view()),
    path('<int:pk>/', views.DetailGraph.as_view()),

    # legacy
    #path('upload-home', views.UploadHome.as_view(), name='home'),
    path('edit', views.Reactview.as_view(), name='edit'),
    path('upload', views.file_upload, name='upload-file'),
    path('', views.ListGraph.as_view()),
]
