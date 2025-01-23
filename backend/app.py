from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import subprocess
import os
import logging
import time
from tenacity import retry, wait_exponential, stop_after_attempt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/app/logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)

OUTPUT_DIR = "/app/output"

# Retry configuration
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_bash_code(prompt: str):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{
            "role": "user",
            "content": f"Generate bash code for: {prompt}. Return ONLY raw code, no markdown."
        }],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"→ INCOMING {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"💥 ERROR: {str(e)}")
        raise
    logger.info(f"← OUTGOING {response.status_code}")
    return response

@app.post("/generate_bash")
async def generate_bash(request: Request, payload: dict = Body(...)):
    try:
        prompt = payload.get("prompt", "")
        if not prompt:
            raise ValueError("Empty prompt")
        
        logger.info(f"Processing prompt: {prompt}")
        
        # Get and clean bash code
        bash_code = get_bash_code(prompt)
        
        # Remove markdown artifacts
        clean_lines = []
        for line in bash_code.split("\n"):
            stripped = line.strip()
            if stripped in ('```bash', '```') or stripped.startswith(('```bash', '```')):
                continue
            clean_lines.append(line)
        bash_code = "\n".join(clean_lines).strip('` \n')
        
        # Ensure shebang
        if not bash_code.startswith('#!/bin/bash'):
            bash_code = "#!/bin/bash\n" + bash_code
            
        # Generate filenames
        filename = f"script_{hash(prompt)}.sh"
        script_path = os.path.join(OUTPUT_DIR, filename)
        log_path = f"{script_path}.log"
        
        # Save script
        with open(script_path, "w") as f:
            f.write(bash_code)
        os.chmod(script_path, 0o755)
        
        # Execute script
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Save logs
        with open(log_path, "w") as f:
            f.write(f"PROMPT: {prompt}\n")
            f.write(f"STDOUT:\n{result.stdout}\n")
            f.write(f"STDERR:\n{result.stderr}\n")
            f.write(f"EXIT CODE: {result.returncode}\n")
        
        return {
            "status": "OK",
            "output_file": f"output/{os.path.basename(log_path)}"
        }
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return {"status": "ERROR", "error": str(e)}
