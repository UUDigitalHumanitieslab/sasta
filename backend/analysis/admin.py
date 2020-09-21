# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (AssessmentMethod, AssessmentQuery, Compound, CompoundFile,
                     Corpus, MethodCategory, Transcript, UploadFile, Utterance)


class TranscriptInline(admin.TabularInline):
    model = Transcript


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    model = Corpus
    inlines = (TranscriptInline,)


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
    readonly_fields = ('date_added',)
    list_display = ('category', 'name', 'queries')

    def queries(self, obj):
        if obj.queries:
            return len(obj.queries.all())
        return 0


@admin.register(AssessmentQuery)
class AssessmentQueryAdmin(admin.ModelAdmin):
    model = AssessmentQuery


@admin.register(CompoundFile)
class CompoundFileAdmin(admin.ModelAdmin):
    model = CompoundFile


@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    model = Compound


@admin.register(MethodCategory)
class MethodCategoryAdmin(admin.ModelAdmin):
    model = MethodCategory
