import os
import django
import json
from django.apps import apps
from django.core import serializers

# Django初期化
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polls.settings")  # プロジェクト名に合わせて変更
django.setup()

all_data = []

for model in apps.get_models():
    model_name = model.__name__
    app_label = model._meta.app_label

    # ログ系・履歴系など除外したいモデル（必要に応じて拡張）
    if app_label == "admin" or model_name in ["LogEntry"]:
        continue

    try:
        qs = model.objects.all()
        if qs.exists():
            serialized = serializers.serialize("json", qs)
            all_data.extend(json.loads(serialized))
    except Exception as e:
        print(f"[{model_name}] skipped: {e}")

# 保存
with open("data.json", "w", encoding="utf-8-sig") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
