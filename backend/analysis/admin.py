# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (AssessmentMethod, AssessmentQuery, Corpus, Transcript,
                     UploadFile, Utterance)


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    model = Corpus


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    model = Transcript


@admin.register(Utterance)
class UtteranceAdmin(admin.ModelAdmin):
    model = Utterance


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    model = UploadFile


@admin.register(AssessmentMethod)
class AssessmentMethodAdmin(admin.ModelAdmin):
    model = AssessmentMethod


@admin.register(AssessmentQuery)
class AssessmentQueryAdmin(admin.ModelAdmin):
    model = AssessmentQuery
