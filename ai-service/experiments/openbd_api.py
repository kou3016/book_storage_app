import json
from datetime import datetime
from pathlib import Path

import requests


def main(isbn):
    response = requests.get(
        "https://api.openbd.jp/v1/get",
        params={"isbn": isbn},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def save_result(isbn, result):
    output_dir = Path(__file__).resolve().parent / "results" / "openbd_api"
    output_dir.mkdir(parents=True, exist_ok=True)
    isbn_digits = "".join(char for char in isbn if char in "0123456789Xx")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = output_dir / f"openbd_isbn_{isbn_digits}_{timestamp}.json"

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
