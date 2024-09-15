# your_app/middleware.py

from django.utils import translation


class SetLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set language here. You can also use logic to determine language based on user preference.
        user_language = 'ru'
        translation.activate(user_language)
        request.LANGUAGE_CODE = user_language  # Set the language code in request

        response = self.get_response(request)

        # Optionally deactivate translation
        translation.deactivate()
        return response
