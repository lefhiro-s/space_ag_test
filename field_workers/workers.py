from field_workers.models import FieldWorker
from field_workers.serializers import FieldWorkersSerializer

from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response


class WorkersView(viewsets.ViewSet):
    """
    List Workers methods [List, Create, Partial Update, Retrieve, Destroy]
    """
    lookup_field = 'worker_id'
    serializer_class = FieldWorkersSerializer

    def __get_worker(self, worker_id):
        try:
            return FieldWorker.objects.get(id=worker_id)
        except FieldWorker.DoesNotExist:
            raise Http404

    def __validate_data(self, data):

        if not data.get('first_name'):
            raise ParseError('first_name is required')

        if not data.get('last_name'):
            raise ParseError('last_name is required')

        functions = ['Harvest', 'Pruning', 'Scouting', 'Other']
        if data.get('function') and data.get('function') not in functions:
            raise ParseError('function field is not valid')

    def __build_response(self, request, page):
        workers = FieldWorker.objects.all()
        paginator = Paginator(workers, 10)
        data = []

        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = []

        serializer = self.serializer_class(data, many=True)

        return {
            'content': serializer.data,
            'count': paginator.count,
            'numpages': paginator.num_pages
        }

    def list(self, request, format=None):
        page = request.query_params.get('page', 1)
        json_response = self.__build_response(request, page)
        return Response(json_response, status=status.HTTP_200_OK)

    def create(self, request, format=None):
        data = request.data
        self.__validate_data(data)
        data['function'] = data.get('function', 'Other')
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ParseError(serializer.errors)

    def partial_update(self, request, worker_id, format=None):
        data = request.data
        worker = self.__get_worker(worker_id)
        functions = ['Harvest', 'Pruning', 'Scouting', 'Other']
        if data.get('function') and data.get('function') not in functions:
            raise ParseError('function field is not valid')
        serializer = self.serializer_class(worker, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ParseError(serializer.errors)

    def retrieve(self, request, worker_id=None):
        worker = self.__get_worker(worker_id)
        serializer_class = self.serializer_class(worker)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def destroy(self, request, worker_id=None):
        worker = self.__get_worker(worker_id)
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
