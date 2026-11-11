import json
from datetime import datetime
from pathlib import Path

import requests
import xmltodict


# 参考ブログ: https://qiita.com/yknm1989/items/f77d22e1c7f1347d79b0
# 現行API仕様: https://ndlsearch.ndl.go.jp/help/api/specifications
def main(isbn):
    response = requests.get(
        "https://ndlsearch.ndl.go.jp/api/opensearch",
        params={"isbn": isbn},
        timeout=30,
    )
    response.raise_for_status()
    # XMLを辞書に変換する。属性・名前空間・複数の検索結果も保持する。
    return xmltodict.parse(response.content, disable_entities=True)


def save_result(isbn, result):
    output_dir = Path(__file__).resolve().parent / "results" / "ndl_api"
    output_dir.mkdir(parents=True, exist_ok=True)
    isbn_digits = "".join(char for char in isbn if char in "0123456789Xx")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = output_dir / f"ndl_isbn_{isbn_digits}_{timestamp}.json"

    with output_path.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return output_path


if __name__ == "__main__":
    while True:
        isbn_input = input("input ISBN >>>").strip().replace("-", "")
        if len(isbn_input) != 13 or not all(char in "0123456789" for char in isbn_input):
            print("ISBNは13桁の数字で入力してください。")
            continue
        result = main(isbn_input)
        print(result)
        output_path = save_result(isbn_input, result)
        print(f"保存先: {output_path}")
