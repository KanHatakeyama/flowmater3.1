from django.shortcuts import render
from .models import Graph, MediaFile
from .serializer import GraphSeriarizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from rest_framework import permissions

MAX_RETURN_GRAPHS = 30

# return recently updated graph lists


class ListGraph(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # if True:
        try:
            graphs = Graph.objects.filter()
            graphs = Graph.objects.all().order_by(
                '-updated_at')[:MAX_RETURN_GRAPHS]
            print(type(graphs))
            res_list = [
                {
                    'pk': d.pk,
                    'title': d.title,
                    # 'graph': d.graph,
                }
                for d in graphs
            ]
            return Response(res_list)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailGraph(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            try:
                d = Graph.objects.get(id=pk)
            except:
                error_msg = "target graph not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
            res = {
                'title': d.title,
                'graph': d.graph,
                "tags": d.tags,
            }
            return Response(res)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateGraph(generics.UpdateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Graph.objects.all()
    serializer_class = GraphSeriarizer


class CreateGraph(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GraphSeriarizer


# caution! no auth for file upload!
def file_upload(request):
    if request.method == "POST":
        my_file = request.FILES.get('file')
        obj = MediaFile.objects.create(upload=my_file)
        return HttpResponse(f"file {obj.pk}_{obj.filename()}")

    return JsonResponse({'post': 'false'})


class Reactview(TemplateView):
    template_name = 'public/index.html'
