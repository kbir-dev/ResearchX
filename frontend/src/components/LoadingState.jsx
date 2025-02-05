import { Loader2 } from 'lucide-react';

const LoadingState = ({ loadingSteps }) => {
  return (
    <div className="mt-12 backdrop-blur-sm bg-white/5 rounded-2xl p-8 border border-white/10 max-w-2xl mx-auto">
      <div className="flex items-center justify-center mb-8">
        <div className="relative">
          <Loader2 className="w-16 h-16 animate-spin text-indigo-400" />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-12 h-12 rounded-full bg-indigo-500/20"></div>
          </div>
        </div>
      </div>
      
      <div className="space-y-4">
        {loadingSteps.map((step, index) => (
          <div
            key={index}
            className={`flex items-center space-x-3 transition-all duration-500 ${
              step.active ? 'text-white' : 'text-gray-500'
            }`}
          >
            <div
              className={`w-2 h-2 rounded-full ${
                step.active
                  ? 'bg-indigo-400 animate-pulse'
                  : step.completed
                  ? 'bg-green-400'
                  : 'bg-gray-600'
              }`}
            />
            <span className={`font-light ${step.completed && 'text-green-400'}`}>
              {step.label}
              {step.completed && ' ✓'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LoadingState; 