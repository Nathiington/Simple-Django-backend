from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializers

class TodoListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    #Get all to dos
    def get(self, request,*args,**kwargs):
        todos = Todo.objects.filter(user= request.user.id)
        serializer = TodoSerializers(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new to do
    def post(self, request, *args, **kwargs):
        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('completed'),
            'user':request.user.id
        }
        serializer = TodoSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # helper method for getting object given 2 parameters
    def getObject(self,todo_id,user_id):
        try:
            return Todo.objects.get(id=todo_id,user=user_id)
        except Todo.DoesNotExist:
            return None

    # actual method to retrieve task with specific id
    def get(self,request,todo_id,*args,**kwargs):
        todo_instance = self.getObject(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with this id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TodoSerializers(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a task with specific id
    def put(self, request):
        todo_instance = self.getObject(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with that id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TodoSerializers(instance = todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # delete a task with specific id
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.getObject(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with that id does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res":"Objected deleted successfully"},
            status = status.HTTP_200_OK
        )

