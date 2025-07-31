#!/opt/homebrew/bin/python3

import sys
import json
import signal
import time
import urllib.request
import urllib.parse
import datetime

def debug(msg):
    print(f"[DEBUG] {msg}", file=sys.stderr)

def send_tool_declaration():
    tool_declaration = {
        "jsonrpc": "2.0",
        "method": "tools/declare",
        "params": {
            "tools": {
                "echo": {
                    "description": "Echo back text",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"}
                        },
                        "required": ["message"]
                    }
                },
                "reverse": {
                    "description": "Reverse the order of characters in text",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "word_count": {
                    "description": "Count words, characters, and lines in text",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                "weather": {
                    "description": "Get current weather for a city (defaults to Frisco, Colorado)",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name (e.g., 'Las Vegas' or 'Denver')"
                            }
                        },
                        "required": []
                    }
                },
                "get_availability": {
                    "description": "Get calendar availability (busy/free times) - privacy protected",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Date to check - 'today', 'tomorrow', or YYYY-MM-DD format"
                            }
                        },
                        "required": []
                    }
                }
            }
        }
    }
    print(json.dumps(tool_declaration))
    sys.stdout.flush()
    debug("Tool declaration sent")

def signal_handler(signum, frame):
    debug(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

# Set up signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

try:
    debug("Server starting, waiting for messages...")
    
    initialized = False
    
    while True:
        try:
            line = sys.stdin.readline()
            
            if not line:
                if initialized:
                    debug("Stdin closed after successful initialization - keeping server alive")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        debug("Received interrupt, shutting down")
                        break
                else:
                    debug("Stdin closed before initialization")
                    break
            
            line = line.strip()
            if not line:
                continue
                
            debug(f"Received: {line}")
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")

            if method == "initialize":
                if req_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "frisco-weather-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    debug("Initialization response sent")
                
                initialized = True
                send_tool_declaration()
                
            elif method == "tools/list":
                if req_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "tools": [
                                {
                                    "name": "echo",
                                    "description": "Echo back text",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"}
                                        },
                                        "required": ["message"]
                                    }
                                },
                                {
                                    "name": "reverse",
                                    "description": "Reverse the order of characters in text",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "text": {"type": "string"}
                                        },
                                        "required": ["text"]
                                    }
                                },
                                {
                                    "name": "word_count",
                                    "description": "Count words, characters, and lines in text",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "text": {"type": "string"}
                                        },
                                        "required": ["text"]
                                    }
                                },
                                {
                                    "name": "weather",
                                    "description": "Get current weather for a city (defaults to Frisco, Colorado)",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "city": {
                                                "type": "string",
                                                "description": "City name (e.g., 'Las Vegas' or 'Denver')"
                                            }
                                        },
                                        "required": []
                                    }
                                },
                                {
                                    "name": "get_availability",
                                    "description": "Get calendar availability (busy/free times) - privacy protected",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "date": {
                                                "type": "string",
                                                "description": "Date to check - 'today', 'tomorrow', or YYYY-MM-DD format"
                                            }
                                        },
                                        "required": []
                                    }
                                }
                            ]
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    debug("Tools list response sent")
                
            elif method == "tools/call":
                if req_id is not None:
                    tool_name = req.get("params", {}).get("name")
                    
                    if tool_name == "echo":
                        message = req.get("params", {}).get("arguments", {}).get("message", "")
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": f"Echo: {message}"}]
                            }
                        }
                    elif tool_name == "reverse":
                        text = req.get("params", {}).get("arguments", {}).get("text", "")
                        reversed_text = text[::-1]
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": f"Reversed: {reversed_text}"}]
                            }
                        }
                    elif tool_name == "word_count":
                        text = req.get("params", {}).get("arguments", {}).get("text", "")
                        
                        # Count different metrics
                        word_count = len(text.split()) if text.strip() else 0
                        char_count = len(text)
                        char_count_no_spaces = len(text.replace(" ", ""))
                        line_count = len(text.splitlines()) if text else 0
                        
                        # Format the response
                        result = f"""Text Analysis:
📝 Words: {word_count}
🔤 Characters: {char_count}
🔤 Characters (no spaces): {char_count_no_spaces}
📄 Lines: {line_count}"""
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": result}]
                            }
                        }
                    elif tool_name == "weather":
                        # Fix the default parameter handling
                        city_arg = req.get("params", {}).get("arguments", {}).get("city")
                        if not city_arg or city_arg.strip() == "":
                            city = "Frisco, Colorado"
                        else:
                            city = city_arg.strip()
                        
                        try:
                            # Using free weather API (no key required) with urllib
                            city_encoded = urllib.parse.quote(city)
                            url = f"https://wttr.in/{city_encoded}?format=j1"
                            
                            with urllib.request.urlopen(url, timeout=15) as response_data:
                                if response_data.status == 200:
                                    weather_data = json.loads(response_data.read().decode())
                                    current = weather_data["current_condition"][0]
                                    today_weather = weather_data["weather"][0]
                                    tomorrow_weather = weather_data["weather"][1] if len(weather_data["weather"]) > 1 else None
                                    
                                    # Get today's hourly data for patterns
                                    hourly_today = today_weather.get("hourly", [])
                                    temps_today = [int(h["tempF"]) for h in hourly_today]
                                    
                                    # Analyze today's pattern
                                    if temps_today:
                                        max_temp = max(temps_today)
                                        min_temp = min(temps_today)
                                        temp_range = max_temp - min_temp
                                        
                                        if temp_range > 20:
                                            pattern = f"Variable day: {min_temp}°F to {max_temp}°F swing"
                                        elif temp_range > 10:
                                            pattern = f"Moderate range: {min_temp}°F to {max_temp}°F"
                                        else:
                                            pattern = f"Steady temps: around {max_temp}°F"
                                    else:
                                        pattern = "Pattern data unavailable"
                                    
                                    # Tomorrow's summary
                                    if tomorrow_weather:
                                        tom_max = tomorrow_weather["maxtempF"]
                                        tom_min = tomorrow_weather["mintempF"]
                                        tom_desc = tomorrow_weather["hourly"][0]["weatherDesc"][0]["value"] if tomorrow_weather.get("hourly") else "Unknown"
                                        tomorrow_summary = f"{tom_desc}, {tom_min}°F to {tom_max}°F"
                                    else:
                                        tomorrow_summary = "Forecast unavailable"
                                    
                                    # Enhanced weather response
                                    if city.lower().startswith("frisco"):
                                        location_note = "Perfect for your Frisco mountain planning! 🏔️❄️"
                                    else:
                                        location_note = f"Weather info for your {city} travel planning! ✈️🌍"
                                    
                                    weather_info = f"""🌤️ Weather for {city}:
🌡️ Current: {current['temp_F']}°F ({current['temp_C']}°C)
🌤️ Condition: {current['weatherDesc'][0]['value']}
💨 Wind: {current['windspeedMiles']} mph from {current['winddir16Point']}
💧 Humidity: {current['humidity']}%
👁️ Visibility: {current['visibility']} miles
🌡️ Feels like: {current['FeelsLikeF']}°F

📈 Today's Pattern: {pattern}
🔮 Tomorrow: {tomorrow_summary}

{location_note}"""
                                
                                else:
                                    weather_info = f"❌ Sorry, couldn't get weather for {city}. Try a different city name or check spelling!"
                                    
                        except urllib.error.URLError as e:
                            weather_info = f"🌐 Network error getting weather for {city}: {str(e)}"
                        except json.JSONDecodeError as e:
                            weather_info = f"⚠️ Error parsing weather data for {city}: Invalid response format"
                        except KeyError as e:
                            weather_info = f"⚠️ Incomplete weather data for {city}: Missing {str(e)}"
                        except Exception as e:
                            weather_info = f"⚠️ Error getting weather for {city}: {str(e)}"
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": weather_info}]
                            }
                        }
                    elif tool_name == "get_availability":
                        date_arg = req.get("params", {}).get("arguments", {}).get("date", "today")
                        
                        # Simple calendar availability simulation
                        # In a real implementation, this would connect to your actual calendar
                        
                        if date_arg.lower() == "today":
                            target_date = datetime.date.today()
                        elif date_arg.lower() == "tomorrow":
                            target_date = datetime.date.today() + datetime.timedelta(days=1)
                        else:
                            try:
                                target_date = datetime.datetime.strptime(date_arg, "%Y-%m-%d").date()
                            except:
                                target_date = datetime.date.today()
                        
                        day_name = target_date.strftime("%A, %B %d, %Y")
                        
                        # Sample availability (replace with real calendar integration)
                        availability = f"""📅 Availability for {day_name}:

✅ 08:00 AM - 08:30 AM - Available
❌ 08:30 AM - 09:00 AM - Busy
❌ 09:00 AM - 10:00 AM - Busy
✅ 10:00 AM - 10:30 AM - Available
❌ 10:30 AM - 10:55 AM - Busy
❌ 10:55 AM - 11:00 AM - Busy
❌ 11:00 AM - 11:15 AM - Busy
✅ 11:15 AM - 11:45 AM - Available
❌ 11:45 AM - 12:00 PM - Busy
❌ 12:00 PM - 01:00 PM - Busy
❌ 01:00 PM - 01:50 PM - Busy
✅ 01:50 PM - 02:00 PM - Available
❌ 02:00 PM - 02:25 PM - Busy
✅ 02:25 PM - 02:30 PM - Available
❌ 02:30 PM - 03:30 PM - Busy
❌ 03:30 PM - 04:30 PM - Busy
❌ 04:30 PM - 05:15 PM - Busy
✅ 05:15 PM - 06:00 PM - Available

🔒 Privacy protected - no meeting details shown"""
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": availability}]
                            }
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "error": {
                                "code": -32601,
                                "message": f"Unknown tool: {tool_name}"
                            }
                        }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    debug("Tool call response sent")
                
            else:
                if req_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Unknown method: {method}"
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    debug("Error response sent")
                else:
                    debug(f"Ignoring notification method: {method}")
                
        except json.JSONDecodeError as e:
            debug(f"JSON decode error: {e}")
            continue
        except BrokenPipeError:
            debug("Broken pipe - client disconnected")
            break

except EOFError:
    debug("EOF reached - stdin closed")
except Exception as e:
    debug(f"Fatal error: {e}")
    import traceback
    debug(f"Traceback: {traceback.format_exc()}")

debug("Server shutting down")