from django.utils.translation import ugettext_lazy as _

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_extensions.cache.mixins import RetrieveCacheResponseMixin

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission, HasObjectPermission
from rdmo.conditions.models import Condition
from rdmo.questions.models import Catalog, QuestionSet

from .models import Project, Snapshot, Value
from .filters import ValueFilterBackend
from .serializers import ProjectSerializer, ValueSerializer
from .serializers.questionset import QuestionSetSerializer
from .serializers.catalog import CatalogSerializer
from .serializers.api import (
    ProjectSerializer as ProjectApiSerializer,
    SnapshotSerializer as SnapshotApiSerializer,
    ValueSerializer as ValueApiSerializer
)


class ProjectViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ValueViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, HasObjectPermission)
    serializer_class = ValueSerializer

    filter_backends = (ValueFilterBackend, DjangoFilterBackend)
    filter_fields = (
        'attribute',
        'set_index'
    )

    permission_required = {
        'view': 'projects.view_value_object',
        'add': 'projects.add_value_object',
        'change': 'projects.change_value_object',
        'delete': 'projects.delete_value_object'
    }

    def get_queryset(self):
        return Value.objects.filter(project=self.project, snapshot=self.snapshot) \
            .order_by('set_index', 'collection_index')

    def get_project(self, request):
        project_id = request.GET.get('project')

        if project_id is None:
            raise ValidationError({'project': [_('This field is required.')]})
        else:
            try:
                return Project.objects.get(pk=project_id)
            except Project.DoesNotExist as e:
                raise ValidationError({'project': [e.message]})

    def get_snapshot(self, request):
        snapshot_id = request.GET.get('snapshot')

        if snapshot_id is None:
            return None
        else:
            try:
                return self.project.snapshots.get(pk=snapshot_id)
            except Snapshot.DoesNotExist as e:
                raise ValidationError({'snapshot': [e.message]})

    def get_condition(self, request):
        condition_id = request.GET.get('condition')

        if condition_id is None:
            raise ValidationError({'condition': [_('This field is required.')]})
        else:
            try:
                return Condition.objects.get(pk=condition_id)
            except Condition.DoesNotExist as e:
                raise ValidationError({'condition': [e.message]})

    def get_permission_object(self):
        return self.project

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_project(request)
        self.snapshot = self.get_snapshot(request)

        return super(ValueViewSet, self).dispatch(request, *args, **kwargs)

    @list_route()
    def resolve(self, request):
        self.project = self.get_project(request)

        condition = self.get_condition(request)
        return Response({'result': condition.resolve(self.project, self.snapshot)})


class QuestionSetViewSet(RetrieveCacheResponseMixin, ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer

    @list_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def first(self, request, pk=None):
        try:
            catalog = Catalog.objects.get(pk=request.GET.get('catalog'))
            questionset = QuestionSet.objects.order_by_catalog(catalog).first()
            serializer = self.get_serializer(questionset)
            return Response(serializer.data)
        except Catalog.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def prev(self, request, pk=None):
        try:
            return Response({'id': QuestionSet.objects.get_prev(pk).pk})
        except QuestionSet.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @detail_route(methods=['get'], permission_classes=[DjangoModelPermissions])
    def next(self, request, pk=None):
        try:
            return Response({'id': QuestionSet.objects.get_next(pk).pk})
        except QuestionSet.DoesNotExist as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)


class CatalogViewSet(RetrieveCacheResponseMixin, ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class ProjectApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Project.objects.all()
    serializer_class = ProjectApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'title',
        'user',
        'user__username',
        'catalog',
        'catalog__uri',
        'catalog__key',
    )


class SnapshotApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'title',
        'project'
    )


class ValueApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Value.objects.all()
    serializer_class = ValueApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'project',
        'snapshot',
        'attribute',
        'attribute__uri',
        'attribute__path',
        'option__uri',
        'option__path',
    )
