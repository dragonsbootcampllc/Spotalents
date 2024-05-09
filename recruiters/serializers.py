from rest_framework import serializers
from django.contrib.auth.models import Group, User

from recruiters.models import Recruiter, Question, Application, Category, JobPost, Applied, Interview
from recruiters.models import JobPost, Application


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']

# serialize all the modles
class RecruiterSerializer(serializers.ModelSerializer):
    user = serializers.DictField(write_only=True)
    
    class Meta:
        model = Recruiter
        fields = ['id','user', 'date_of_birth']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            validated_data['user'] = user
        return super().create(validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question','answer','answered','q_type']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ApplicationSerializer(serializers.ModelSerializer):
    # recruiter = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all())
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Application
        fields = ['id', 'recruiter', 'questions'] 
    
    # def create(self, validated_data):
    #     questions_data = validated_data.pop('questions', None)
    #     print(questions_data)
    #     recruiter = validated_data.pop('recruiter', None)
        
    #     application = Application.objects.create(recruiter=recruiter)
        
    #     if questions_data:
    #         for question_data in questions_data:
    #             question = Question.objects.create(**question_data)
    #             application.questions.add(question)
        
    #     application.save()
    #     return application




class JobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPost
        fields = ['id', 'recruiter_id', 'category', 'name', 'description', 'candidates_number', 'application', 'active']
    
    # def create(self, validated_data):
    #     application_data = validated_data.pop('application', None)
    #     recruiter = validated_data.pop('recruiter', None)  # Extract recruiter data
    #     job_post = JobPost.objects.create(recruiter=recruiter, **validated_data)  # Create JobPost with recruiter
        
    #     if application_data:
    #         application_serializer = ApplicationSerializer(data=application_data)
    #         application_serializer.is_valid(raise_exception=True)
    #         application = application_serializer.save()
    #         job_post.application = application
    #         job_post.save()
        
    #     return job_post

    

    

class AppliedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applied
        fields = ['recruiter','applicant','approved']

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['recruiter','applicant','date']

