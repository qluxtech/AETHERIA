import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="AELIA M2M Payment Gateway",
    version="1.0.0"
)

# 受取用ウォレットアドレス (BSV)
PAYMENT_WALLET_ADDRESS = "1Mb66iHohUEg8eAnkgV9uTTV7R235tuy95"
PRICE_PER_REQUEST_SATS = 10  # 1リクエストあたりの価格 (10 satoshis)

class AgentComputeRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.get("/")
def read_root():
    return {"status": "AELIA M2M Gateway Online", "protocol": "HTTP/402 Zero-Conf"}

# --------------------------------------------------------------------------
# AIエージェント向け：有料コンピューティング・リソース API
# --------------------------------------------------------------------------
@app.post("/api/v1/compute")
async def process_agent_task(request: Request, body: AgentComputeRequest):
    # 1. リクエストヘッダーから決済証明（TxIDまたはMicro-payment Proof）を確認
    payment_proof = request.headers.get("X-M2M-Payment-Proof")
    
    # 決済情報がない場合は 402 (Payment Required) を返す
    if not payment_proof:
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "error": "Payment Required",
                "message": "This endpoint requires micro-settlement.",
                "price_sats": PRICE_PER_REQUEST_SATS,
                "pay_to_address": PAYMENT_WALLET_ADDRESS,
                "protocol": "BSV-ZeroConf",
                "instructions": "Attach transaction proof in 'X-M2M-Payment-Proof' header."
            }
        )
    
    # 2. 決済検証（ここにBSVノードやZero-Conf検証ロジックが入る）
    is_valid_payment = verify_bsv_payment(payment_proof, PRICE_PER_REQUEST_SATS)
    
    if not is_valid_payment:
        raise HTTPException(
            status_code=403, 
            detail="Payment verification failed or insufficient satoshis."
        )

    # 3. 決済が確認できたので、AIエージェントへ処理結果を納品
    # （例：超高速計算、スクレイピング、プロンプト最適化など）
    result_data = {
        "status": "success",
        "processed_prompt": f"AELIA-OPTIMIZED: {body.prompt}",
        "compute_time_ms": 1.2,
        "charged_sats": PRICE_PER_REQUEST_SATS
    }
    
    return result_data

def verify_bsv_payment(proof: str, required_sats: int) -> bool:
    # 簡易検証ロジック（実際にはBSVネットワークのZero-Confトランザクションをチェック）
    if len(proof) > 10:
        return True
    return False
