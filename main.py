import os
import json
import logging
import mimetypes
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from mcp.types import (
    JSONRPCMessage,
    JSONRPCResponse,
    JSONRPCError,
    ErrorData,
    RequestId,
    ListResourcesRequest,
    ListResourcesResult,
    Resource,
)
from pydantic import BaseModel
import uvicorn

# 環境変数の読み込み
load_dotenv()

# 設定
ROOT_PATH = os.getenv('ROOT_PATH', str(Path.home() / 'mcp_search'))
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5001))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ロギングの設定
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP Provider", description="Media Control Protocol Provider for file system access")

class JSONRPCRequest(BaseModel):
    jsonrpc: str
    method: str
    params: dict
    id: Any

def create_error_response(id: Any, code: int, message: str, data: Any = None) -> Dict:
    """JSONRPCエラーレスポンスを作成する"""
    error = {
        "jsonrpc": "2.0",
        "id": id,
        "error": {
            "code": code,
            "message": message
        }
    }
    if data:
        error["error"]["data"] = data
    return error

async def list_resources() -> List[Dict]:
    """ファイルリソースの一覧を取得する"""
    files = []
    root_path = Path(ROOT_PATH)
    
    if not root_path.exists():
        raise FileNotFoundError(f"検索対象ディレクトリが存在しません: {ROOT_PATH}")
        
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            try:
                rel_path = file_path.relative_to(root_path)
                normalized_path = str(rel_path).replace("\\", "/")
                mime_type, _ = mimetypes.guess_type(str(file_path))
                
                files.append({
                    "uri": f"file:///{normalized_path}",
                    "name": file_path.name,
                    "mimeType": mime_type or "application/octet-stream"
                })
            except Exception as e:
                logger.error(f"ファイル処理中のエラー: {file_path.name} - {str(e)}")
                continue
    
    return files

@app.on_event("startup")
async def startup_event():
    """サーバー起動時の初期化処理"""
    logger.info("✅ MCP Custom Server 起動中...")
    logger.info(f"📁 検索対象ディレクトリ: {ROOT_PATH}")
    if not os.path.exists(ROOT_PATH):
        logger.warning(f"⚠️ 検索対象ディレクトリが存在しません: {ROOT_PATH}")
        os.makedirs(ROOT_PATH, exist_ok=True)
        logger.info(f"📁 検索対象ディレクトリを作成しました: {ROOT_PATH}")

@app.post("/")
async def handle_jsonrpc(request: Request):
    """JSONRPCリクエストを処理する"""
    try:
        data = await request.json()
        logger.info(f"受信したリクエスト: {data}")
        
        # リクエストのバリデーション
        try:
            rpc_request = JSONRPCRequest(**data)
        except Exception as e:
            return JSONResponse(
                content=create_error_response(data.get("id", 0), -32600, "Invalid Request"),
                media_type="application/json"
            )

        # メソッドの処理
        if rpc_request.method == "resources/list":
            try:
                files = await list_resources()
                return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "id": rpc_request.id,
                        "result": {
                            "resources": files
                        }
                    },
                    media_type="application/json"
                )
            except Exception as e:
                logger.error(f"ファイル一覧取得中のエラー: {str(e)}")
                return JSONResponse(
                    content=create_error_response(rpc_request.id, -32603, "Internal error", str(e)),
                    media_type="application/json"
                )

        # 未対応メソッド
        logger.warning(f"未対応のメソッド: {rpc_request.method}")
        return JSONResponse(
            content=create_error_response(rpc_request.id, -32601, "Method not found"),
            media_type="application/json"
        )

    except Exception as e:
        logger.error(f"サーバーエラー: {str(e)}")
        return JSONResponse(
            content=create_error_response(0, -32603, "Internal error", str(e)),
            media_type="application/json"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
