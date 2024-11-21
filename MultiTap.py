from burp import IBurpExtender, IHttpListener, ITab, IContextMenuFactory
from javax.swing import JMenuItem, JPopupMenu, JSplitPane, JTabbedPane, JColorChooser
from java.util import ArrayList
from java.awt import Color, Dimension
from javax.swing import JPanel, JButton, JTextField, BoxLayout, JLabel, Box, JTextArea, JScrollPane, JTable
from javax.swing.table import AbstractTableModel
from java.awt import BorderLayout
from java.text import SimpleDateFormat
from java.util import Date
import random
import json
import threading
import os
import traceback
from javax.swing.table import DefaultTableCellRenderer
from java.lang import Object

class BurpExtender(IBurpExtender, IHttpListener, ITab, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.sessions = {}
        self.matched_requests = []
        
        callbacks.setExtensionName("MultiTapBurp")
        callbacks.registerHttpListener(self)
        callbacks.registerContextMenuFactory(self)
        
        self.setupUI()
        self.setupRequestsTab()
        callbacks.addSuiteTab(self)
        callbacks.addSuiteTab(self.requestsTab)
        
        self.log("Extension initialized")
    
    def setupUI(self):
        self.panel = JPanel(BorderLayout())
        
        topPanel = JPanel()
        topPanel.setLayout(BoxLayout(topPanel, BoxLayout.Y_AXIS))
        
        creditsPanel = JPanel()
        creditsLabel = JLabel("Multi Taps by Aymen @J4k0m | LinkedIn: linkedin.com/in/jakom/")
        creditsPanel.add(creditsLabel)
        
        controlPanel = JPanel()
        self.sessionNameField = JTextField(15)
        self.patternField = JTextField(25)
        self.currentColor = self.generate_random_color()
        
        colorButton = JButton("Pick Color", actionPerformed=self.showColorPicker)
        self.colorPreview = JPanel()
        self.colorPreview.setBackground(self.currentColor)
        self.colorPreview.setPreferredSize(Dimension(20, 20))
        self.colorPreview.setMaximumSize(Dimension(20, 20))
        
        addButton = JButton("Add Session Pattern", actionPerformed=self.addBrowserSession)
        
        controlPanel.add(JLabel("Session Name:"))
        controlPanel.add(self.sessionNameField)
        controlPanel.add(Box.createHorizontalStrut(10))
        controlPanel.add(JLabel("Pattern:"))
        controlPanel.add(self.patternField)
        controlPanel.add(Box.createHorizontalStrut(10))
        controlPanel.add(colorButton)
        controlPanel.add(self.colorPreview)
        controlPanel.add(Box.createHorizontalStrut(10))
        controlPanel.add(addButton)
        
        topPanel.add(creditsPanel)
        topPanel.add(Box.createVerticalStrut(10))
        topPanel.add(controlPanel)
        
        centerPanel = JPanel()
        centerPanel.setLayout(BoxLayout(centerPanel, BoxLayout.Y_AXIS))
        
        self.sessionsPanel = JPanel()
        self.sessionsPanel.setLayout(BoxLayout(self.sessionsPanel, BoxLayout.Y_AXIS))
        sessionsScrollPane = JScrollPane(self.sessionsPanel)
        sessionsScrollPane.setPreferredSize(Dimension(800, 200))
        
        centerPanel.add(JLabel("Active Sessions:"))
        centerPanel.add(Box.createVerticalStrut(5))
        centerPanel.add(sessionsScrollPane)
        
        bottomPanel = JPanel(BorderLayout())
        bottomPanel.add(JLabel("Logs:"), BorderLayout.NORTH)
        
        self.logArea = JTextArea()
        self.logArea.setEditable(False)
        self.logArea.setLineWrap(True)
        self.logArea.setWrapStyleWord(True)
        logScrollPane = JScrollPane(self.logArea)
        logScrollPane.setPreferredSize(Dimension(800, 200))
        
        bottomPanel.add(logScrollPane, BorderLayout.CENTER)
        
        self.panel.add(topPanel, BorderLayout.NORTH)
        self.panel.add(centerPanel, BorderLayout.CENTER)
        self.panel.add(bottomPanel, BorderLayout.SOUTH)

    def setupRequestsTab(self):
        self.requestsTab = RequestsTab(self)
    
    def log(self, message):
        timestamp = SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(Date())
        log_message = "[{}] {}\n".format(timestamp, message)
        self.logArea.append(log_message)
        self.logArea.setCaretPosition(self.logArea.getDocument().getLength())
    
    def addBrowserSession(self, event):
        session_name = self.sessionNameField.getText()
        pattern = self.patternField.getText()
        
        if not session_name or not pattern:
            self.log("ERROR: Both session name and pattern are required")
            return
        
        session_id = str(random.randint(10000, 99999))
        
        self.sessions[session_id] = {
            'name': session_name,
            'pattern': pattern,
            'color': self.currentColor
        }
        
        self.currentColor = self.generate_random_color()
        self.colorPreview.setBackground(self.currentColor)
        
        self.updateSessionsList()
        self.log("Added new session: {} (ID: {}, Pattern: {})".format(
            session_name, session_id, pattern))
    
    def generate_random_color(self):
        hue = random.random()
        saturation = 0.7 + random.random() * 0.3
        brightness = 0.7 + random.random() * 0.3
        
        color = Color.getHSBColor(hue, saturation, brightness)
        return color
    
    def updateSessionsList(self):
        self.sessionsPanel.removeAll()
        
        for session_id, session_info in self.sessions.items():
            row = JPanel()
            row.setLayout(BoxLayout(row, BoxLayout.X_AXIS))
            row.setMaximumSize(Dimension(32767, 30))
            
            sessionLabel = JLabel("{} (Pattern: {})".format(
                session_info['name'], session_info['pattern']))
            labelPanel = JPanel()
            labelPanel.add(sessionLabel)
            
            colorPanel = JPanel()
            colorPanel.setBackground(session_info['color'])
            colorPanel.setPreferredSize(Dimension(20, 20))
            
            row.add(labelPanel)
            row.add(Box.createHorizontalGlue())
            row.add(colorPanel)
            
            self.sessionsPanel.add(row)
            self.sessionsPanel.add(Box.createVerticalStrut(5))
        
        self.sessionsPanel.revalidate()
        self.sessionsPanel.repaint()
    
    def showColorPicker(self, event):
        color = JColorChooser.showDialog(
            self.panel,
            "Choose Session Color",
            self.currentColor
        )
        if color:
            self.currentColor = color
            self.colorPreview.setBackground(color)
    
    def getTabCaption(self):
        return "Multi Tap"
    
    def getUiComponent(self):
        return self.panel
    
    def createMenuItems(self, invocation):
        return None
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            try:
                request = messageInfo.getRequest()
                requestInfo = self.helpers.analyzeRequest(request)
                
                headers = requestInfo.getHeaders()
                body = request[requestInfo.getBodyOffset():].tostring()
                full_request = "\n".join(str(header) for header in headers) + "\n" + body
                
                for session_id, session_info in self.sessions.items():
                    pattern = session_info['pattern']
                    
                    if pattern.lower() in full_request.lower():
                        color = session_info['color']
                        rgb_int = color.getRGB() & 0xFFFFFF
                        messageInfo.setHighlight(str(rgb_int))
                        
                        self.requestsTab.addRequest(messageInfo, session_info['name'], pattern)
                        
                        self.log("Request matched session {} (Pattern: {})".format(
                            session_info['name'], pattern))
                        break
                        
            except Exception as e:
                self.log("ERROR: Processing message failed - {}".format(str(e)))
                self.log("Stack trace: {}".format(traceback.format_exc()))

class RequestsTab(ITab):
    def __init__(self, extender):
        self.extender = extender
        self.matched_requests = []
        
        self.panel = JPanel(BorderLayout())
        
        topPanel = JPanel(BorderLayout())
        clearButton = JButton("Clear History", actionPerformed=self.clearHistory)
        topPanel.add(clearButton, BorderLayout.EAST)
        
        self.requestsTable = JTable(self.RequestsTableModel(self))
        self.requestsTable.setAutoCreateRowSorter(True)
        self.requestsTable.setDefaultRenderer(Object, self.CellRenderer(self))
        
        self.setupPopupMenu()
        
        scrollPane = JScrollPane(self.requestsTable)
        
        splitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        splitPane.setResizeWeight(0.5)
        
        self.requestViewer = self.extender.callbacks.createMessageEditor(None, False)
        self.responseViewer = self.extender.callbacks.createMessageEditor(None, False)
        
        reqResPanel = JPanel(BorderLayout())
        tabs = JTabbedPane()
        tabs.addTab("Request", self.requestViewer.getComponent())
        tabs.addTab("Response", self.responseViewer.getComponent())
        reqResPanel.add(tabs, BorderLayout.CENTER)
        
        splitPane.setLeftComponent(scrollPane)
        splitPane.setRightComponent(reqResPanel)
        
        self.panel.add(topPanel, BorderLayout.NORTH)
        self.panel.add(splitPane, BorderLayout.CENTER)
        
        self.requestsTable.getSelectionModel().addListSelectionListener(
            lambda e: self.showReqRes(e) if not e.getValueIsAdjusting() else None
        )
    
    def setupPopupMenu(self):
        self.menu = JPopupMenu()
        sendToRepeater = JMenuItem("Send to Repeater",
            actionPerformed=lambda x: self.sendToRepeater())
        sendToIntruder = JMenuItem("Send to Intruder",
            actionPerformed=lambda x: self.sendToIntruder())
        
        self.menu.add(sendToRepeater)
        self.menu.add(sendToIntruder)
        
        self.requestsTable.setComponentPopupMenu(self.menu)
    
    def sendToRepeater(self):
        row = self.requestsTable.getSelectedRow()
        if row != -1:
            row = self.requestsTable.convertRowIndexToModel(row)
            request = self.matched_requests[row]
            
            messageInfo = request['messageInfo']
            url = self.extender.helpers.analyzeRequest(messageInfo).getUrl()
            
            self.extender.callbacks.sendToRepeater(
                url.getHost(),
                url.getPort(),
                url.getProtocol() == "https",
                messageInfo.getRequest(),
                request['session']
            )
    
    def sendToIntruder(self):
        row = self.requestsTable.getSelectedRow()
        if row != -1:
            row = self.requestsTable.convertRowIndexToModel(row)
            request = self.matched_requests[row]
            
            messageInfo = request['messageInfo']
            url = self.extender.helpers.analyzeRequest(messageInfo).getUrl()
            
            self.extender.callbacks.sendToIntruder(
                url.getHost(),
                url.getPort(),
                url.getProtocol() == "https",
                messageInfo.getRequest()
            )
    
    def getTabCaption(self):
        return "Session Requests"
    
    def getUiComponent(self):
        return self.panel
    
    def addRequest(self, messageInfo, session_name, pattern):
        request = messageInfo.getRequest()
        url = self.extender.helpers.analyzeRequest(messageInfo).getUrl()
        
        self.matched_requests.append({
            'messageInfo': messageInfo,
            'session': session_name,
            'pattern': pattern,
            'url': str(url),
            'method': self.extender.helpers.analyzeRequest(messageInfo).getMethod(),
            'timestamp': SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(Date())
        })
        
        self.requestsTable.getModel().fireTableDataChanged()
    
    def showReqRes(self, event):
        row = self.requestsTable.getSelectedRow()
        if row != -1:
            row = self.requestsTable.convertRowIndexToModel(row)
            messageInfo = self.matched_requests[row]['messageInfo']
            
            self.requestViewer.setMessage(messageInfo.getRequest(), True)
            
            response = messageInfo.getResponse()
            if response:
                self.responseViewer.setMessage(response, False)
            else:
                self.responseViewer.setMessage(None, False)
    
    def clearHistory(self, event):
        self.matched_requests = []
        self.requestsTable.getModel().fireTableDataChanged()
        self.requestViewer.setMessage(None, False)
        self.responseViewer.setMessage(None, False)
        self.extender.log("Request history cleared")
    
    class RequestsTableModel(AbstractTableModel):
        def __init__(self, tab):
            self.tab = tab
            self.columnNames = ["Time", "Session", "Method", "URL", "Pattern"]
        
        def getColumnCount(self):
            return len(self.columnNames)
        
        def getRowCount(self):
            return len(self.tab.matched_requests)
        
        def getColumnName(self, col):
            return self.columnNames[col]
        
        def getValueAt(self, row, col):
            request = self.tab.matched_requests[row]
            if col == 0: return request['timestamp']
            elif col == 1: return request['session']
            elif col == 2: return request['method']
            elif col == 3: return request['url']
            elif col == 4: return request['pattern']
            return ""
    
    class CellRenderer(DefaultTableCellRenderer):
        def __init__(self, tab):
            self.tab = tab
        
        def getTableCellRendererComponent(self, table, value, isSelected, hasFocus, row, col):
            c = DefaultTableCellRenderer.getTableCellRendererComponent(
                self, table, value, isSelected, hasFocus, row, col)
            
            if not isSelected:
                row = table.convertRowIndexToModel(row)
                session_name = self.tab.matched_requests[row]['session']
                
                for session in self.tab.extender.sessions.values():
                    if session['name'] == session_name:
                        c.setBackground(session['color'])
                        break
            
            return c
