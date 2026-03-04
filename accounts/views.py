from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from .utils import check_trophies

class MyLoginView(LoginView):
    """
    ログイン処理は標準のLoginViewに任せる。
    ログイン後の処理（トロフィー判定など）は signals.py の user_logged_in で実行されるため、
    ここで重ねて実行する必要はない。
    """
    pass

@login_required
def dashboard(request):
    # sessionから通知を取り出す（取得したら削除される）
    new_trophies = request.session.pop('trophy_notification', [])
    return render(request, 'dashboard.html', {'new_trophies': new_trophies})

@never_cache
@login_required
def check_trophies_api(request):
    """
    非同期でトロフィー判定を行うAPI
    結果はセッション 'trophy_notification' に格納される
    """
    try:
        user = request.user
        new_trophies = check_trophies(user)
        
        if new_trophies:
            # Dashboardで表示するためにsessionに保存
            current = request.session.get('trophy_notification', [])
            for t in new_trophies:
                current.append({
                    'name': t.name,
                    'description': t.description,
                    'icon': t.icon
                })
            request.session['trophy_notification'] = current
        
        return JsonResponse({'status': 'success', 'count': len(new_trophies)})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

