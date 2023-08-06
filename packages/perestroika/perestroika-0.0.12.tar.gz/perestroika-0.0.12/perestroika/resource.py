class DjangoResource:
    from django.views.decorators.csrf import csrf_exempt

    methods = None

    @csrf_exempt
    def handler(self, request):
        from django.http import HttpResponseNotAllowed

        if self.methods:
            method = self.methods.get(request.method.lower())

            if method:
                return method.handle(request)

        permitted_methods = self.methods.values() if self.methods else []
        return HttpResponseNotAllowed(permitted_methods=permitted_methods)

    def schema(self, request):
        from django.http import JsonResponse
        _schema = {
            k: v.schema() for k, v in self.methods.items()
        }

        return JsonResponse(_schema)
