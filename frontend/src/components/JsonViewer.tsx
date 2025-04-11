
import React, { useState } from "react";
import { ChevronDown, ChevronRight, Copy } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

interface JsonViewerProps {
  data: any;
  rootName?: string;
  expanded?: boolean;
}

const JsonViewer: React.FC<JsonViewerProps> = ({ 
  data, 
  rootName = "root", 
  expanded = false 
}) => {
  const [isExpanded, setIsExpanded] = useState(expanded);
  
  const copyToClipboard = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2))
      .then(() => toast.success("JSON copied to clipboard"))
      .catch(() => toast.error("Failed to copy"));
  };
  
  if (data === null) return <span className="text-gray-500">null</span>;
  if (data === undefined) return <span className="text-gray-500">undefined</span>;
  
  const dataType = Array.isArray(data) ? "array" : typeof data;
  
  if (dataType === "object" || dataType === "array") {
    const keys = Object.keys(data);
    const isEmpty = keys.length === 0;
    
    return (
      <div className="font-mono text-sm">
        <div className="flex items-center gap-1">
          {!isEmpty && (
            <button 
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-1 hover:bg-gray-100 rounded"
            >
              {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </button>
          )}
          <span className="font-semibold">{rootName}</span>
          <span className="text-gray-500 text-xs">
            {dataType === "array" ? `[${keys.length}]` : `{${keys.length}}`}
          </span>
          
          <button 
            onClick={copyToClipboard} 
            className="ml-2 p-1 hover:bg-gray-100 rounded"
            title="Copy to clipboard"
          >
            <Copy size={14} />
          </button>
        </div>
        
        {!isEmpty && isExpanded && (
          <div className="pl-6 border-l border-gray-200 ml-2 mt-1">
            {keys.map((key) => (
              <div key={key} className="mt-1">
                <JsonViewer 
                  data={data[key]} 
                  rootName={key} 
                />
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }
  
  // For primitive values
  return (
    <div className="font-mono text-sm flex">
      <span className="font-semibold mr-2">{rootName}:</span>
      <span className={cn(
        dataType === "string" && "text-green-600",
        dataType === "number" && "text-blue-600",
        dataType === "boolean" && "text-purple-600"
      )}>
        {dataType === "string" ? `"${data}"` : String(data)}
      </span>
    </div>
  );
};

export default JsonViewer;
