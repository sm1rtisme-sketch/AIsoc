from django.http import JsonResponse


def tools(request):
    return JsonResponse({'tools': []})


def external_mcp(request):
    return JsonResponse({'servers': []})
