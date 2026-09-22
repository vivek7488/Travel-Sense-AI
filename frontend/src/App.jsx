function App() {
  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-white mb-4">
          🌍 TravelSense AI
        </h1>
        <p className="text-blue-400 text-xl mb-8">
          Intelligent Travel Experience Analyzer
        </p>
        <div className="bg-gray-800 rounded-xl p-6 max-w-md mx-auto">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-3 h-3 rounded-full bg-green-400"></div>
            <span className="text-green-400 font-medium">Scaffold only</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-green-400"></div>
            <span className="text-green-400 font-medium">API lives in backend/</span>
          </div>
        </div>
        <p className="text-gray-500 mt-6 text-sm">
          Web UI not built yet — see the README roadmap. Use the API at :8001/docs.
        </p>
      </div>
    </div>
  )
}

export default App