import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, AlertCircle, Link, Download } from "lucide-react";
import { toast } from "sonner";
import JsonViewer from "./JsonViewer";
import { extractBiologyInfo, downloadAsJson } from "@/services/extractService";
import { isValidUrl, isUrlEmpty } from "@/lib/validations";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";

const BiologyExtractor: React.FC = () => {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);
  const [isOpen, setIsOpen] = useState(true);
  
  const handleExtract = async () => {
    setError(null);
    setResult(null);
  
    if (isUrlEmpty(url)) {
      setError("Please enter a URL");
      return;
    }
  
    if (!isValidUrl(url)) {
      setError("Please enter a valid URL");
      return;
    }
  
    try {
      setIsLoading(true);
  
      const response = await fetch("http://localhost:5000/api/extract", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
      });
  
      const data = await response.json();
  
      if (data.redirect_url) {
        toast.success("Redirecting to annotated Streamlit view...");
        window.location.href = data.redirect_url; // 👈 Redirect to Streamlit app
      } else {
        setError("Extraction succeeded, but no redirect URL was provided.");
      }
  
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
      toast.error("Failed to extract biology information");
    } finally {
      setIsLoading(false);
    }
  };
  
  
  const handleDownload = () => {
    if (result) {
      downloadAsJson(result);
      toast.success("JSON file downloaded successfully!");
    }
  };
  
  return (
    <Card className="w-full max-w-2xl shadow-lg">
      <CardHeader className="border-b">
        <CardTitle className="text-biology">Cancer Biomarker Identification</CardTitle>
        <CardDescription>
          Paste an article URL to extract the information
        </CardDescription>
      </CardHeader>
      
      <CardContent className="pt-6">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-2 sm:flex-row">
            <div className="relative flex-grow">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                <Link size={18} />
              </div>
              <Input 
                type="url" 
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste article URL here"
                className="pl-10"
                disabled={isLoading}
              />
            </div>
            <Button 
              onClick={handleExtract}
              disabled={isLoading}
              className="bg-biology hover:bg-biology-dark"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Extracting...
                </>
              ) : (
                "Extract Biology Info"
              )}
            </Button>
          </div>
          
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          {result && (
            <div className="mt-4 rounded-md bg-gray-50 p-4">
              <Collapsible open={isOpen} onOpenChange={setIsOpen}>
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-gray-500">Results:</div>
                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      onClick={handleDownload}
                      className="flex items-center gap-1"
                    >
                      <Download className="h-4 w-4" />
                      Download JSON
                    </Button>
                    <CollapsibleTrigger asChild>
                      <Button variant="ghost" size="sm">
                        {isOpen ? "Collapse" : "Expand"}
                      </Button>
                    </CollapsibleTrigger>
                  </div>
                </div>
                <CollapsibleContent>
                  <JsonViewer data={result} expanded={true} />
                </CollapsibleContent>
              </Collapsible>
            </div>
          )}
        </div>
      </CardContent>
      
      {/* <CardFooter className="border-t bg-gray-50 text-xs text-gray-500">
        <p>This tool extracts Cancer  information from scientific articles and web pages.</p>
      </CardFooter> */}
    </Card>
  );
};

export default BiologyExtractor;