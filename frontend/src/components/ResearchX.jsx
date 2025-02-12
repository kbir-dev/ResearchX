import React, { useState, useEffect } from 'react';
import { SearchIcon, Download, FileText, BookOpen, Loader2, Sparkles } from 'lucide-react';
import LoadingState from './LoadingState';

const BackgroundPattern = () => (
  <div className="absolute inset-0 overflow-hidden">
    {/* Grid Pattern */}
    <div className="absolute inset-0 bg-[linear-gradient(to_right,#232338_1px,transparent_1px),linear-gradient(to_bottom,#232338_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_80%_at_50%_50%,black_20%,transparent_100%)]" />
    
    {/* Gradient Orbs */}
    <div className="absolute top-[20%] left-[20%] w-[40rem] h-[40rem] bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
    <div className="absolute bottom-[10%] right-[10%] w-[30rem] h-[30rem] bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-700" />
    
    {/* Animated Dots */}
    <div className="absolute inset-0">
      {Array.from({ length: 50 }).map((_, i) => (
        <div
          key={i}
          className="absolute w-1 h-1 bg-indigo-400/20 rounded-full animate-float"
          style={{
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${5 + Math.random() * 5}s`
          }}
        />
      ))}
    </div>
  </div>
);

const ResearchX = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [papers, setPapers] = useState([]);
  const [synopsis, setSynopsis] = useState(null);
  const [error, setError] = useState(null);
  const [loadingSteps, setLoadingSteps] = useState([
    { label: 'Initializing search...', active: false, completed: false },
    { label: 'Fetching research papers...', active: false, completed: false },
    { label: 'Analyzing papers...', active: false, completed: false },
    { label: 'Generating title...', active: false, completed: false },
    { label: 'Writing introduction...', active: false, completed: false },
    { label: 'Creating synopsis...', active: false, completed: false },
  ]);

  // Function to update loading steps
  const updateLoadingStep = (index, active = true, completed = false) => {
    setLoadingSteps(steps =>
      steps.map((step, i) => {
        if (i === index) return { ...step, active, completed };
        if (i < index) return { ...step, active: false, completed: true };
        return { ...step, active: false, completed: false };
      })
    );
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setPapers([]);
    setSynopsis(null);
    
    try {
      // Update loading state for paper fetch
      updateLoadingStep(0, true);
      updateLoadingStep(1, true);

      // First, fetch papers
      console.log('Making API call to fetch papers:', `${import.meta.env.VITE_BACKEND_URL}/fetch-papers/`);
      
      const fetchResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}/fetch-papers/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          max_results: 10
        }),
      });
      
      if (!fetchResponse.ok) {
        const errorData = await fetchResponse.json().catch(() => ({ detail: 'Failed to fetch papers' }));
        throw new Error(errorData.detail || `HTTP error! status: ${fetchResponse.status}`);
      }
      
      const fetchData = await fetchResponse.json();
      console.log('Fetch Papers Response:', fetchData);
      
      if (!fetchData.papers || !Array.isArray(fetchData.papers)) {
        throw new Error('Invalid response format from server');
      }
      
      setPapers(fetchData.papers);
      
      // Then, analyze papers
      updateLoadingStep(2, true);
      console.log('Making API call to analyze papers:', `${import.meta.env.VITE_BACKEND_URL}/analyze-papers/`);
      
      const analyzeResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}/analyze-papers/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          max_results: 10
        }),
      });
      
      if (!analyzeResponse.ok) {
        const errorData = await analyzeResponse.json().catch(() => ({ detail: 'Failed to analyze papers' }));
        throw new Error(errorData.detail || `HTTP error! status: ${analyzeResponse.status}`);
      }
      
      const analyzeData = await analyzeResponse.json();
      console.log('Analyze Papers Response:', analyzeData);
      
      if (!analyzeData.synopsis) {
        throw new Error('No synopsis generated');
      }
      
      setSynopsis(analyzeData.synopsis);
      setLoadingSteps(steps => steps.map(step => ({ ...step, active: false, completed: true })));
      
    } catch (error) {
      console.error('Search error:', error);
      setError(error.message || 'An unexpected error occurred');
      setLoadingSteps(steps => steps.map(step => ({ ...step, active: false, completed: false })));
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadCSV = async () => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/download/${encodeURIComponent('csv')}/${encodeURIComponent(searchQuery)}`
      );

      if (!response.ok) {
        throw new Error('Failed to get CSV download path');
      }

      const data = await response.json();
      window.location.href = `${import.meta.env.VITE_BACKEND_URL}/${data.path}`;
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    }
  };

  const handleDownloadWord = async () => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/download/${encodeURIComponent('docx')}/${encodeURIComponent(searchQuery)}`
      );

      if (!response.ok) {
        throw new Error('Failed to get Word document download path');
      }

      const data = await response.json();
      window.location.href = `${import.meta.env.VITE_BACKEND_URL}/${data.path}`;
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#0F0F1A] text-white overflow-hidden font-sans">
      <BackgroundPattern />
      
      {/* Main Content */}
      <div className="relative container mx-auto px-4 py-16 max-w-7xl">
        {/* Enhanced Header */}
        <div className="text-center mb-16 p-8 rounded-3xl backdrop-blur-sm bg-white/5 border border-white/10 max-w-3xl mx-auto transform hover:scale-[1.01] transition-all duration-300">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-12 h-12 text-indigo-400 animate-pulse" />
          </div>
          <h1 className="text-7xl font-bold mb-3 bg-gradient-to-r from-purple-400 via-indigo-400 to-blue-400 bg-clip-text text-transparent tracking-tight animate-gradient">
            ResearchX
          </h1>
          <p className="text-gray-400 text-xl font-light tracking-wide">
            Explore Research Papers with AI Intelligence
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/50 via-indigo-500/50 to-blue-500/50 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="What would you like to research?"
              className="relative w-full px-8 py-5 rounded-xl bg-gray-900/90 border border-white/10 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-white placeholder-gray-400 backdrop-blur-sm font-light text-lg"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-3 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-lg hover:from-purple-600 hover:to-indigo-600 transition-all duration-300 shadow-lg disabled:opacity-50"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 text-white animate-spin" />
              ) : (
                <SearchIcon className="w-5 h-5 text-white" />
              )}
            </button>
          </div>
        </form>

        {/* Enhanced Error Message */}
        {error && (
          <div className="mt-8 text-center backdrop-blur-sm bg-red-900/20 rounded-lg p-6 max-w-3xl mx-auto border border-red-500/20">
            <div className="flex items-center justify-center space-x-2 text-red-400">
              <span className="font-medium">{error}</span>
            </div>
          </div>
        )}

        {/* Enhanced Loading State */}
        {isLoading && <LoadingState loadingSteps={loadingSteps} />}

        {/* Results Section */}
        {papers.length > 0 && !isLoading && (
          <div className="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl mx-auto">
            {/* Papers Section - Left Side */}
            <div className="backdrop-blur-sm bg-gray-900/80 rounded-2xl p-8 border border-white/10 hover:border-indigo-500/30 transition-all duration-300">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center space-x-3">
                  <BookOpen className="text-indigo-400 w-6 h-6" />
                  <h2 className="text-2xl font-semibold tracking-tight">Research Papers</h2>
                </div>
                <button
                  onClick={handleDownloadCSV}
                  className="flex items-center space-x-2 px-4 py-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors border border-white/10"
                >
                  <Download className="w-4 h-4 text-indigo-400" />
                  <span className="font-light">Download CSV</span>
                </button>
              </div>
              <div className="space-y-4 max-h-[800px] overflow-y-auto">
                {papers.map((paper, index) => (
                  <div key={index} className="p-6 bg-white/5 rounded-xl hover:bg-white/10 transition-colors border border-white/5">
                    <h3 className="font-medium mb-2 text-lg">{paper.Title}</h3>
                    <p className="text-gray-400 font-light leading-relaxed">
                      {paper.Abstract}
                    </p>
                    <div className="mt-4 text-sm text-gray-500">
                      <span>{paper.Authors} • {paper.Year}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Synopsis Section - Right Side */}
            {synopsis && (
              <div className="backdrop-blur-sm bg-gray-900/80 rounded-2xl p-8 border border-white/10 hover:border-indigo-500/30 transition-all duration-300">
                <div className="flex justify-between items-center mb-6">
                  <div className="flex items-center space-x-3">
                    <FileText className="text-indigo-400 w-6 h-6" />
                    <h2 className="text-2xl font-semibold tracking-tight">AI Generated Synopsis</h2>
                  </div>
                  <button
                    onClick={handleDownloadWord}
                    className="flex items-center space-x-2 px-4 py-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors border border-white/10"
                  >
                    <FileText className="w-4 h-4 text-indigo-400" />
                    <span className="font-light">Download Word</span>
                  </button>
                </div>
                <div className="prose prose-invert max-w-none max-h-[800px] overflow-y-auto">
                  {/* Title */}
                  <h1 className="text-3xl font-bold mb-6">{synopsis.title}</h1>

                  {/* Introduction */}
                  <h2 className="text-2xl font-semibold mt-8 mb-4">Introduction</h2>
                  <p className="mb-6">{synopsis.introduction}</p>

                  {/* Rationale */}
                  <h3 className="text-xl font-semibold mt-6 mb-3">Rationale</h3>
                  <p className="mb-6">{synopsis.rationale}</p>

                  {/* Objectives */}
                  <h3 className="text-xl font-semibold mt-6 mb-3">Objectives</h3>
                  <p className="mb-6">{synopsis.objectives}</p>

                  {/* Literature Review */}
                  <h2 className="text-2xl font-semibold mt-8 mb-4">Literature Review</h2>
                  <p className="mb-6">{synopsis.literature_review}</p>

                  {/* Feasibility Study */}
                  <h2 className="text-2xl font-semibold mt-8 mb-4">Feasibility Study</h2>
                  <p className="mb-6">{synopsis.feasibility}</p>

                  {/* Methodology */}
                  <h2 className="text-2xl font-semibold mt-8 mb-4">Methodology</h2>
                  <p className="mb-6">{synopsis.methodology}</p>

                  {/* Facilities */}
                  <h2 className="text-2xl font-semibold mt-8 mb-4">Facilities Required</h2>
                  <p className="mb-6">{synopsis.facilities}</p>

                  {/* Outcomes */}
                  <h2 className="text-2xl font-semibold mt-8 mb-4">Expected Outcomes</h2>
                  <p className="mb-6">{synopsis.outcomes}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResearchX;