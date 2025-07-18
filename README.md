# MCP Weather & Utility Server

A fully functional Model Context Protocol (MCP) server built from scratch, featuring text processing tools and real-time weather API integration.

## 🌟 Features

This MCP server provides four powerful tools that extend Claude's capabilities:

### 🔄 **Echo Tool**
- Simple text echoing functionality
- Perfect for testing MCP connections
- Returns formatted response with "Echo:" prefix

### 🔀 **Reverse Tool** 
- Reverses any text string character by character
- Useful for text manipulation and processing
- Example: "hello" → "olleh"

### 📊 **Word Count Tool**
- Comprehensive text analysis with detailed metrics
- Counts words, characters (with/without spaces), and lines
- Returns beautifully formatted results with emojis
- Perfect for content analysis and writing assistance

### 🌤️ **Weather Tool**
- **Real-time weather data** via HTTP API integration
- Defaults to Frisco, Colorado (customizable for any city)
- Fetches live temperature, conditions, wind, humidity, and visibility
- Returns formatted weather reports with emojis
- Demonstrates full web API integration capabilities

## 🛠️ Technical Implementation

### MCP Protocol Features
- ✅ Full JSON-RPC 2.0 implementation
- ✅ Proper initialization handshake
- ✅ Tool declaration and discovery (`tools/list` support)
- ✅ Error handling and graceful shutdowns
- ✅ Signal handling for clean termination

### Web API Integration
- HTTP requests using Python's built-in `urllib`
- JSON parsing and data processing
- Error handling for network issues
- Real-time data fetching from external APIs

### Enterprise Compatibility
- Works alongside existing DLP (Data Loss Prevention) systems
- Security-compliant architecture
- Proper logging and debugging support
- Production-ready code structure

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Claude Desktop with MCP support
- Internet connection for weather functionality

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/g-gerchow/MCP-xjg.git
   cd MCP-xjg
   ```

2. **Configure Claude Desktop:**
   
   Create or edit `~/.config/claude-desktop/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "xjg_server": {
         "command": "/opt/homebrew/bin/python3",
         "args": ["-u", "/path/to/your/mcp-xjg/xjg.py"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test the connection:**
   Ask Claude: "What tools are available from xjg_server?"

## 📝 Usage Examples

### Echo Tool
```
User: "Echo the message 'Hello MCP!'"
Response: "Echo: Hello MCP!"
```

### Reverse Tool
```
User: "Reverse the text 'MCP Server'"
Response: "Reversed: revreS PCM"
```

### Word Count Tool
```
User: "Count words in 'Building MCP servers is awesome!'"
Response: 
Text Analysis:
📝 Words: 5
🔤 Characters: 32
🔤 Characters (no spaces): 27
📄 Lines: 1
```

### Weather Tool
```
User: "Get the weather"
Response:
🌤️ Weather for Frisco, Colorado:
🌡️ Temperature: 51°F (10°C)
🌤️ Condition: Sunny
💨 Wind: 2 mph
💧 Humidity: 50%
👁️ Visibility: 16 miles

Perfect for checking your hometown weather! 🏔️❄️
```

## 🏗️ Architecture

### Server Structure
- **Initialization**: Handles MCP protocol handshake
- **Tool Declaration**: Announces available tools to Claude
- **Tool Discovery**: Responds to `tools/list` requests
- **Tool Execution**: Processes and responds to tool calls
- **Error Handling**: Graceful error management and logging

### Code Organization
```
xjg.py
├── Imports and setup
├── Debug logging function
├── Tool declaration function
├── Signal handlers
├── Main server loop
│   ├── Initialize method handler
│   ├── Tools/list method handler
│   ├── Tools/call method handler
│   └── Error handling
└── Graceful shutdown
```

## 🛡️ Security Features

- Input validation and sanitization
- Proper error handling to prevent crashes
- Graceful handling of network timeouts
- Compatible with enterprise DLP systems
- No sensitive data logging

## 🔧 Development

### Adding New Tools

1. **Add tool to declaration** in `send_tool_declaration()`
2. **Add tool to list response** in the `tools/list` handler  
3. **Implement tool logic** in the `tools/call` handler
4. **Test thoroughly** with Claude

### Debugging
- Enable debug logging by monitoring stderr output
- Check Claude's MCP logs for connection issues
- Test tools individually for isolation

## 📈 Performance

- Lightweight Python implementation
- Efficient JSON processing
- Minimal memory footprint
- Fast response times for all tools
- Reliable HTTP requests with timeout handling

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for:
- New tool implementations
- Performance improvements
- Bug fixes
- Documentation enhancements

## 📄 License

This project is open source and available under the MIT License.

## 🎯 What I Learned

Building this MCP server taught me:
- **MCP Protocol**: Complete understanding of JSON-RPC and MCP specifications
- **Web API Integration**: Real-time data fetching and processing
- **Error Handling**: Robust error management and graceful failures
- **Enterprise Software**: Building tools that work in corporate environments
- **Python Development**: Advanced Python programming and debugging
- **Version Control**: Git workflow and collaborative development

## 🚀 Future Enhancements

Potential additions:
- **News API integration** for latest headlines
- **File operations** for document processing  
- **Database connectivity** for data storage
- **Email integration** for communication tools
- **Calendar integration** for scheduling

---

**Built with ❤️ and lots of debugging!** 

This project represents a journey from basic syntax errors to building production-ready MCP servers with web API integration.
