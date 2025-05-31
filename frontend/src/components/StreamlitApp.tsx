import React from 'react';
import { getStreamlitUrl } from '../services/api';

interface StreamlitAppProps {
  className?: string;
}

export const StreamlitApp: React.FC<StreamlitAppProps> = ({ className }) => {
  const streamlitUrl = getStreamlitUrl();

  return (
    <div className={`w-full h-full ${className}`}>
      <iframe
        src={streamlitUrl}
        title="ML Analysis"
        className="w-full h-full border-0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      />
    </div>
  );
};

export default StreamlitApp; 