from rest_framework import permissions


class IsCorpusOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_admin


class IsCorpusChildOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        corpus = obj.corpus
        return corpus.user == request.user or request.user.is_admin

# class IsTranscriptOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         corpus = obj.corpus
#         return corpus.user == request.user or request.user.is_admin


# class IsUploadOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         corpus = obj.corpus
#         return corpus.user == request.user or request.user.is_admin
