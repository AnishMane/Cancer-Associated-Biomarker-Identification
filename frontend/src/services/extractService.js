// extractionService.js
import axios from 'axios';

export const extractBiologyInfo = async (url) => {
  try {
    // You would replace this with your actual API endpoint
    const response = await axios.post('http://localhost:5000/api/extract', { url });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to extract information');
  }
};

// Function to download JSON as a file
export const downloadAsJson = (data, filename = 'extracted_content.json') => {
  // Create a blob of the data
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  
  // Create an anchor element and dispatch a click event
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  
  // Append to the DOM, click and remove
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  // Free up memory by revoking the object URL
  setTimeout(() => URL.revokeObjectURL(link.href), 100);
};