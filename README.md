# MultiTapBurp

![image](https://github.com/user-attachments/assets/dd49b92b-534b-48bc-bc6d-41daf8559ec8)


MultiTapBurp is a Burp Suite extension that helps track and manage multiple sessions simultaneously by color-coding HTTP requests based on custom patterns.

## Features

1. **Session Management**
   - Create multiple sessions with unique names
   - Define custom patterns to identify requests
   - Assign custom colors to each session
   - Visual display of active sessions

2. **Request Tracking**
   - Automatically captures and color-codes requests matching session patterns
   - Real-time request monitoring
   - Displays timestamp, session name, HTTP method, URL, and matching pattern
   - Color-coded table rows for easy visual identification

3. **Request Analysis**
   - View full request and response details
   - Split view showing request list and request/response details
   - Tabbed interface for request and response inspection

4. **Integration with Burp Tools**
   - Send requests to Burp Repeater
   - Send requests to Burp Intruder
   - Right-click context menu for easy access

5. **Utility Features**
   - Clear history functionality
   - Custom color picker for sessions
   - Activity logging
   - Sortable request table

## Use Cases

- Testing multiple user sessions simultaneously
- Tracking requests from different authentication tokens
- Monitoring specific request patterns
- Organizing and categorizing HTTP traffic
- Identifying session-specific behaviors

## Interface

1. **Main Tab**
   - Session creation controls
   - Active sessions display
   - Activity logs

2. **Session Requests Tab**
   - Color-coded request table
   - Request/Response viewer
   - Tool integration options

## Installation

1. Download the extension file
2. Open Burp Suite
3. Go to Extender tab
4. Click "Add" button
5. Select the extension file
6. The extension will appear as "MultiTapBurp" in the extensions list

## Usage

1. Create a new session:
   - Enter a session name
   - Define a pattern to match requests
   - Choose a color (or use random)
   - Click "Add Session Pattern"

2. Monitor requests:
   - Requests matching your patterns will be automatically captured
   - View requests in the Session Requests tab
   - Use the color coding to identify different sessions

3. Analyze requests:
   - Click on any request to view details
   - Use tabs to switch between request and response
   - Right-click to send to other Burp tools

## Author
Multi Taps by Aymen @J4k0m | LinkedIn: linkedin.com/in/jakom/
