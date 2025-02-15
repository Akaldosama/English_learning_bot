import json
import logging
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User, LearningEnglish

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            fullname = data.get('fullname', None)
            phone = data.get('phone', None)
            level = data.get('level', None)
            # skill = data.get('skill', None)

            if not telegram_id:
                return JsonResponse({'error': 'Telegram ID is required.'}, status=400)

            user, created = User.objects.get_or_create(telegram_id=telegram_id)

            if not created and user.is_registered:
                return JsonResponse({
                    'message': 'User is already registered.',
                    'level': user.level
                }, status=200)

            if fullname and phone and level:
                user.fullname = fullname
                user.phone = phone
                user.level = level
                user.is_registered = True
                user.save()

                return JsonResponse({
                    'message': 'User registered successfully.',
                    'level': user.level,
                }, status=200)
            else:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

from django.shortcuts import get_object_or_404
@method_decorator(csrf_exempt, name="dispatch")
class MaterialView(View):
    def get(self, request):
        telegram_id = request.GET.get("telegram_id")
        skill = request.GET.get("skill")  # 'listening', 'reading', 'writing', 'speaking'

        if not telegram_id or not skill:
            return JsonResponse({"error": "Missing parameters."}, status=400)

        user = get_object_or_404(User, telegram_id=telegram_id)
        if not user.level:
            return JsonResponse({"error": "User level not set."}, status=400)

        learning_material = LearningEnglish.objects.filter(level=user.level).first()
        if not learning_material:
            return JsonResponse({"error": "No materials found for this level."}, status=404)

        skill_mapping = {
            "listening": learning_material.listening,
            "reading": learning_material.reading,
            "writing": learning_material.writing,
            "speaking": learning_material.speaking,
        }

        file_field = skill_mapping.get(skill)
        if not file_field or not file_field.name:
            return JsonResponse({"error": f"No {skill} material available."}, status=404)

        file_url = f"https://534b-84-54-84-135.ngrok-free.app/media/{file_field.name}"

        print(f"Generated file URL: {file_url}")

        return JsonResponse({"file_url": file_url})

