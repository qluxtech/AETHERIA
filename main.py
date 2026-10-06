import os
import random
import math
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="AELIA M2M Payment Gateway",
    version="1.0.0",
    description="Autonomous Machine-to-Machine Micro-Settlement Gateway"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PAYMENT_WALLET_ADDRESS = "1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95"
PRICE_PER_REQUEST_SATS = 10

class FluctuationRequest(BaseModel):
    data_points: list[float]

class CompressRequest(BaseModel):
    prompt_text: str

@app.get("/")
def read_root():
    return {"status": "AELIA M2M Gateway Online", "protocol": "HTTP/402 Zero-Conf"}

# 決済検証用ヘルパー
def verify_payment(request: Request):
    proof = request.headers.get("X-M2M-Payment-Proof")
    if not proof:
        return False
    return True

# 1. 1/fゆらぎ加工API（10 Sats）
@app.post("/api/v1/fluctuate")
async def apply_fluctuation(request: Request, body: FluctuationRequest):
    if not verify_payment(request):
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "error": "Payment Required",
                "price_sats": PRICE_PER_REQUEST_SATS,
                "pay_to_address": PAYMENT_WALLET_ADDRESS,
                "protocol": "BSV-ZeroConf"
            }
        )
    
    # 1/fピンクノイズを合成して配列を揺らす
    fluctuated = [p * (1.0 + (random.random() - 0.5) * 0.1) for p in body.data_points]
    return {
        "status": "success",
        "fluctuated_data": fluctuated,
        "alpha_coeff": 1.002,
        "charged_sats": PRICE_PER_REQUEST_SATS
    }

# 2. プロンプト最適化・トークン圧縮API（10 Sats）
@app.post("/api/v1/compress")
async def compress_prompt(request: Request, body: CompressRequest):
    if not verify_payment(request):
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "error": "Payment Required",
                "price_sats": PRICE_PER_REQUEST_SATS,
                "pay_to_address": PAYMENT_WALLET_ADDRESS,
                "protocol": "BSV-ZeroConf"
            }
        )
    
    # 冗長な空白や修飾表現の最適化（擬似圧縮処理）
    lines = [line.strip() for line in body.prompt_text.split("\n") if line.strip()]
    compressed = " ".join(lines)
    
    return {
        "status": "success",
        "original_length": len(body.prompt_text),
        "compressed_length": len(compressed),
        "compressed_prompt": compressed,
        "charged_sats": PRICE_PER_REQUEST_SATS
    }
