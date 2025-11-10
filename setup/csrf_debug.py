from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware

def csrf_debug_view(request, reason=""):
    response = HttpResponse(
        f"""
        <h1>❌ Falha na verificação CSRF</h1>
        <p><b>Motivo:</b> {reason}</p>
        <p><b>Referer:</b> {request.META.get('HTTP_REFERER')}</p>
        <p><b>Host:</b> {request.get_host()}</p>
        <p><b>Cookie recebido:</b> {request.COOKIES.get('csrftoken')}</p>
        <p><b>Token enviado no formulário:</b> {request.POST.get('csrfmiddlewaretoken')}</p>
        """,
        content_type="text/html"
    )
    response.status_code = 403
    return response
