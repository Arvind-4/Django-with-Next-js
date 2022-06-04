from django.shortcuts import render

def handler404(request, exception, template_name="_next/404.html"):
    return render(request, template_name, context={}, status=404)