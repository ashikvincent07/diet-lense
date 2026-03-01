from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from diet_app.serializers import UserSerializer, UserProfileSerializer, FoodLogSerializer
from diet_app.permissions import IsOwner, ProfileRequired
from diet_app.models import UserProfile, User, FoodLog
from diet_app.get_diet_plan import generate_kerala_diet_plan
from diet_app.process_food_image import analyze_food



class UserRegisterView(CreateAPIView):
    
    permission_classes = [permissions.AllowAny]

    serializer_class = UserSerializer



class UserRetrieveView(RetrieveAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    serializer_class = UserSerializer

    queryset = User.objects.all()



class UserProfileCreateView(CreateAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):

    #     validated_data = serializer.validated_data

    #     cal = daily_calorie_consumption(height=validated_data.get("height"), weight=validated_data.get("weight"),
    #                                     age=validated_data.get("age"), gender=validated_data.get("gender"),
    #                                     activity_level=float(validated_data.get("activity_level", 1.2)))

        return serializer.save(owner=self.request.user)
    


class UserProfileRetrieveUpdateView(RetrieveAPIView, UpdateAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ProfileRequired, IsOwner]

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()
        


class FoodLogCreateListView(ListCreateAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = FoodLogSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return FoodLog.objects.filter(owner=self.request.user)
    


class FoodLogRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [ProfileRequired, IsOwner]

    serializer_class = FoodLogSerializer

    def get_queryset(self):
        return FoodLog.objects.all()



class SummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ProfileRequired]

    def get(self, request, *args, **kwrags):

        current_date = timezone.now().date()

        try:

            qs = FoodLog.objects.filter(owner=request.user, created_at__date=current_date)

            total_consumed = qs.values('calories').aggregate(total=Sum('calories'))

            meal_type_summary = qs.values('meal_type').annotate(total=Sum('calories'))

            context = {
                "daily_target":request.user.profile.bmr,
                "total_consumed":total_consumed.get("total", 0),
                "balance": request.user.profile.bmr - total_consumed.get("total", 0),
                "meal_type_summary": meal_type_summary
            }

            return Response(data=context)
        
        except Exception as e:

            return Response(str(e))
        


class GetDietPlan(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ProfileRequired]

    def post(self, request, *args, **kwargs):

        age = request.user.profile.age

        weight = request.user.profile.weight

        height = request.user.profile.height

        gender = request.user.profile.gender

        goal = request.data.get("goal")

        target_weight = request.data.get("target_weight")

        duration = request.data.get("duration")

        result = generate_kerala_diet_plan(goal=goal,age=age,
                                           weight=weight,gender=gender,
                                           target_weight=target_weight,duration=duration)

        return Response(data=result)
    


class AnalyzeFoodImageView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,ProfileRequired]

    def post(self,request,*args,**kwargs):

        image = request.data.get("image")

        data = analyze_food(image)

        food_instance = FoodLog.objects.create(name=data.get("food_name"),calories=data.get("average_calorie"),owner=request.user)

        serializer_instance = FoodLogSerializer(food_instance)

        return Response(data=serializer_instance.data)