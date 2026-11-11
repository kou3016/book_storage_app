import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

def main(isbn):
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={
            "q": f"isbn:{isbn}",
            "key": os.environ["GOOGLE_BOOKS_API_KEY"],
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def save_result(isbn, result):
    output_dir = Path(__file__).resolve().parent / "results" / "google_books_api"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名にはISBNの数字とチェック文字Xだけを使う。
    isbn_digits = "".join(char for char in isbn if char in "0123456789Xx")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = output_dir / f"googlebooks_isbn_{isbn_digits}_{timestamp}.json"

    with output_path.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write("\n")

    return output_path


if __name__ == "__main__":
    while True:
        isbn_input = input("input ISBN >>>").strip()
        result = main(isbn_input)
        print(result)
        output_path = save_result(isbn_input, result)
        print(f"保存先: {output_path}")
