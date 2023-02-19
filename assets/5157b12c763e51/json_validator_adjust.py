import zipfile
import json
import jsonschema
import sys

# テスト基準となるJSONスキーマ
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
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


# Zipファイル内の全てのJSONファイルに対して実行
with zipfile.ZipFile(sys.argv[1], 'r') as z:
    for filename in z.namelist():
        # JSONファイルのみ対象
        if not filename.endswith('.json'):
            continue

        # JSONファイルを読み込み
        with z.open(filename) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f'{filename}: JSONDecodeError: {e}')
                continue

        # スキーマと比較
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            print(f'{filename} [{e.relative_path[0]}]: {e}')
