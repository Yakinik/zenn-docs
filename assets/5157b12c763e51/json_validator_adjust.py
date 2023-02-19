import zipfile
import json
import jsonschema
import sys

# JSON Schema
schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "period": {"type": "string"},
        "artist": {"type": "string"},
        "trackList": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "date": {"type": "integer"},
                    "bpm": {"type": "integer"}
                },
                "required": ["name", "date", "bpm"]
            }
        }
    },
    "required": ["period", "artist", "trackList"]
}

# Zipファイル内を再帰的に探す関数


def search_zip(zip, path):
    for name in zip.namelist():
        # フォルダはスキップ
        if name.endswith('/'):
            continue
        # JSONファイルかチェック
        if name.endswith('.json'):
            try:
                # JSONを読み込んでスキーマチェック
                with zip.open(name) as f:
                    data = json.load(f)
                    jsonschema.validate(data, schema)
            except (json.JSONDecodeError, jsonschema.exceptions.ValidationError) as e:
                # エラー内容を表示
                if hasattr(e, 'path'):
                    print(f'{path}/{name} [{e.path}]: {e}')
                else:
                    print(f'{path}/{name}: {e}')


# Zipファイルを指定されたパスから読み込み
zip_path = sys.argv[1]
with zipfile.ZipFile(zip_path) as zip:
    search_zip(zip, zip_path)
