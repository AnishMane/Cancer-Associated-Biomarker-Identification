
# Biology Information Extractor API

A Flask-based API that extracts biology-related information from web pages.

## Features

- Extracts biology information from provided URLs
- Parses HTML content using BeautifulSoup
- Filters content based on biology-related keywords
- Returns structured JSON with extracted information

## Installation

### Local Development

1. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```
   python app.py
   ```

### Docker

Build and run with Docker:

```
docker build -t biology-extractor .
docker run -p 5000:5000 biology-extractor
```

## API Usage

### Extract Biology Information

**Endpoint:** `POST /extract`

**Request Body:**
```json
{
  "url": "https://example.com/biology-article"
}
```

**Response:**
```json
{
  "title": "Article Title",
  "headlines": {
    "h1": ["Main Headline"],
    "h2": ["Subheading 1", "Subheading 2"]
  },
  "biology_paragraphs": [
    "This paragraph contains biology-related content...",
    "Another paragraph about cells and DNA..."
  ],
  "tables": [
    {
      "headers": ["Column 1", "Column 2"],
      "rows": [
        ["Data 1", "Data 2"],
        ["Data 3", "Data 4"]
      ]
    }
  ]
}
```

## Error Handling

The API provides appropriate error responses with status codes:

- `400 Bad Request`: Missing URL parameter
- `500 Internal Server Error`: Issues with fetching the URL or parsing content
