from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_202_ACCEPTED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from .tasks import test_model


class ParseTaskView(APIView):
    '''View for starting Alpino parse tasks and retrieving task status'''
    status_code_mapping = {
        "PENDING": HTTP_202_ACCEPTED,
        "STARTED": HTTP_202_ACCEPTED,
        "RETRY": HTTP_202_ACCEPTED,
        "FAILURE": HTTP_500_INTERNAL_SERVER_ERROR,
        "SUCCESS": HTTP_200_OK,
    }

    def get(self, request, *args, **kwargs):
        '''Returns task status'''
        task_id = kwargs.get("task_id", None)
        if task_id is None:
            return Response("No task ID specified.", HTTP_400_BAD_REQUEST)

        task = AsyncResult(str(task_id))

        response = Response()
        response.data = {
            "task_id": task.id,
            "task_status": task.status,
            "task_result": task.result
        }
        response.status_code = self.status_code_mapping.get(task.status, HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    def post(self, request, *args, **kwargs):
        '''Starts a parse task and returns task id'''
        # TODO: start task
        transcript_id = request.data.get('transcript_id')
        res = test_model.apply_async([transcript_id], countdown=10)

        return Response({
            "transcript_id": transcript_id,
            "task_id": res.id},
            HTTP_202_ACCEPTED)
