from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_410_GONE
from rest_framework.views import APIView


class ParseTaskView(APIView):
    '''View for starting Alpino parse tasks and retrieving task status'''

    def get(self, request, *args, **kwargs):
        '''Returns task status'''
        task_id = kwargs.get("task_id", None)
        if task_id is None:
            return Response("No task ID specified.", HTTP_400_BAD_REQUEST)
        result = {
            "task_id": task_id,
            "task_status": "running",
            "task_result": False
        }
        return Response(result, HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Starts a parse task and returns task id'''
        # TODO: start task
        return Response(None, HTTP_410_GONE)
