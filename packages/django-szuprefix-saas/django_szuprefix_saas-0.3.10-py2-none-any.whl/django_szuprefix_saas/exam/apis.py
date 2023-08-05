# -*- coding:utf-8 -*-
from rest_framework.decorators import list_route, detail_route
from rest_framework.serializers import ModelSerializer

from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix_saas.saas.mixins import PartyMixin, PartySerializerMixin
from django_szuprefix_saas.saas.permissions import IsSaasWorker
from django_szuprefix_saas.school.permissions import IsStudent, IsTeacher
from .apps import Config
from rest_framework.response import Response
from rest_condition.permissions import Or

__author__ = 'denishuang'
from . import models, serializers, stats
from rest_framework import viewsets, filters
from django_szuprefix.api.helper import register
from rest_framework import status


class PaperViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Paper.objects.all()
    serializer_class = serializers.PaperFullSerializer
    search_fields = ('title',)
    filter_fields = {'id': ['in', 'exact'], 'is_active': ['exact'], 'is_break_through': ['exact']}
    ordering_fields = ('is_active', 'title', 'create_time')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PaperSerializer
        return super(PaperViewSet, self).get_serializer_class()

    @detail_route(['post'], permission_classes=[IsSaasWorker])
    def answer(self, request, pk=None):
        paper = self.get_object()
        serializer = serializers.AnswerSerializer(data=request.data, party=self.party)
        if serializer.is_valid():
            answer = serializer.save(user=self.request.user, paper=paper)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            data['is_passed'] = answer.performance.get('stdScore') >= models.EXAM_MIN_PASS_SCORE
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(['get'])
    def stat(self, request, pk=None):
        paper = self.get_object()
        if hasattr(paper, 'stat'):
            serializer = serializers.StatSerializer(instance=paper.stat)
            d = serializer.data
            pms = request.query_params
            answers = paper.answers.all()
            clazz = pms.get('clazz')
            if clazz:
                from django_szuprefix_saas.school.models import Student
                uids = Student.objects.filter(clazz_id=clazz).values_list('user_id', flat=True)
                answers = answers.filter(user__in=uids)

            if pms.get('recent'):
                d['answer_user'] = stats.count_answer_user(answers, ['yesterday', 'today', 'all'])

            if pms.get('by_answer'):

                from django_szuprefix.utils import statutils
                r = {'right': {}, 'userAnswer': {}}
                for a in answers:
                    statutils.group_stat(a.detail, ['number', 'right'], r['right'])
                    statutils.group_stat(a.detail, ['number', 'userAnswer'], r['userAnswer'])

                co = paper.content_object
                for g in co['groups']:
                    for q in g['questions']:
                        num = q['number']
                        q['stat'] = {'right': r['right'].get(num), 'userAnswer': r['userAnswer'].get(num)}
                    g['questions'].sort(key=lambda a: a['stat']['right'].get(True))
                d['content_object'] = co
            return Response(d)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    @list_route(['get'], permission_classes=[Or(IsStudent, IsTeacher)])
    def for_course(self, request):
        course_id = request.query_params.get("id")
        course = self.party.course_courses.get(id=course_id)
        serializer = serializers.CoursePaperSerializer(course)
        from django.forms import model_to_dict
        c = serializer.data
        unlock = False
        user = request.user

        def fill_papers(papers, unlock=False):
            pids = [p.get('id') for p in papers]
            pfs = user.exam_performances.filter(paper_id__in=pids)
            pfm = dict([(p.paper_id, p) for p in pfs])
            for p in papers:
                performance = pfm.get(p['id'])
                ibt = p.get('is_break_through')
                if ibt:
                    if (performance is None or performance.is_passed == False) and unlock is False:
                        unlock = True
                        p['lock'] = 'unlock'
                    elif performance is not None and performance.is_passed == True:
                        p['lock'] = None
                    else:
                        p['lock'] = 'lock'
                else:
                    p['lock'] = None

                # if p.get('is_break_through') and unlock is False and (
                #                 performance is None or performance.is_passed == False):
                #     unlock = True
                #     p['unlock'] = True
                p['performance'] = model_to_dict(performance, ['score', 'detail', 'is_passed']) if performance else None
            return unlock

        for cpt in c['chapters']:
            unlock = fill_papers(cpt['exam_papers'], unlock)
        fill_papers(c['exam_papers'])
        return Response(dict(course=c))

    @list_route(['get'], permission_classes=[IsSaasWorker, ])  # [ IsStudent])
    def for_student(self, request):
        major = self.party.as_school.majors.first()
        # major = request.user.as_school_student.major
        serializer = serializers.CoursePaperSerializer(major.course_courses.all(), many=True)
        from django.forms import model_to_dict
        performances = dict([(p.paper_id, model_to_dict(p, ['score', 'detail'])) for p in
                             models.Performance.objects.filter(user=request.user)])
        courses = serializer.data
        for c in courses:
            unlock = False
            for cpt in c['chapters']:
                for p in cpt['exam_papers']:
                    performance = performances.get(p['id'])
                    if unlock is False and (
                                    performance is None or performance['passed'] == False):
                        unlock = True
                        p['unlock'] = True
                    p['performance'] = performance
        return Response(dict(courses=courses))

    @detail_route(methods=['get'])
    def my_performance(self, request, pk):
        paper = self.get_object()
        performance = request.user.exam_performances.filter(paper=paper).first()
        serializer = serializers.PerformanceSerializer(performance)
        return Response(serializer.data)


register(Config.label, 'paper', PaperViewSet)


class AnswerViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    filter_fields = ('paper',)

    @list_route(['get'])
    def list_stat(self, request):
        qset = self.get_queryset()
        pms = request.query_params
        ms = pms.getlist('measures', ['all'])
        ans = stats.count_answer_user(qset, ms, begin_time=pms.get('begin_time'), end_time=pms.get('end_time'))
        return Response({'users': ans})


register(Config.label, 'answer', AnswerViewSet)


class StatViewSet(PartyMixin, UserApiMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Stat.objects.all()
    serializer_class = serializers.StatSerializer
    filter_fields = ('paper',)


register(Config.label, 'stat', StatViewSet)


class PerformanceViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Performance.objects.all()
    serializer_class = serializers.PerformanceSerializer
    filter_fields = ('paper',)
    search_fields = ('paper__title',)
    ordering_fields = ('score', 'update_time')

    def filter_queryset(self, queryset):
        qset = super(PerformanceViewSet, self).filter_queryset(queryset)
        ids = self.request.query_params.get("papers")
        # qset = qset.filter(user=self.request.user)
        if ids:
            qset = qset.filter(paper_id__in=[int(id) for id in ids.split(",")])
        return qset


register(Config.label, 'performance', PerformanceViewSet)
