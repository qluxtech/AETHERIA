import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="AELIA M2M Payment Gateway",
    version="1.0.0"
)

# ★フロントエンドからの通信を許可するCORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのドメインからのアクセスを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PAYMENT_WALLET_ADDRESS = "1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95"
PRICE_PER_REQUEST_SATS = 10

class AgentComputeRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.get("/")
def read_root():
    return {"status": "AELIA M2M Gateway Online", "protocol": "HTTP/402 Zero-Conf"}

@app.post("/api/v1/compute")
async def process_agent_task(request: Request, body: AgentComputeRequest):
    payment_proof = request.headers.get("X-M2M-Payment-Proof")
    
    if not payment_proof:
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "error": "Payment Required",
                "message": "This endpoint requires micro-settlement.",
                "price_sats": PRICE_PER_REQUEST_SATS,
                "pay_to_address": PAYMENT_WALLET_ADDRESS,
                "protocol": "BSV-ZeroConf"
            }
        )
    
    return {
        "status": "success",
        "processed_prompt": f"AELIA-OPTIMIZED: {body.prompt}",
        "charged_sats": PRICE_PER_REQUEST_SATS
    }
