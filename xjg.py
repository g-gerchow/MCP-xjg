#!/opt/homebrew/bin/python3

import sys
import json
import signal
import time
import urllib.request
import urllib.parse

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
                        city = req.get("params", {}).get("arguments", {}).get("city", "Frisco, Colorado")
                        
                        try:
                            # Using free weather API (no key required) with urllib
                            city_encoded = urllib.parse.quote(city)
                            url = f"https://wttr.in/{city_encoded}?format=j1"
                            
                            with urllib.request.urlopen(url, timeout=10) as response_data:
                                if response_data.status == 200:
                                    weather_data = json.loads(response_data.read().decode())
                                    current = weather_data["current_condition"][0]
                                    
                                    # Format weather info for your hometown!
                                    weather_info = f"""🌤️ Weather for {city}:
🌡️ Temperature: {current['temp_F']}°F ({current['temp_C']}°C)
🌤️ Condition: {current['weatherDesc'][0]['value']}
💨 Wind: {current['windspeedMiles']} mph
💧 Humidity: {current['humidity']}%
👁️ Visibility: {current['visibility']} miles

Perfect for checking your hometown weather! 🏔️❄️"""
                                
                                else:
                                    weather_info = f"❌ Sorry, couldn't get weather for {city}. Try a different city name!"
                                    
                        except urllib.error.URLError as e:
                            weather_info = f"🌐 Network error getting weather: {str(e)}"
                        except Exception as e:
                            weather_info = f"⚠️ Error processing weather data: {str(e)}"
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "content": [{"type": "text", "text": weather_info}]
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