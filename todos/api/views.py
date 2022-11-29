from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import Todoss
from api.serializers import TodoSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from api.serializers import RegistrationSerializer
from rest_framework import authentication,permissions
# Create your views here.
 

#viewset
class TodosViews(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todoss.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todoss.objects.get(id=id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)
    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        TodosViews.objects.get(id=id).delete()
        return Response (data="deleted")
    def update(self,request,*args,**kw):
        id=kw.get("pk")
        objects=Todoss.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        






#model view set
        

#localhost:8000/api/v1/todos/pending_todos/
#GET
        
#localhost:8000/api/v1/todos/Completed_todos/
#GET        
        



class TodosModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoSerializer
    queryset=Todoss.objects.all()


    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todoss.objects.filter(status=False)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todoss.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todoss.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=True)
        return Response(data=serializer.data)      
    

    def list(self,request,*args,**kw):                            
        qs=Todoss.objects.filter(user=request.user)     #OR     def get_queryset(self):
        serializers=TodoSerializer(qs,many=True)         #          return Todoss.objects.filter(user=self.request.user)    
        return Response(data=serializers.data)

    def create(self, request, *args, **kwargs):              
        serializer=TodoSerializer(data=request.data,context={"user":request.user})       #OR       def perform_create(self ,serializer)
        if serializer.is_valid():                           #            serializer.save()
            Todoss.objects.create(**serializer.validated_data,User=request.User)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)         
     

 #auth  model view   
    

class UserView(ModelViewSet):
   
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()
    
    # def create(self, request, *args, **kwargs):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)