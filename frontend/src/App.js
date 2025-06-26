import React, { useState, useEffect, useRef, useCallback } from 'react';
import './App.css';

// Main App Component
function App() {
  // --- STATES ---
  const [isListening, setIsListening] = useState(false);
  const [isVoiceSupported, setIsVoiceSupported] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(true); // Set to true for easier testing
  const [activeView, setActiveView] = useState('chat'); // Start at chat view
  const [username, setUsername] = useState('user'); // Pre-fill for testing
  const [password, setPassword] = useState('password');
  const [email, setEmail] = useState('user@example.com');
  const [loginError, setLoginError] = useState('');
  const [signupError, setSignupError] = useState('');
  const [isSigningUp, setIsSigningUp] = useState(false);
  const [faqMessages, setFaqMessages] = useState([]);
  const [faqInput, setFaqInput] = useState('');
  const [isFaqSending, setIsFaqSending] = useState(false);
  const faqChatEndRef = useRef(null);
  const [urlA, setUrlA] = useState('');
  const [urlB, setUrlB] = useState('');
  const [initialPrompt, setInitialPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [ragConversation, setRagConversation] = useState([]);
  const [ragInput, setRagInput] = useState('');
  const [language, setLanguage] = useState('en'); // 'en' or 'kn'
  const ragChatEndRef = useRef(null);
  const [historicalMessages, setHistoricalMessages] = useState([]);
  const [linkedAccounts, setLinkedAccounts] = useState([
    { id: '1', name: 'Nandini', email: 'nandueduka@gmail.com', status: 'active' },
    { id: '2', name: 'NANDINI N.', email: '1ms22is085@msrit.edu', status: 'signed out' },
  ]);
  
  const API_BASE_URL = process.env.REACT_APP_API_URL;

  const samplePrompts = {
    en: [
      "Compare these two for a personal loan. Which has lower fees and better pre-payment terms?",
      "Analyze the interest rates of both documents. Which one is better for a long-term fixed deposit?",
      "Summarize the key differences in the terms and conditions of these two products.",
      "Which of these two options is better for someone with a low risk appetite? Explain why."
    ],
    kn: [
      "ವೈಯಕ್ತಿಕ ಸಾಲಕ್ಕಾಗಿ ಇವೆರಡನ್ನೂ ಹೋಲಿಕೆ ಮಾಡಿ. ಯಾವುದರಲ್ಲಿ ಕಡಿಮೆ ಶುಲ್ಕ ಮತ್ತು ಉತ್ತಮ ಪೂರ್ವ-ಪಾವತಿ ನಿಯಮಗಳಿವೆ?",
      "ಎರಡೂ ದಾಖಲೆಗಳ ಬಡ್ಡಿ ದರಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ. ದೀರ್ಘಾವಧಿಯ ಸ್ಥಿರ ಠೇವಣಿಗೆ ಯಾವುದು ಉತ್ತಮ?",
      "ಈ ಎರಡು ಉತ್ಪನ್ನಗಳ ನಿಯಮಗಳು ಮತ್ತು ಷರತ್ತುಗಳಲ್ಲಿನ ಪ್ರಮುಖ ವ್ಯತ್ಯಾಸಗಳನ್ನು ಸಾರಾಂಶಗೊಳಿಸಿ.",
      "ಕಡಿಮೆ ರಿಸ್ಕ್ ತೆಗೆದುಕೊಳ್ಳುವವರಿಗೆ ಈ ಎರಡು ಆಯ್ಕೆಗಳಲ್ಲಿ ಯಾವುದು ಉತ್ತಮ? ಕಾರಣವನ್ನು ವಿವರಿಸಿ."
    ]
  };

  const sampleFaqQuestions = [
    {
        "en": "What is an investment?",
        "kn": "ಹೂಡಿಕೆ ಎಂದರೇನು?"
    },
    {
        "en": "How does health insurance help?",
        "kn": "ಆರೋಗ್ಯ ವಿಮೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ?"
    },
    {
        "en": "How can a student save money?",
        "kn": "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಉತ್ತಮವಾದ ಆರ್ಥಿಕ ಯೋಜನೆ ಯಾವುದು?"
    },
    {
        "en": "What are schemes for farmers?",
        "kn": "ರೈತರಿಗಾಗಿ ಇರುವ ಯೋಜನೆಗಳು ಯಾವುವು?"
    }
  ];

  const recognitionRef = useRef(null);


  const loadHistoricalMessages = useCallback(async (currentUserId) => {
    if (!currentUserId) return;
    try {
      const response = await fetch(`${API_BASE_URL}/chat/history/${currentUserId}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const history = await response.json();
      setHistoricalMessages(history);
    } catch (error) {
      console.error("Failed to load historical messages:", error);
      setHistoricalMessages([]);
    }
  }, [API_BASE_URL]);
  // --- CHANGE 1: UPDATED VOICE RECOGNITION LOGIC ---
  // This useEffect now checks which view is active to update the correct input field.
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsVoiceSupported(false);
      console.error("Speech Recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = language === 'en' ? 'en-US' : 'kn-IN';

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      setIsListening(false);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      // This logic now correctly routes the transcript to the active input
      if (activeView === 'compare') {
          setRagInput(transcript);
      } else {
          setFaqInput(transcript);
      }
    };

    recognitionRef.current = recognition;

  }, [language, activeView]); // Added activeView to the dependency array

  useEffect(() => {
    if (activeView === 'chat') {
        faqChatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [activeView,faqMessages]);

  useEffect(() => {
    if (activeView === 'compare') {
        ragChatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [activeView,ragConversation]);


  useEffect(() => {
    if (activeView === 'history' && isLoggedIn && username) {
      loadHistoricalMessages(username);
    }
  }, [activeView, isLoggedIn, username,loadHistoricalMessages]);

  const handleLanguageToggle = () => setLanguage(prev => prev === 'en' ? 'kn' : 'en');
  const handleLogin = (e) => { e.preventDefault(); setLoginError(''); if (username === 'user' && password === 'password') { setIsLoggedIn(true); setActiveView('chat'); } else { setLoginError('Invalid credentials.'); } };
  const handleSignup = (e) => { e.preventDefault(); setSignupError(''); if (username && email && password) { setIsLoggedIn(true); setActiveView('chat'); } else { setSignupError('Please fill all fields.'); } };
  const handleSignOut = () => { setIsLoggedIn(false); setUsername(''); setPassword(''); setEmail(''); setFaqMessages([]); setRagConversation([]); setSessionId(null); setActiveView('auth'); };

  const handleFaqSendMessage = async (e) => {
    e.preventDefault();
    if (!faqInput.trim() || isFaqSending) return;
    const currentInput = faqInput;
    setFaqInput('');
    await sendFaqMessage(currentInput);
  };

  const handleSampleQuestionClick = async (question) => {
    if (isFaqSending) return;
    await sendFaqMessage(question);
  };
  
  

  const sendFaqMessage = async (messageText) => {
    const userMsg = { id: crypto.randomUUID(), message: messageText, sender: 'user', timestamp: new Date().toISOString() };
    setFaqMessages((prev) => [...prev, userMsg]);
    setIsFaqSending(true);
    try {
        const response = await fetch(`${API_BASE_URL}/chat/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: username, message: messageText, sender: "user" }),
        });
        if (!response.ok) throw new Error("Backend error");
        const botMsg = await response.json();
        setFaqMessages((prev) => [...prev, botMsg]);
    } catch (err) {
        setFaqMessages((prev) => [...prev, { id: crypto.randomUUID(), message: "Sorry, I couldn't connect to the server.", sender: 'bot' }]);
    } finally {
        setIsFaqSending(false);
    }
  };

  const handleVoiceInput = () => {
    if (!isVoiceSupported) {
      alert("Sorry, your browser does not support voice input.");
      return;
    }

    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
    }
  };

  const handleProcessUrls = async () => {
    if (!urlA.trim() || !urlB.trim()) {
      alert("Please provide both URLs for analysis.");
      return;
    }
    setIsProcessing(true);
    setRagConversation([]);
    setSessionId(null);

    try {
      const response = await fetch(`${API_BASE_URL}/process-urls`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urls: [urlA, urlB] }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to process URLs.");
      }
      
      const result = await response.json();
      setSessionId(result.session_id);
      
      const questionToSend = initialPrompt.trim() !== ''
        ? initialPrompt
        : language === 'en' 
            ? "Compare the financial products from Website A and Website B. Summarize their key features like interest rates and fees, and recommend which is better for a loan."
            : "ವೆಬ್‌ಸೈಟ್ ಎ ಮತ್ತು ವೆಬ್‌ಸೈಟ್ ಬಿ ಯಿಂದ ಹಣಕಾಸು ಉತ್ಪನ್ನಗಳನ್ನು ಹೋಲಿಕೆ ಮಾಡಿ. ಬಡ್ಡಿ ದರಗಳು ಮತ್ತು ಶುಲ್ಕಗಳಂತಹ ಪ್ರಮುಖ ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ಸಾರಾಂಶಗೊಳಿಸಿ ಮತ್ತು ಸಾಲಕ್ಕೆ ಯಾವುದು ಉತ್ತಮ ಎಂದು ಶಿಫಾರಸು ಮಾಡಿ.";

      handleRagQuestionSubmit(result.session_id, questionToSend);

    } catch (error) {
      setRagConversation([{ sender: 'system', text: `Error: ${error.message}` }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRagQuestionSubmit = async (currentSessionId, question) => {
    if (!question.trim() || !currentSessionId) return;
    const userMessage = { sender: 'user', text: question };
    setRagConversation(prev => [...prev, userMessage]);
    setIsGenerating(true);
    setRagInput('');
    try {
      const response = await fetch(`${API_BASE_URL}/document-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            session_id: currentSessionId, 
            question: question,
            language: language
        }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to get an answer.");
      }
      const result = await response.json();
      const botMessage = { sender: 'bot', text: result.answer };
      setRagConversation(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { sender: 'system', text: `Error: ${error.message}` };
      setRagConversation(prev => [...prev, errorMessage]);
    } finally {
      setIsGenerating(false);
    }
  };
  
  const handleResetAnalysis = () => {
      setSessionId(null);
      setRagConversation([]);
      setUrlA('');
      setUrlB('');
      setInitialPrompt('');
  };
  
  const formatDisplayTimestamp = (isoTimestamp) => {
    if (!isoTimestamp) return '';
    try {
      const date = new Date(isoTimestamp);
      return date.toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true
      });
    } catch (error) {
      console.error("Error formatting timestamp:", error);
      return isoTimestamp;
    }
  };

  

  const handleClearHistory = async () => {
    if (!username) {
        alert("You must be logged in to clear history.");
        return;
    }
    if (window.confirm(`Are you sure you want to permanently delete all chat history for user '${username}'? This action cannot be undone.`)) {
      try {
        const response = await fetch(`${API_BASE_URL}/chat/history/${username}`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        alert(result.message || "Chat history cleared successfully.");
        setHistoricalMessages([]);
        setFaqMessages([]);
      } catch (error) {
        console.error("Failed to clear chat history from server:", error);
        alert(`Failed to clear chat history: ${error.message}`);
      }
    }
  };

  const handleLinkedAccountSignIn = (accountId) => { setLinkedAccounts(prevAccounts => prevAccounts.map(acc => acc.id === accountId ? { ...acc, status: 'active' } : acc)); };
  const handleLinkedAccountRemove = (accountId) => { setLinkedAccounts(prevAccounts => prevAccounts.filter(acc => acc.id !== accountId)); };

  const renderContent = () => {
    if (!isLoggedIn) {
      return (
        <div className="flex flex-col items-center justify-center h-full p-6 bg-gray-100">
          <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md border">
            <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">{isSigningUp ? 'Join Finease' : 'Welcome Back!'}</h2>
            {loginError && <p className="text-red-500 text-sm text-center mb-4">{loginError}</p>}
            {signupError && <p className="text-red-500 text-sm text-center mb-4">{signupError}</p>}
            {isSigningUp ? (
              <form onSubmit={handleSignup} className="space-y-4">
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full p-3 border rounded-lg" required />
                <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full p-3 border rounded-lg" required />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-3 border rounded-lg" required />
                <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg">Sign Up</button>
              </form>
            ) : (
              <form onSubmit={handleLogin} className="space-y-4">
                <input type="text" placeholder="Username or Email" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full p-3 border rounded-lg" required />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-3 border rounded-lg" required />
                <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg">Login</button>
              </form>
            )}
            <p className="text-center text-sm mt-6"><button type="button" className="text-blue-600 hover:underline" onClick={() => setIsSigningUp(!isSigningUp)}>{isSigningUp ? 'Already have an account? Log In' : "Don't have an account? Sign Up"}</button></p>
            {!isSigningUp && (<p className="text-center text-sm mt-2">Hint: user / password</p>)}
          </div>
        </div>
      );
    }
    
    switch (activeView) {
      case 'compare':
        return (
            <div className="flex flex-col h-full bg-gray-100">
                <div className="p-4 border-b bg-white shadow-sm flex-shrink-0">
                    {sessionId ? (
                        <div className="flex justify-between items-center">
                            <h2 className="text-xl font-bold text-gray-800">{language === 'en' ? 'Analysis Results' : 'ವಿಶ್ಲೇಷಣೆಯ ಫಲಿತಾಂಶಗಳು'}</h2>
                            <button onClick={handleResetAnalysis} className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg text-sm">
                                &larr; {language === 'en' ? 'Start New Analysis' : 'ಹೊಸ ವಿಶ್ಲೇಷಣೆ ಪ್ರಾರಂಭಿಸಿ'}
                            </button>
                        </div>
                    ) : (
                        <>
                            <h2 className="text-xl font-bold text-gray-800 mb-4">{language === 'en' ? 'Web Analysis Engine' : 'ವೆಬ್ ವಿಶ್ಲೇಷಣಾ ಇಂಜಿನ್'}</h2>
                            <div className="space-y-3">
                                <div>
                                    <label className="block text-sm font-semibold mb-1 text-gray-700">{language === 'en' ? 'Website URL A' : 'ವೆಬ್‌ಸೈಟ್ URL A'}</label>
                                    <input type="url" value={urlA} onChange={(e) => setUrlA(e.target.value)} className="w-full p-2 border border-gray-300 rounded-lg" placeholder="https://www.icicibank.com/personal-banking/loans/personal-loan/service-charges"/>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-1 text-gray-700">{language === 'en' ? 'Website URL B' : 'ವೆಬ್‌ಸೈಟ್ URL B'}</label>
                                    <input type="url" value={urlB} onChange={(e) => setUrlB(e.target.value)} className="w-full p-2 border border-gray-300 rounded-lg" placeholder="https://www.hdfcbank.com/personal/borrow/popular-loans/personal-loan/fees-and-charges"/>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold mb-1 text-gray-700">{language === 'en' ? 'Your Initial Question' : 'ನಿಮ್ಮ ಆರಂಭಿಕ ಪ್ರಶ್ನೆ'}</label>
                                    <textarea value={initialPrompt} onChange={(e) => setInitialPrompt(e.target.value)} className="w-full p-2 border border-gray-300 rounded-lg" placeholder={language === 'en' ? 'e.g., Compare these two based on their pre-payment penalties...' : 'ಉದಾಹರಣೆಗೆ, ಇವುಗಳ ಪೂರ್ವ-ಪಾವತಿ ದಂಡಗಳನ್ನು ಹೋಲಿಕೆ ಮಾಡಿ...'} rows="2"/>
                                </div>
                                <div className="grid grid-cols-2 gap-2">
                                    {samplePrompts[language].map((prompt, index) => (
                                        <button key={index} onClick={() => setInitialPrompt(prompt)} className="text-xs text-left bg-gray-200 hover:bg-gray-300 p-2 rounded-lg transition-colors">{prompt}</button>
                                    ))}
                                </div>
                            </div>
                            <button onClick={handleProcessUrls} disabled={isProcessing || isGenerating} className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg disabled:bg-gray-400">
                                {isProcessing ? (language === 'en' ? 'Processing...' : 'ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ...') : (language === 'en' ? 'Process and Analyze URLs' : 'URL ಗಳನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಿ ಮತ್ತು ವಿಶ್ಲೇಷಿಸಿ')}
                            </button>
                        </>
                    )}
                </div>
                
                <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-200">
                    {ragConversation.length === 0 && !isProcessing && (
                        <div className="text-center text-gray-500 mt-10 p-4">
                            <i className="fas fa-file-alt text-4xl mb-4"></i>
                            <p className="text-lg">{language === 'en' ? 'Enter two URLs and ask a question to begin.' : 'ಎರಡು URL ಗಳನ್ನು ನಮೂದಿಸಿ ಮತ್ತು ಪ್ರಾರಂಭಿಸಲು ಒಂದು ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ.'}</p>
                        </div>
                    )}
                    {ragConversation.map((msg, index) => (
                        <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-3xl p-4 rounded-xl shadow-md ${ msg.sender === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white text-gray-800 rounded-bl-none border' }`}>
                                <div dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br />') }} />
                            </div>
                        </div>
                    ))}
                    {isGenerating && <div className="text-center text-gray-500 p-4">{language === 'en' ? 'Generating answer...' : 'ಉತ್ತರವನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...'}</div>}
                    <div ref={ragChatEndRef} />
                </div>
                
                {/* --- CHANGE 2: NEW FOLLOW-UP FORM WITH VOICE INPUT --- */}
                {sessionId && (
                    <div className="p-4 bg-white border-t flex-shrink-0">
                        <form
                            onSubmit={(e) => {
                                e.preventDefault();
                                handleRagQuestionSubmit(sessionId, ragInput);
                            }}
                            className="flex items-center space-x-4 max-w-3xl mx-auto"
                        >
                            <input
                                type="text"
                                value={ragInput}
                                onChange={(e) => setRagInput(e.target.value)}
                                className="flex-1 p-3 border border-gray-300 rounded-lg"
                                placeholder={language === 'en' ? 'Ask a follow-up question...' : 'ಮುಂದಿನ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ...'}
                                disabled={isGenerating || isProcessing}
                            />
                            <button 
                                type="button" 
                                onClick={handleVoiceInput} 
                                title="Voice Input"
                                className={`p-3 rounded-lg text-white transition-colors ${isListening ? 'bg-red-600 animate-pulse' : 'bg-purple-600 hover:bg-purple-700'}`}
                                disabled={!isVoiceSupported || isGenerating || isProcessing}
                            >
                                <i className="fas fa-microphone text-xl"></i>
                            </button>
                            <button
                                type="submit"
                                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg disabled:bg-gray-400"
                                disabled={isGenerating || isProcessing || !ragInput.trim()}
                            >
                                {language === 'en' ? 'Ask' : 'ಕೇಳಿ'}
                            </button>
                        </form>
                    </div>
                )}
            </div>
        );
      
      case 'history':
        return (
          <div className="flex flex-col items-center justify-start h-full p-6 text-gray-700 bg-white rounded-lg shadow-inner overflow-y-auto">
            <h2 className="text-3xl font-bold text-gray-800 mb-6 mt-4">{language === 'en' ? 'Your Chat History' : 'ನಿಮ್ಮ ಚಾಟ್ ಇತಿಹಾಸ'}</h2>
            <div className="w-full max-w-3xl bg-gray-50 p-6 rounded-xl shadow-md border border-gray-200 mb-4">
              <div className="flex justify-end items-center mb-4">
                <button className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg shadow transition duration-200 ease-in-out" onClick={handleClearHistory}>{language === 'en' ? 'Clear History' : 'ಇತಿಹಾಸ ಅಳಿಸಿ'}</button>
              </div>
              {historicalMessages.length === 0 ? (<p className="text-lg text-gray-500 text-center py-8">{language === 'en' ? 'No chat history available.' : 'ಚಾಟ್ ಇತಿಹಾಸ ಲಭ್ಯವಿಲ್ಲ.'}</p>) : (
                <div className="overflow-y-auto max-h-[calc(100vh-300px)] custom-scrollbar">
                  {historicalMessages.map((msg) => (
                    <div key={msg.id} className={`mb-4 last:mb-0 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
                        <div className={`inline-block p-3 rounded-lg max-w-[80%] ${msg.sender === 'user' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}>
                          <p className="text-sm font-medium mb-1">{msg.message}</p>
                          <span className="text-xs text-gray-500">{formatDisplayTimestamp(msg.timestamp)}</span>
                        </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );
      
      case 'account':
        return (
          <div className="flex flex-col items-center justify-start h-full p-6 text-gray-700 bg-gray-100 rounded-lg shadow-inner overflow-y-auto">
            <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md border border-gray-200">
              <div className="flex items-center space-x-4 pb-6 border-b border-gray-200 mb-6">
                <div className="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center text-white text-3xl font-bold">{username ? username.charAt(0).toUpperCase() : 'F'}</div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">{language === 'en' ? `Hi, ${username}!` : `ನಮಸ್ಕಾರ, ${username}!`}</h3>
                  <p className="text-gray-600">{email || `${username}@finease.example.com`}</p>
                  <button className="mt-2 text-blue-600 hover:underline text-sm">{language === 'en' ? 'Manage your Finease Account' : 'ನಿಮ್ಮ ಫಿನೀಸ್ ಖಾತೆಯನ್ನು ನಿರ್ವಹಿಸಿ'}</button>
                </div>
              </div>
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">{language === 'en' ? 'Other Accounts' : 'ಇತರ ಖಾತೆಗಳು'}</h3>
                <div className="space-y-4">
                  {linkedAccounts.map(account => (<div key={account.id} className="flex items-center justify-between p-3 bg-gray-100 rounded-lg border border-gray-200"><div className="flex items-center space-x-3"><div className="w-10 h-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold text-lg">{account.name.charAt(0)}</div><div><p className="font-medium text-gray-800">{account.name}</p><p className="text-sm text-gray-600">{account.email}</p></div></div><div className="flex space-x-2">{account.status === 'signed out' ? (<button className="bg-blue-500 hover:bg-blue-600 text-white text-sm py-1 px-3 rounded-lg" onClick={() => handleLinkedAccountSignIn(account.id)}>{language === 'en' ? 'Sign in' : 'ಸೈನ್ ಇನ್ ಮಾಡಿ'}</button>) : (<span className="text-green-600 text-sm font-semibold">{language === 'en' ? 'Active' : 'ಸಕ್ರಿಯ'}</span>)}<button className="bg-red-500 hover:bg-red-600 text-white text-sm py-1 px-3 rounded-lg" onClick={() => handleLinkedAccountRemove(account.id)}>{language === 'en' ? 'Remove' : 'ತೆಗೆದುಹಾಕಿ'}</button></div></div>))}
                </div>
              </div>
              <div className="space-y-3 pt-6 border-t border-gray-200">
                <button className="w-full flex items-center justify-center bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-4 rounded-lg"><i className="fas fa-plus mr-2"></i> {language === 'en' ? 'Add another account' : 'ಇನ್ನೊಂದು ಖಾತೆ ಸೇರಿಸಿ'}</button>
                <button className="w-full flex items-center justify-center bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-4 rounded-lg" onClick={handleSignOut}><i className="fas fa-sign-out-alt mr-2"></i> {language === 'en' ? 'Sign out of all accounts' : 'ಎಲ್ಲಾ ಖಾತೆಗಳಿಂದ ಸೈನ್ ಔಟ್ ಮಾಡಿ'}</button>
              </div>
            </div>
          </div>
        );

      case 'chat':
      default:
        return (
          <div className="flex flex-col h-full bg-gray-50">
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {faqMessages.length === 0 ? (
                <div className="text-center text-gray-500 mt-10">
                    <div className="mb-8">{language === 'en' ? 'Welcome! Ask me a general financial question, or try one of these:' : 'ಸ್ವಾಗತ! ಸಾಮಾನ್ಯ ಹಣಕಾಸಿನ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ, ಅಥವಾ ಇವುಗಳಲ್ಲಿ ಒಂದನ್ನು ಪ್ರಯತ್ನಿಸಿ:'}</div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                        {sampleFaqQuestions.map((q, index) => (
                            <button 
                                key={index} 
                                onClick={() => handleSampleQuestionClick(q[language])}
                                className="bg-white hover:bg-blue-50 text-blue-600 font-semibold p-4 rounded-lg border border-blue-200 shadow-sm transition-all duration-200 text-left"
                                disabled={isFaqSending}
                            >
                                {q[language]}
                            </button>
                        ))}
                    </div>
                </div>
              ) : (
                faqMessages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-2xl p-4 rounded-xl shadow-md ${ msg.sender === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-gray-200 text-gray-800 rounded-bl-none' }`}>
                      {msg.message}
                    </div>
                  </div>
                ))
              )}
              <div ref={faqChatEndRef} />
            </div>
            <form onSubmit={handleFaqSendMessage} className="p-4 bg-white border-t">
              <div className="flex items-center space-x-4 max-w-3xl mx-auto">
                <input type="text" value={faqInput} onChange={(e) => setFaqInput(e.target.value)} className="flex-1 p-3 border rounded-lg" placeholder={language === 'en' ? 'Ask any finance related questions...' : 'ಯಾವುದೇ ಹಣಕಾಸು ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ...'} disabled={isFaqSending} />
                
                <button 
                  type="button" 
                  onClick={handleVoiceInput} 
                  title="Voice Input"
                  className={`p-3 rounded-lg text-white transition-colors ${isListening ? 'bg-red-600 animate-pulse' : 'bg-purple-600 hover:bg-purple-700'}`}
                  disabled={!isVoiceSupported || isFaqSending}
                >
                  <i className="fas fa-microphone text-xl"></i>
                </button>

                <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg disabled:bg-gray-400" disabled={isFaqSending || !faqInput.trim()}>Send</button>
              </div>
            </form>
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 font-inter">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
      <div className="w-64 bg-gray-900 text-white flex flex-col shadow-2xl">
        <div className="p-6 flex justify-center items-center border-b border-gray-700">
            <img src="/finease-removebg-preview-new.png" alt="Finease Logo" className="logo" />
        </div>
        <nav className="flex-1 p-4 space-y-3">
          {isLoggedIn && (
            <>
              <button className={`w-full text-left py-3 px-4 rounded-lg flex items-center ${activeView === 'chat' ? 'bg-blue-700' : 'hover:bg-gray-700'}`} onClick={() => setActiveView('chat')}>
                <i className="fas fa-comment-dots text-xl mr-3"></i> <span className="text-lg">{language === 'en' ? 'FAQ Chat' : 'ಪ್ರಶ್ನೋತ್ತರ ಚಾಟ್'}</span>
              </button>
              <button className={`w-full text-left py-3 px-4 rounded-lg flex items-center ${activeView === 'compare' ? 'bg-blue-700' : 'hover:bg-gray-700'}`} onClick={() => setActiveView('compare')}>
                <i className="fas fa-balance-scale-right text-xl mr-3"></i> <span className="text-lg">{language === 'en' ? 'Analyze URLs' : 'URL ವಿಶ್ಲೇಷಿಸಿ'}</span>
              </button>
              <button className={`w-full text-left py-3 px-4 rounded-lg flex items-center ${activeView === 'history' ? 'bg-blue-700' : 'hover:bg-gray-700'}`} onClick={() => setActiveView('history')}>
                <i className="fas fa-history text-xl mr-3"></i> <span className="text-lg">{language === 'en' ? 'History' : 'ಇತಿಹಾಸ'}</span>
              </button>
              <button className={`w-full text-left py-3 px-4 rounded-lg flex items-center ${activeView === 'account' ? 'bg-blue-700' : 'hover:bg-gray-700'}`} onClick={() => setActiveView('account')}>
                <i className="fas fa-user-circle text-xl mr-3"></i> <span className="text-lg">{language === 'en' ? 'Account' : 'ಖಾತೆ'}</span>
              </button>
              <button onClick={handleLanguageToggle} className="mt-4 w-full text-left py-2 px-4 rounded-lg flex items-center justify-center font-semibold bg-gray-600 hover:bg-gray-500">
                <i className="fas fa-language text-xl mr-2"></i>{language === 'en' ? 'ಕನ್ನಡ' : 'English'}
              </button>
            </>
          )}
        </nav>
        <div className="p-4 border-t border-gray-700">
          <button className={`w-full flex items-center justify-center font-semibold text-lg py-3 px-4 rounded-lg ${isLoggedIn ? 'bg-red-700 hover:bg-red-800' : 'bg-green-700 hover:bg-green-800'}`} onClick={isLoggedIn ? handleSignOut : () => { setIsSigningUp(false); setActiveView('auth');}}>
            <i className={`fas ${isLoggedIn ? 'fa-sign-out-alt' : 'fa-sign-in-alt'} mr-3`}></i>{isLoggedIn ? (language === 'en' ? 'Sign Out' : 'ಸೈನ್ ಔಟ್') : 'Login'}
          </button>
        </div>
      </div>
      <div className="flex-1 flex flex-col bg-gray-100">{renderContent()}</div>
    </div>
  );
}

export default App;