"""NDLサーチの簡易検索相当のキーワード検索。書籍本文の全文検索ではない。"""

import json
from datetime import datetime
from pathlib import Path

import requests
import xmltodict


# 公式仕様: https://ndlsearch.ndl.go.jp/help/api/specifications
MAX_RESULTS = 20


def main(query):
    response = requests.get(
        "https://ndlsearch.ndl.go.jp/api/opensearch",
        params={"any": query, "cnt": MAX_RESULTS},
        timeout=30,
    )
    response.raise_for_status()
    return xmltodict.parse(response.content, disable_entities=True)


def save_result(query, result):
    output_dir = Path(__file__).resolve().parent / "results" / "ndl_search"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = output_dir / f"ndl_search_{timestamp}.json"
    record = {
        "query": query,
        "search_parameters": {"any": query, "cnt": MAX_RESULTS},
        "response": result,
    }
    with output_path.open("x", encoding="utf-8") as file:
        json.dump(record, file, ensure_ascii=False, indent=2)
        file.write("\n")
    return output_path


def show_candidates(result):
    channel = result.get("rss", {}).get("channel", {})
    items = channel.get("item") or []
    # XMLのitemは1件だと辞書、複数件だとリストになる。
    if isinstance(items, dict):
        items = [items]
    print(f"ヒット件数: {channel.get('openSearch:totalResults', '不明')}")
    print(f"今回取得した候補: {len(items)}件")
    for index, item in enumerate(items, start=1):
        print(f"\n{index}. {item.get('title', '書名なし')}")
        print("著者:", item.get("author") or item.get("dc:creator") or "情報なし")
        print("件名・分類:", item.get("dc:subject") or "情報なし")
        print("資料種別:", item.get("category") or "情報なし")
        print("説明・注記:", item.get("dc:description") or "情報なし")
        print("詳細URL:", item.get("link") or "情報なし")


if __name__ == "__main__":
    while True:
        query_input = input("検索語（終了: q） >>>").strip()
        if query_input.lower() == "q":
            break
        if not query_input:
            continue
        try:
            result = main(query_input)
        except requests.RequestException as error:
            print(f"通信に失敗しました: {error}")
            continue
        output_path = save_result(query_input, result)
        show_candidates(result)
        print(f"\n保存先: {output_path}")
