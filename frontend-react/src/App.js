import React, { useState } from 'react';
import { Send, Loader2, CheckCircle, Circle, Code2, Eye, Download, Settings2, Sparkles, Activity, ChevronRight, FileCode, Terminal, Play } from 'lucide-react';

const EmergentProfessionalUI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isBuilding, setIsBuilding] = useState(false);
  const [buildResult, setBuildResult] = useState(null);
  const [activeView, setActiveView] = useState('chat');
  const [modelConfig, setModelConfig] = useState({
    query_refiner_model: 'gemini-2.5-flash',
    orchestrator_model: 'gemini-2.5-flash',
    code_generator_model: 'gemini-2.5-pro',
    ui_enrichment_model: 'gemini-2.5-pro',
    code_reviewer_model: 'gemini-2.5-flash'
  });
  const [showSettings, setShowSettings] = useState(false);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const agents = [
    { name: 'Query Refiner', status: 'idle', icon: Activity },
    { name: 'Orchestrator', status: 'idle', icon: Settings2 },
    { name: 'Code Generator', status: 'idle', icon: Code2 },
    { name: 'UI Enrichment', status: 'idle', icon: Sparkles },
    { name: 'Code Reviewer', status: 'idle', icon: CheckCircle },
    { name: 'Deployment', status: 'idle', icon: Play }
  ];

  const [agentStatuses, setAgentStatuses] = useState(agents);

  const handleSend = async () => {
    if (!input.trim() || isBuilding) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsBuilding(true);
    setBuildResult(null);

    // Add assistant thinking message
    setMessages(prev => [...prev, { role: 'assistant', content: 'Building your application...', thinking: true }]);

    try {
      // Reset agent statuses
      setAgentStatuses(agents.map(a => ({ ...a, status: 'idle' })));

      const response = await fetch(`${API_BASE}/api/build-poc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requirement: input, model_config: modelConfig })
      });

      if (!response.ok) throw new Error('Build failed');

      const data = await response.json();

      // Simulate agent progress
      if (data.agent_responses) {
        for (let i = 0; i < data.agent_responses.length; i++) {
          await new Promise(r => setTimeout(r, 400));
          setAgentStatuses(prev => prev.map((a, idx) => 
            idx === i ? { ...a, status: 'completed' } : 
            idx === i + 1 ? { ...a, status: 'running' } : a
          ));
        }
      }

      setBuildResult(data);
      
      // Replace thinking message with success
      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1] = {
          role: 'assistant',
          content: `✅ Application built successfully!\n\nProject ID: ${data.project_id}\n\nQuality Scores:\n• Backend: ${data.review?.backend_score}/100\n• Frontend: ${data.review?.frontend_score}/100\n• Overall: ${data.review?.overall_score}/100\n\nYour application is ready to launch!`,
          thinking: false
        };
        return newMsgs;
      });

    } catch (error) {
      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1] = {
          role: 'assistant',
          content: '❌ Build failed: ' + error.message,
          thinking: false
        };
        return newMsgs;
      });
    } finally {
      setIsBuilding(false);
      setAgentStatuses(agents.map(a => ({ ...a, status: 'idle' })));
    }
  };

  const downloadCode = (code, filename) => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const launchApp = () => {
    if (buildResult?.frontend_code) {
      const win = window.open('', '_blank');
      win.document.write(buildResult.frontend_code);
      win.document.close();
    }
  };

  return (
    <div className="h-screen flex flex-col bg-white">
      {/* Header */}
      <div className="h-14 border-b border-gray-200 flex items-center justify-between px-6 bg-white">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-gray-900">Multi-Agent Builder</span>
          </div>
          <div className="h-5 w-px bg-gray-300" />
          <span className="text-sm text-gray-500">Agentic Development Platform</span>
        </div>
        
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            <Settings2 className="w-5 h-5 text-gray-600" />
          </button>
          <div className="px-3 py-1 bg-green-50 border border-green-200 rounded-full">
            <span className="text-xs font-medium text-green-700">● Connected</span>
          </div>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Model Configuration</h3>
          <div className="grid grid-cols-5 gap-3">
            {Object.keys(modelConfig).map((key) => (
              <div key={key}>
                <label className="block text-xs text-gray-600 mb-1.5">
                  {key.replace(/_model|_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </label>
                <select
                  value={modelConfig[key]}
                  onChange={(e) => setModelConfig({...modelConfig, [key]: e.target.value})}
                  className="w-full px-2 py-1.5 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                >
                  <option value="gemini-2.5-flash">Gemini 1.5 Flash</option>
                  <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                  <option value="gemini-pro">Gemini Pro</option>
                </select>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar - Agent Status */}
        <div className="w-72 border-r border-gray-200 bg-gray-50 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-sm font-semibold text-gray-900">Agent Pipeline</h2>
            <p className="text-xs text-gray-500 mt-1">6 agents • LangGraph workflow</p>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {agentStatuses.map((agent, idx) => {
              const Icon = agent.icon;
              return (
                <div
                  key={idx}
                  className={`p-3 rounded-lg border transition-all ${
                    agent.status === 'running'
                      ? 'border-violet-300 bg-violet-50'
                      : agent.status === 'completed'
                      ? 'border-green-300 bg-green-50'
                      : 'border-gray-200 bg-white'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {agent.status === 'running' ? (
                      <Loader2 className="w-4 h-4 text-violet-600 animate-spin" />
                    ) : agent.status === 'completed' ? (
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    ) : (
                      <Circle className="w-4 h-4 text-gray-400" />
                    )}
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">{agent.name}</div>
                      <div className="text-xs text-gray-500 capitalize">{agent.status}</div>
                    </div>
                    <Icon className={`w-4 h-4 ${
                      agent.status === 'running' ? 'text-violet-600' :
                      agent.status === 'completed' ? 'text-green-600' : 'text-gray-400'
                    }`} />
                  </div>
                </div>
              );
            })}
          </div>

          {buildResult && (
            <div className="p-4 border-t border-gray-200 space-y-2">
              <button
                onClick={launchApp}
                className="w-full bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition flex items-center justify-center gap-2"
              >
                <Eye className="w-4 h-4" />
                Launch Application
              </button>
              <button
                onClick={() => setActiveView('code')}
                className="w-full bg-gray-100 hover:bg-gray-200 text-gray-900 text-sm font-medium py-2 px-4 rounded-lg transition flex items-center justify-center gap-2"
              >
                <Code2 className="w-4 h-4" />
                View Source Code
              </button>
            </div>
          )}
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col bg-white">
          {activeView === 'chat' && (
            <>
              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto">
                {messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center px-6 text-center">
                    <div className="w-16 h-16 bg-gradient-to-br from-violet-100 to-indigo-100 rounded-2xl flex items-center justify-center mb-6">
                      <Sparkles className="w-8 h-8 text-violet-600" />
                    </div>
                    <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                      Build Any Application with AI Agents
                    </h2>
                    <p className="text-gray-600 mb-8 max-w-md">
                      Describe your application in natural language. Our AI agents will design, code, test, and deploy it for you.
                    </p>
                    <div className="grid grid-cols-2 gap-3 max-w-2xl">
                      <button
                        onClick={() => setInput('Build a task management app with priorities and deadlines')}
                        className="p-4 text-left border border-gray-200 rounded-lg hover:border-violet-300 hover:bg-violet-50 transition group"
                      >
                        <div className="font-medium text-gray-900 text-sm mb-1">Task Manager</div>
                        <div className="text-xs text-gray-500">With priorities and deadlines</div>
                      </button>
                      <button
                        onClick={() => setInput('Create an expense tracker with categories and monthly reports')}
                        className="p-4 text-left border border-gray-200 rounded-lg hover:border-violet-300 hover:bg-violet-50 transition group"
                      >
                        <div className="font-medium text-gray-900 text-sm mb-1">Expense Tracker</div>
                        <div className="text-xs text-gray-500">Categories and reports</div>
                      </button>
                      <button
                        onClick={() => setInput('Build a recipe sharing platform with ratings and comments')}
                        className="p-4 text-left border border-gray-200 rounded-lg hover:border-violet-300 hover:bg-violet-50 transition group"
                      >
                        <div className="font-medium text-gray-900 text-sm mb-1">Recipe Platform</div>
                        <div className="text-xs text-gray-500">Ratings and comments</div>
                      </button>
                      <button
                        onClick={() => setInput('Create an inventory system with stock alerts and suppliers')}
                        className="p-4 text-left border border-gray-200 rounded-lg hover:border-violet-300 hover:bg-violet-50 transition group"
                      >
                        <div className="font-medium text-gray-900 text-sm mb-1">Inventory System</div>
                        <div className="text-xs text-gray-500">Stock alerts and suppliers</div>
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="px-6 py-6 space-y-6 max-w-3xl mx-auto">
                    {messages.map((msg, idx) => (
                      <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                        {msg.role === 'assistant' && (
                          <div className="w-8 h-8 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
                            <Sparkles className="w-5 h-5 text-white" />
                          </div>
                        )}
                        <div className={`max-w-xl ${msg.role === 'user' ? 'order-first' : ''}`}>
                          <div className={`px-4 py-3 rounded-2xl ${
                            msg.role === 'user'
                              ? 'bg-violet-600 text-white'
                              : msg.thinking
                              ? 'bg-gray-100 text-gray-600 italic'
                              : 'bg-gray-100 text-gray-900'
                          }`}>
                            {msg.thinking && <Loader2 className="w-4 h-4 inline mr-2 animate-spin" />}
                            <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                          </div>
                        </div>
                        {msg.role === 'user' && (
                          <div className="w-8 h-8 bg-gray-200 rounded-lg flex items-center justify-center flex-shrink-0">
                            <span className="text-sm font-medium text-gray-600">You</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Input Area */}
              <div className="border-t border-gray-200 p-4 bg-white">
                <div className="max-w-3xl mx-auto">
                  <div className="flex gap-3">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                      placeholder="Describe the application you want to build..."
                      disabled={isBuilding}
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
                    />
                    <button
                      onClick={handleSend}
                      disabled={isBuilding || !input.trim()}
                      className="px-6 py-3 bg-violet-600 hover:bg-violet-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-xl transition flex items-center gap-2 font-medium"
                    >
                      {isBuilding ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Send className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">Press Enter to send • Shift+Enter for new line</p>
                </div>
              </div>
            </>
          )}

          {activeView === 'code' && buildResult && (
            <div className="flex-1 overflow-y-auto p-6">
              <div className="max-w-5xl mx-auto space-y-6">
                <div className="flex items-center justify-between mb-6">
                  <button
                    onClick={() => setActiveView('chat')}
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition"
                  >
                    <ChevronRight className="w-4 h-4 rotate-180" />
                    <span className="text-sm font-medium">Back to Chat</span>
                  </button>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
                      <Terminal className="w-4 h-4" />
                      Backend Code (Python/FastAPI)
                    </h3>
                    <button
                      onClick={() => downloadCode(buildResult.backend_code, 'backend.py')}
                      className="text-sm text-violet-600 hover:text-violet-700 flex items-center gap-1.5"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </button>
                  </div>
                  <div className="border border-gray-200 rounded-lg overflow-hidden">
                    <pre className="bg-gray-50 p-4 text-xs overflow-x-auto max-h-96">
                      <code className="text-gray-800">{buildResult.backend_code}</code>
                    </pre>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-gray-900 flex items-center gap-2">
                      <FileCode className="w-4 h-4" />
                      Frontend Code (HTML/CSS/JS)
                    </h3>
                    <button
                      onClick={() => downloadCode(buildResult.frontend_code, 'frontend.html')}
                      className="text-sm text-violet-600 hover:text-violet-700 flex items-center gap-1.5"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </button>
                  </div>
                  <div className="border border-gray-200 rounded-lg overflow-hidden">
                    <pre className="bg-gray-50 p-4 text-xs overflow-x-auto max-h-96">
                      <code className="text-gray-800">{buildResult.frontend_code}</code>
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmergentProfessionalUI;
