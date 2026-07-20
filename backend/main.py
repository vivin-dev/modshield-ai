from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ModShield AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    logger.info("✅ Supabase connected")
except Exception as e:
    logger.error(f"❌ Supabase connection failed: {e}")

class MetricData(BaseModel):
    guild_id: str
    messages_analyzed: int
    flagged_toxic: int
    warnings_issued: int
    burnout_score: float

class ToxicityScore(BaseModel):
    guild_id: str
    user_id: str
    message_id: str
    content: str
    score: float
    reason: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/metrics")
async def receive_metrics(data: MetricData):
    try:
        guild = supabase.table("guilds").select("id").eq("discord_guild_id", data.guild_id).execute()
        
        if not guild.data:
            guild = supabase.table("guilds").insert({"discord_guild_id": data.guild_id}).execute()
            guild_uuid = guild.data[0]["id"]
        else:
            guild_uuid = guild.data[0]["id"]
        
        supabase.table("mod_metrics").insert({
            "guild_id": guild_uuid,
            "total_messages_analyzed": data.messages_analyzed,
            "flagged_messages_count": data.flagged_toxic,
            "warnings_issued": data.warnings_issued,
            "burnout_score": data.burnout_score
        }).execute()
        
        logger.info(f"✅ Metrics stored for guild {data.guild_id}")
        return {"success": True}
    except Exception as e:
        logger.error(f"❌ Error storing metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/toxicity-score")
async def log_toxicity_score(data: ToxicityScore):
    try:
        guild = supabase.table("guilds").select("id").eq("discord_guild_id", data.guild_id).execute()
        
        if not guild.data:
            guild = supabase.table("guilds").insert({"discord_guild_id": data.guild_id}).execute()
            guild_uuid = guild.data[0]["id"]
        else:
            guild_uuid = guild.data[0]["id"]
        
        supabase.table("chat_messages").insert({
            "guild_id": guild_uuid,
            "discord_user_id": data.user_id,
            "discord_message_id": data.message_id,
            "content": data.content,
            "toxicity_score": data.score,
            "is_flagged": data.score > 0.7,
            "ai_reason": data.reason
        }).execute()
        
        return {"success": True, "flagged": data.score > 0.7}
    except Exception as e:
        logger.error(f"❌ Error logging toxicity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/{guild_id}")
async def get_dashboard_metrics(guild_id: str):
    try:
        guild = supabase.table("guilds").select("id").eq("discord_guild_id", guild_id).execute()
        
        if not guild.data:
            return {
                "messagesAnalyzed": 0,
                "flaggedToxic": 0,
                "actionsTaken": 0,
                "burnoutScore": 0
            }
        
        metrics = supabase.table("mod_metrics").select("*").eq("guild_id", guild.data[0]["id"]).order("date", desc=True).limit(1).execute()
        
        if metrics.data:
            return {
                "messagesAnalyzed": metrics.data[0]["total_messages_analyzed"],
                "flaggedToxic": metrics.data[0]["flagged_messages_count"],
                "actionsTaken": metrics.data[0]["warnings_issued"],
                "burnoutScore": metrics.data[0]["burnout_score"]
            }
        
        return {"messagesAnalyzed": 0, "flaggedToxic": 0, "actionsTaken": 0, "burnoutScore": 0}
    except Exception as e:
        logger.error(f"❌ Error fetching dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recent-messages/{guild_id}")
async def get_recent_messages(guild_id: str, limit: int = 20):
    try:
        guild = supabase.table("guilds").select("id").eq("discord_guild_id", guild_id).execute()
        
        if not guild.data:
            return []
        
        response = supabase.table("chat_messages").select("*").eq("guild_id", guild.data[0]["id"]).eq("is_flagged", True).order("created_at", desc=True).limit(limit).execute()
        
        return response.data
    except Exception as e:
        logger.error(f"❌ Error fetching messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
