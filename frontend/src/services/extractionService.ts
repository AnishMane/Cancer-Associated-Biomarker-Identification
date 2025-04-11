
interface ExtractionRequest {
  url: string;
}

interface ExtractionResponse {
  data: any;
}

export async function extractBiologyInfo(url: string): Promise<any> {
  try {
    const response = await fetch("/extract", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        errorData?.message || errorData?.error || `Error: ${response.status} ${response.statusText}`
      );
    }
    
    return await response.json();
  } catch (error) {
    console.error("Extraction error:", error);
    throw error;
  }
}
