from django import forms
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
    manual_timestamp = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    # ★ species をフォーム側で追加（レア個体は含めない）
    species = forms.ChoiceField(
        choices=[
            ("タヌキ", "タヌキ"),
            ("キツネ", "キツネ"),
            ("シカ", "シカ"),
            ("イノシシ", "イノシシ"),
            ("サル", "サル"),
            ("クマ", "クマ"),
            ("ハクビシン", "ハクビシン"),
            ("不明", "わからない"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "species-select"})
    )

    class Meta:
        model = Post
        fields = [
            "presence",
            "species",          # ← 追加
            "image",
            "time_mode",
            "manual_timestamp",
            "lat",
            "lon",
        ]
        widgets = {
            "presence": forms.RadioSelect,
            "time_mode": forms.RadioSelect,
            # ★ カメラ起動/ファイル選択の両対応 (ユーザビリティ重視)
            "image": forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean(self):
        cleaned = super().clean()

        presence = cleaned.get("presence")
        species = cleaned.get("species")
        time_mode = cleaned.get("time_mode")
        manual_timestamp = cleaned.get("manual_timestamp")

        # ★ presence = present → species 必須
        if presence == "present" and not species:
            self.add_error("species", "『いた』を選んだ場合は動物種を選択してください。")

        # ★ presence = absent → species を空にする
        if presence == "absent":
            cleaned["species"] = None

        # time_mode = manual → manual_timestamp 必須
        if time_mode == "manual":
            if not manual_timestamp:
                self.add_error("manual_timestamp", "手動入力の日時を指定してください。")
            else:
                cleaned["timestamp"] = manual_timestamp

        # time_mode = auto → timestamp を現在時刻に
        if time_mode == "auto":
            from django.utils import timezone
            cleaned["timestamp"] = timezone.now()

        return cleaned

class PostTimeForm(forms.Form):
    TIME_MODE_CHOICES = [
        ("auto", "現在時刻を使う"),
        ("manual", "手動で入力する"),
    ]

    time_mode = forms.ChoiceField(
        choices=TIME_MODE_CHOICES,
        widget=forms.RadioSelect,
        initial="auto"
    )

    manual_timestamp = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    def clean(self):
        cleaned = super().clean()

        time_mode = cleaned.get("time_mode")
        manual_timestamp = cleaned.get("manual_timestamp")

        # manual → manual_timestamp 必須
        if time_mode == "manual":
            if not manual_timestamp:
                self.add_error("manual_timestamp", "手動入力の日時を指定してください。")
            else:
                cleaned["timestamp"] = manual_timestamp

        # auto → 現在時刻
        if time_mode == "auto":
            cleaned["timestamp"] = timezone.now()

        return cleaned

    def get_timestamp(self):
        """view で使う：cleaned_data から timestamp を返す"""
        return self.cleaned_data["timestamp"]
