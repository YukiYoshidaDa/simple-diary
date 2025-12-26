# Simple Diary

Flask (Backend) と React + Vite (Frontend) を組み合わせたフルスタック SNS アプリケーションです。

## 1. プロジェクト概要

このプロジェクトは、ユーザー管理、日記の投稿、パーソナライズされた設定などの機能を提供するモダンな SNS アプリケーションです。

- **Backend**: Python (Flask) をベースに、クリーンなレイヤー設計（Router, Service, Model, Schema）を採用。高いテスト性と拡張性を備えています。
- **Frontend**: React + Vite による高速な開発環境を構築。現在は基盤構築（スキャフォールド）段階にあり、今後リッチな UI/UX を展開していくための柔軟な土台を整えています。

## 2. ディレクトリ構成

```text
simple-diary/
├── backend/
│   ├── app.py              # Flask アプリケーションのファクトリー
│   ├── config.py           # 環境ごとの設定管理（dev/testing/prod）
│   ├── Dockerfile          # 開発・本番用 Docker イメージ
│   ├── Dockerfile.test     # テスト専用 Docker イメージ
│   ├── requirements.txt    # 実行に必要なライブラリ
│   ├── requirements-dev.txt # テスト・開発用ライブラリ（requirements.txt を含む）
│   ├── models/             # SQLAlchemy のデータモデル（DB定義）
│   ├── services/           # ビジネスロジック（データの加工、検証）
│   ├── routers/            # API エンドポイントの定義（Blueprint）
│   ├── schemas/            # Marshmallow による検証と変換
│   └── tests/              # pytest によるテストコード群
│       └── conftest.py     # テスト用フィクスチャ（共通設定）
├── frontend/               # React（Vite）フロントエンド
└── docker-compose.yml      # 全体のオーケストレーション
```

## 3. 開発環境の構築方法

docker compose を使用して、バックエンド、フロントエンド、データベースを一括で起動できます。

```bash
# プロジェクトルートで実行
docker compose up --build
```

- **Backend (API)**: `http://localhost:5001/api`
- **Frontend**: `http://localhost:5173`
- **MySQL (DB)**: `localhost:3306`

## 4. テスト環境の実行方法

本プロジェクトでは、Docker コンテナ内で **pytest** を実行し、**SQLite (in-memory)** を使用して高速かつ、開発環境に影響を与えない独立したテストを行います。

### 実行手順

1. **テストイメージのビルド**
   ```bash
   docker build -t diary-backend-test -f backend/Dockerfile.test backend
   ```

2. **テストの実行**
   ```bash
   docker run --rm diary-backend-test
   ```

### 依存関係の分離（Dockerfile.test の役割）
本番用イメージを軽量かつ安全に保つため、依存関係を分離しています。
- **requirements.txt**: 実行に必要な最小限のパッケージ。
- **requirements-dev.txt**: テスト・開発のみで使用するパッケージ一式。
`Dockerfile.test` はこれらを包含したテスト専用の実行環境を提供します。

### 設計のポイント（こだわり）

- **環境の自動切り替え**: `FLASK_ENV=testing` を検知すると、`config.py` が動的に `sqlite:///:memory:` を選択するように設計されています。これにより、外部 DB（MySQL）の状態に関わらず、常にクリーンな状態でテストを開始できます。
- **自動スキーマ管理**: `tests/conftest.py` 内の `db` フィクスチャに `autouse=True` を設定しています。各テストケースの実行直前にテーブルを自動生成し、終了後にクリーンアップを行うことで、テスト間の干渉を完全に排除しています。
- **確実なモジュールインポート**: コンテナ環境の `PYTHONPATH` を `/app` に固定することで、アプリケーションルート配下のモジュール（`app`, `services`, `models` 等）を階層に関わらず安全にインポートできる構成にしています。
