from django.shortcuts import redirect

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/login/') and (not request.path.startswith('/register/') or request.path == ""):
            if 'student_id' not in request.session:
                return redirect('/login/')

        response = self.get_response(request)
        return response
