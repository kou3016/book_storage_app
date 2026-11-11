"""キーワード検索で推薦候補を探す検証用。推薦や条件の自動解釈は行わない。"""

import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")

# 取得候補数。画面に推薦する冊数とは別の設定。
MAX_RESULTS = 20


def main(query):
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={
            "q": query,
            "key": os.environ["GOOGLE_BOOKS_API_KEY"],
            "langRestrict": "ja",
            "printType": "books",
            "orderBy": "relevance",
            "maxResults": MAX_RESULTS,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def save_result(query, result):
    output_dir = Path(__file__).resolve().parent / "results" / "google_books_search"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = output_dir / f"googlebooks_search_{timestamp}.json"
    # 比較時に検索条件を確認できるよう、APIキーを除く条件と生の応答を保存。
    record = {
        "query": query,
        "search_parameters": {
            "langRestrict": "ja",
            "printType": "books",
            "orderBy": "relevance",
            "maxResults": MAX_RESULTS,
        },
        "response": result,
    }
    with output_path.open("x", encoding="utf-8") as file:
        json.dump(record, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return output_path


def show_candidates(result):
    items = result.get("items", [])
    print(f"今回取得した候補: {len(items)}件")
    for index, item in enumerate(items, start=1):
        info = item.get("volumeInfo", {})
        print(f"\n{index}. {info.get('title', '書名なし')}")
        print("著者:", ", ".join(info.get("authors", [])) or "情報なし")
        print("分類:", ", ".join(info.get("categories", [])) or "情報なし")
        identifiers = info.get("industryIdentifiers", [])
        print("識別子:", ", ".join(
            f"{entry.get('type')}: {entry.get('identifier')}"
            for entry in identifiers
        ) or "情報なし")
        print("紹介文:", info.get("description") or "情報なし")


if __name__ == "__main__":
    while True:
        query_input = input("検索語（終了: q） >>>").strip()
        if query_input.lower() == "q":
            break
        if not query_input:
            continue
        try:
            result = main(query_input)
        except KeyError:
            print(".envにGOOGLE_BOOKS_API_KEYを設定してください。")
            break
        except requests.HTTPError as error:
            # 例外全文にはAPIキー入りのURLが含まれるため表示しない。
            print(f"HTTPエラー: {error.response.status_code}")
            continue
        except requests.RequestException:
            print("通信に失敗しました。接続を確認して再実行してください。")
            continue
        except ValueError:
            print("APIの応答をJSONとして読み取れませんでした。")
            continue
        output_path = save_result(query_input, result)
        show_candidates(result)
        print(f"\n保存先: {output_path}")
