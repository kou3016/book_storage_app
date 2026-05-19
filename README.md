# Book Storage App

Spring Boot + MySQL で作成した本管理アプリです。  
本の登録、一覧表示、詳細表示、更新、削除、検索ができます。

## Tech Stack

- Java 26
- Spring Boot 4.x
- Spring Data JPA
- Thymeleaf
- MySQL 8 (Docker)
- Gradle (Wrapper)

## Project Structure

- `src/main/java/com/example/demo` : アプリ本体
- `src/main/java/com/example/demo/book` : 本機能（Controller / Service / Repository / Entity）
- `src/main/resources/templates` : 画面テンプレート
- `script/init.sql` : DB初期化SQL

## Setup

### 1. MySQL 起動

プロジェクトルート（`book_storage_app`）で実行:

```bash
docker compose up -d
docker exec -it book_shelves mysql -uuser -pbookapp --default-character-set=utf8mb4 book_app
```

### 2. DB 初期化

`script/init.sql` が初回起動時に適用されます。  
既存ボリュームを消して再初期化したい場合:

```bash
docker compose down -v
docker compose up -d
```

### 3. アプリ起動

`demo` ディレクトリで実行:

```powershell
cd C:\Users\~~~\book_storage_app\demo
.\gradlew.bat bootRun
```

## Access URLs

- Book List: `http://localhost:8080/books`
- Register: `http://localhost:8080/books/register`

## Features

- 本データ登録
- 本データ一覧表示
- 本データ詳細表示
- 本データ更新
- 本データ削除（一覧画面から）
- 検索（ID / Title / Author）
  - ID: 完全一致
  - Title / Author: 前方一致（`keyword%`）

## Search Spec

検索フォームは `type` と `keyword` を送信します。

- `type=id` : ID検索
- `type=title` : タイトル前方一致
- `type=author` : 著者前方一致

## Useful Commands

```powershell
.\gradlew.bat compileJava
.\gradlew.bat test
.\gradlew.bat clean build
.\gradlew.bat bootRun
```

## Future Improvements

- DTO 分離（Entity 直返し解消）
- バリデーション強化
- 例外ハンドリングの共通化
- レビュー機能 / 読書ログ機能の追加
