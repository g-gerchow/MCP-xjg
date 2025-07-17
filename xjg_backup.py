#!/opt/homebrew/bin/python3

import sys
import json
import signal
import time

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
    
    # Make stdin non-blocking and handle connection state
    initialized = False
    
    while True:
        try:
            line = sys.stdin.readline()
            
            # If readline returns empty string, stdin is closed
            if not line:
                if initialized:
                    debug("Stdin closed after successful initialization - keeping server alive")
                    # Keep the server running even if stdin closes
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
                # Only respond if there's an ID (this is a request, not a notification)
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
                                "name": "xjg-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    debug("Initialization response sent")
                
                # Mark as initialized
                initialized = True
                
                # Now send tool declaration
                send_tool_declaration()
                
            elif method == "tools/call":
                # Only respond if there's an ID
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
                # Only send error response if there's an ID
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