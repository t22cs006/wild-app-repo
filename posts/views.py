from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .models import Post
from django.utils import timezone
import json
from wildlife.constants import GRID_SIZE, MIN_LAT, MIN_LON, MAX_LAT, MAX_LON, CENTER_LAT, CENTER_LON
from .utils import get_random_species
from accounts.utils import check_trophies
from accounts.models import UserProfile
from .forms import PostTimeForm
import math

User = get_user_model()

# 管理者だけアクセス可能
def admin_only(user):
    return user.is_staff or user.is_superuser


# def calc_grid(lat, lon): 
#     gx = int((lon - MIN_LON) // GRID_SIZE) 
#     gy = int((lat - MIN_LAT) // GRID_SIZE) 
#     return gx, gy

def latlon_to_grid(lat, lon):
    gx = math.floor((lon - MIN_LON) / GRID_SIZE)
    gy = math.floor((lat - MIN_LAT) / GRID_SIZE)
    return gx, gy



@login_required
def create_post(request):
    # GET パラメータから緯度経度を取得（あればフォームに初期値として渡す）
    lat = request.GET.get("lat") 
    lon = request.GET.get("lon") 
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            # 保存前にインスタンスを取得
            post = form.save(commit=False)
            post.user = request.user
            post.source = "manual"
            present = post.presence
            species = post.species

            # 動物種の判定（Demo: 実際はAI等で判定する場所）
            if(species == "不明" and present == "present"):
                # 現状は判定せず "不明" のままにする（将来的に画像認識などを実装）
                species = get_random_species() # 名前はそのままAI判定関数のプレースホルダー
                post.species = species
                
                # もし将来 "クマ" が検出されたら "レア個体" にする例
                # if species == "クマ":
                #     post.species = "レア個体"

            # グリッド計算
            gx, gy = latlon_to_grid(post.lat, post.lon)
            post.gx = gx
            post.gy = gy

            # timestamp（time_mode に応じて）
            post.timestamp = form.cleaned_data["timestamp"]

            # 保存
            post.save()

            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            
            # --- カウント更新 ---
            # 1. 出現/不在
            if present == "present":
                profile.present_count += 1
            else:
                profile.absent_count += 1
            
            # 2. レア個体
            if species == "レア個体":
                profile.rare_found += 1

            # 3. 未開拓地＆久しぶり判定用ロジック
            # この投稿を除いた、同じグリッドの過去投稿を取得
            match_grid_posts = Post.objects.filter(gx=gx, gy=gy).exclude(id=post.id)
            
            # (A) 未開拓エリア (投稿数がこの投稿を含めても6件以下 = 過去分が5件以下)
            if match_grid_posts.count() <= 5:
                profile.pioneer_count += 1

            # (B) 1ヶ月以上投稿なし (リバイバル)
            # 直近1ヶ月以内の投稿があるかチェック
            one_month_ago = timezone.now() - timezone.timedelta(days=30)
            if not match_grid_posts.filter(timestamp__gte=one_month_ago).exists():
                profile.revival_count += 1

            profile.save()

            new_trophies = check_trophies(request.user)
            trophy_list = []
            if new_trophies:
                trophy_list = [{'name': t.name, 'description': t.description, 'icon': t.icon} for t in new_trophies]

            # success 画面に渡すデータを session に保存
            request.session["post_result"] = {
                "gx": gx,
                "gy": gy,
                "lat": post.lat,
                "lon": post.lon,
                "presence": post.presence,
                "timestamp": str(post.timestamp),
                "species": post.species,
                "new_trophies": trophy_list,
            }

            return redirect("post_result")  # URL 名はあなたの設定に合わせて

    else: # ★ GET のときだけ lat/lon を初期値としてフォームに入れる 
        if lat and lon: 
            form = PostForm(initial={"lat": lat, "lon": lon}) 
        else: 
            form = PostForm()

    grid_rows = math.floor((MAX_LAT - MIN_LAT) / GRID_SIZE)
    grid_cols = math.floor((MAX_LON - MIN_LON) / GRID_SIZE)


    return render(request, "posts/create_post.html", {"form": form, 
        'CENTER_LAT': CENTER_LAT,
        'CENTER_LON': CENTER_LON,
        'GRID_SIZE': GRID_SIZE,
        'GRID_ROWS': grid_rows,
        'GRID_COLS': grid_cols,
        'MIN_LAT': MIN_LAT,
        'MAX_LAT': MAX_LAT,
        'MIN_LON': MIN_LON,
        'MAX_LON': MAX_LON,
        'lat': lat if lat else "",
        'lon': lon if lon else "",
    })


@login_required
def post_result(request):
    data = request.session.pop("post_result", None)

    # 直アクセス防止
    if not data:
        return redirect("posts:create")
    
    data["MIN_LAT"] = MIN_LAT 
    data["MIN_LON"] = MIN_LON

    return render(request, "posts/post_result.html", data)

@login_required
def bulk_absent(request):
    if request.method != "POST":
        return redirect("dashboard")

    # ① フォーム（時刻入力）
    time_form = PostTimeForm(request.POST)
    if not time_form.is_valid():
        return render(request, "posts/bulk_error.html", {"errors": time_form.errors})

    timestamp = time_form.get_timestamp()

    # ② フロントから送られたポイント一覧
    #    [{lat, lon, gx, gy}, ...]
    try:
        points = json.loads(request.POST.get("points", "[]"))
    except:
        return render(request, "posts/bulk_error.html", {"errors": ["不正なデータ形式です"]})

    if not points:
        return render(request, "posts/bulk_error.html", {"errors": ["ポイントが選択されていません"]})

    created_posts = []
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    for p in points:
        lat = p["lat"]
        lon = p["lon"]
        gx = p["gx"]
        gy = p["gy"]

        # ③ Post インスタンス作成
        post = Post(
            user=request.user,
            source="bulk",
            presence="absent",
            species="不明",
            lat=lat,
            lon=lon,
            gx=gx,
            gy=gy,
            timestamp=timestamp,
        )

        post.save()
        created_posts.append(post)

        # ④ プロフィール更新
        profile.absent_count += 1

    # ⑤ プロフィール保存
    profile.save()

    # ⑥ トロフィー判定（1回だけ）
    new_trophies = check_trophies(request.user)
    trophy_list = []
    if new_trophies:
        trophy_list = [{'name': t.name, 'description': t.description, 'icon': t.icon} for t in new_trophies]

    # ⑦ 結果画面へ
    request.session["bulk_success"] = {
        "count": len(created_posts),
        "points": [
            {"gx": p.gx, "gy": p.gy, "lat": p.lat, "lon": p.lon}
            for p in created_posts
        ],
        "timestamp": str(timestamp),
        "new_trophies": trophy_list,
    }

    return redirect("bulk_success")

@login_required
def bulk_success(request):
    data = request.session.get("bulk_success")
    if not data:
        return redirect("dashboard")
    return render(request, "posts/bulk_success.html", data)



@user_passes_test(admin_only)
def batch_post_view(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        presence = request.POST.get("presence")
        timestamp = request.POST.get("timestamp")
        image = request.FILES.get("image")
        grid_data = request.POST.get("grids")  # JSON 文字列

        grids = json.loads(grid_data)  # [{lat:..., lon:...}, ...]

        user = User.objects.get(id=user_id)
        # プロフィールを確実に取得
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # カウント用変数
        present_count = 0
        absent_count = 0
        rare_count = 0

        for g in grids:
            gx, gy = latlon_to_grid(g["lat"], g["lon"])
            # species = get_random_species() # バッチ投稿ではランダムやめる
            species = "不明"

            # 画像がある場合、シーク位置をリセットして再利用可能にする
            if image:
                image.seek(0)

            Post.objects.create(
                user=user,
                presence=presence,
                image=image if presence == "present" else None,
                timestamp=timestamp,      # ← 手動入力の日時をそのまま入れる
                time_mode="manual",  
                lat=g["lat"],
                lon=g["lon"],
                gx=gx,
                gy=gy,
                source="manual",
                species=species,
            )
            if presence == "present":
                present_count += 1
                if species == "レア個体":
                    rare_count += 1
            else:
                absent_count += 1

        # profile更新
        # 再取得せず、上で取得したオブジェクトを使う
        profile.present_count += present_count
        profile.absent_count += absent_count
        profile.rare_found += rare_count
        profile.save()

        # トロフィーチェック
        check_trophies(user)

        return redirect("batch_post_success")

    users = User.objects.all()
    return render(request, "posts/batch_post.html", {"users": users,
        'CENTER_LAT': CENTER_LAT,
        'CENTER_LON': CENTER_LON,
        'GRID_SIZE': GRID_SIZE,
        'MIN_LAT': MIN_LAT,
        'MAX_LAT': MAX_LAT,
        'MIN_LON': MIN_LON,
        'MAX_LON': MAX_LON,
    })


@user_passes_test(admin_only)
def batch_post_success(request):
    return render(request, "posts/batch_post_success.html")