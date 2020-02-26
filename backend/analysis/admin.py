# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (AssessmentMethod, AssessmentQuery, Corpus, Transcript,
                     UploadFile, Utterance)


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    model = Corpus


@admin.register(Utterance)
class UtteranceAdmin(admin.ModelAdmin):
    list_display = ('transcript', '__str__')
    model = Utterance


class UtteranceInline(admin.TabularInline):
    model = Utterance


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    inlines = (UtteranceInline, )
    list_display = ('__str__', 'status')
    model = Transcript


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    model = UploadFile


@admin.register(AssessmentMethod)
class AssessmentMethodAdmin(admin.ModelAdmin):
    model = AssessmentMethod


@admin.register(AssessmentQuery)
class AssessmentQueryAdmin(admin.ModelAdmin):
    model = AssessmentQuery
