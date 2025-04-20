# tsuki_mcp_filesystem_server
**MCPファイルプロバイダー**

A custom MCP-compatible server for searching local filesystem files. Works with OpenAI's Agent SDK via the resources/list method.  ローカルファイルの検索を行う、自作のMCP対応サーバーです。 Agent SDK の `resources/list` に対応しています。

A custom server compatible with the **Model Context Protocol (MCP)**.  
Designed for integration with OpenAI's Agent SDK, it enables file search and open operations over the local filesystem.  
Model Context Protocol（MCP） に準拠したカスタムサーバーです。
OpenAIのAgent SDKとの統合を想定して設計されており、ローカルファイルシステム上のファイル検索やオープン操作が可能です。

---

## Features  
**特徴**

- Provides file system resources via MCP (supports file search and open operations)  
  ファイルシステムのリソースをMCP経由で提供（検索とファイルオープンに対応）  
- Automatic MIME type detection  
  MIMEタイプの自動検出  
- Flexible configuration via environment variables  
  環境変数による柔軟な設定  
- Supports JSON-RPC protocol  
  JSON-RPCプロトコルのサポート

---

## Installation  
**インストール**

```bash
# Clone the repository
git clone https://github.com/yuutotsuki/tsuki_mcp_filesystem_server.git
cd tsuki_mcp_filesystem_server

# Install dependencies
pip install -r requirements.txt
```

```bash
# リポジトリのクローン
git clone https://github.com/yuutotsuki/tsuki_mcp_filesystem_server.git
cd tsuki_mcp_filesystem_server

# 依存関係のインストール
pip install -r requirements.txt
```

---

## Configuration  
**設定**

1. Copy `.env.example` to `.env` and configure it:  
   `.env.example` を `.env` にコピーして設定を行います：

```bash
cp .env.example .env
```

2. Edit `.env` file as needed:  
   `.env` ファイルを編集して以下のように設定してください：

```env
ROOT_PATH=/path/to/your/search/directory  # Directory to be searched
HOST=127.0.0.1                            # Server host
PORT=5001                                 # Server port
LOG_LEVEL=INFO                            # Logging level (DEBUG / INFO / WARNING / ERROR)
```

---

## Usage  
**使用方法**

```bash
# Start the server
python main.py
```

```bash
# サーバーの起動
python main.py
```

The server will start on the specified host and port and wait for MCP client requests.  
サーバーは指定されたホストとポートで起動し、MCPクライアントからのリクエストを待ち受けます。

---

## API Endpoints  
**APIエンドポイント**

Currently supported methods:  
現在サポートされているメソッド：

- `resources/list`: Retrieves a list of files in the target directory  
  `resources/list`：指定されたディレクトリ内のファイル一覧を取得

---

## Development  
**開発**

If you'd like to contribute, please follow these guidelines:  
貢献したい方は、以下の点にご注意ください：

1. Follow [PEP 8](https://peps.python.org/pep-0008/) coding style  
   コードスタイルは PEP 8 に従ってください  
2. Add appropriate tests for new features  
   新機能を追加する場合は、適切なテストを作成してください  
3. Make sure all tests pass before submitting a pull request  
   プルリクエストを作成する前に、すべてのテストが通っていることを確認してください

---

## License  
**ライセンス**

MIT License  
MITライセンス

---

## Author  
**作者**

[yuutotsukitocu]  

---

## Contribution  
**貢献**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.  
プルリクエストは歓迎します。大きな変更を行う場合は、まず issue を作成して議論してください。

---
