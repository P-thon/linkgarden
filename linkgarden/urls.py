from django.urls import path
from django.views.decorators.csrf import requires_csrf_token
from django.conf import settings
from django.conf.urls.static import static
from listings import view_public_form
from listings import view_public_static
from listings import view_admin
from listings import view_login
urlpatterns = [
    path('', requires_csrf_token(view_public_form.Home.as_view()), name = ''),
    path('error/', requires_csrf_token(view_public_static.Error.as_view()), name = 'error'),
    path('home/', requires_csrf_token(view_public_form.Home.as_view()), name = 'home'),
    path('ranking/', requires_csrf_token(view_public_form.Ranking.as_view()), name = 'ranking'),
    path('register/', requires_csrf_token(view_public_form.Register.as_view()), name = 'register'),
    path('verification/', requires_csrf_token(view_public_form.Verification.as_view()), name = 'verification'),
    path('admin-login/', requires_csrf_token(view_login.AdminLogin.as_view()), name = 'admin-login'),
    path('admin/', requires_csrf_token(view_admin.AdminDashboard.as_view()), name = 'admin'),
    path('logout/', view_login.logout_user, name = 'logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'listings.system_error.error400'
handler401 = 'listings.system_error.error401'
handler403 = 'listings.system_error.error403'
handler404 = 'listings.system_error.error404'
handler500 = 'listings.system_error.error500'
handler504 = 'listings.system_error.error504'
