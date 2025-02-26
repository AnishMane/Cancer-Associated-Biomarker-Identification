import requests
from bs4 import BeautifulSoup
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_table_data(soup):
    tables = []
    for table in soup.find_all('table'):
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if cells:  # Only add rows that have cells
                rows.append(cells)
        if headers:  # If the table has headers, include them in the output
            tables.append({"headers": headers, "rows": rows})
        else:
            tables.append({"rows": rows})  # Append rows only if no headers

    return tables

def extract_text_content(url, biology_keywords):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }

    try:
        # Fetch the content from the URL with custom headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove unwanted tags like scripts, styles, etc.
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        # Extract the headline information
        headline_content = {
            "title": soup.title.string if soup.title else "",
            "h1": [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
            "h2": [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
        }

        # Extract biology-related paragraphs
        biology_paragraphs = set()
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div']):
            text_content = element.get_text(strip=True)
            if any(keyword.lower() in text_content.lower() for keyword in biology_keywords):
                biology_paragraphs.add(text_content)

        # Extract table data
        tables = extract_table_data(soup)

        # Create a dictionary with the extracted content
        result = {
            "url": url,
            "headline": headline_content,
            "biology_paragraphs": list(biology_paragraphs),
            "tables": tables
        }

        logging.info(f"Content from {url} extracted successfully.")
        return result

    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred for {url}: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred for {url}: {err}")
    return None

def extract_from_url(url, output_file='extracted_content.json', retries=3):
    biology_keywords = [
        'cancer', 'tumor', 'malignant', 'carcinoma', 'oncology', 'chemotherapy', 'radiation',
        'immunotherapy', 'biopsy', 'oncologist', 'gene', 'cell', 'DNA', 'RNA', 'chromosome',
        'genetic', 'mutation', 'protein', 'enzyme', 'tissue', 'microorganism', 'bacteria',
        'virus', 'immune', 'pathogen', 'bioinformatics', 'stem cell', 'neuroscience',
        'biomarker', 'apoptosis', 'metastasis', 'carcinogenesis', 'tumorigenesis',
        'clinical trial', 'biotechnology', 'genomics', 'proteomics', 'metabolomics', 'CRISPR',
        'genome', 'transcription', 'translation', 'ribosome', 'epigenetics', 'mRNA', 'microRNA',
        'therapeutics', 'vaccination', 'immunology', 'lymphocyte', 'antibody', 'cytokine',
        'pathophysiology', 'organism', 'microbiome', 'antigen', 'cellular', 'cell signaling',
        'genetic engineering', 'transgenic', 'virology', 'mycology', 'botany', 'zoology',
        'ecology', 'endocrinology', 'neurobiology', 'physiology', 'toxicology', 'pharmacology',
        'biochemistry', 'cell culture', 'bioethics', 'phytochemistry', 'ethology',
        'biomechanics', 'forensics', 'molecular biology', 'molecular genetics', 'synthetic biology',
        'neoplasm', 'leukemia', 'lymphoma', 'sarcoma', 'immunogenetics', 'signal transduction',
        'nucleic acid', 'receptor', 'angiogenesis', 'oncogene', 'tumor suppressor',
        'metabolic syndrome', 'biophysics', 'pharmacogenomics', 'genetic predisposition',
        'stem cell therapy', 'gene therapy', 'cell differentiation', 'tissue engineering',
        'regenerative medicine', 'chronic disease', 'autoimmunity', 'infection', 'pathology',
        'histology', 'phytotherapy', 'genetic diversity', 'population genetics', 'comparative genomics',
        'microbial ecology', 'environmental biology', 'behavioral biology', 'ethnobotany',
        'marine biology', 'evolutionary biology', 'cell cycle', 'mitosis', 'meiosis',
        'fetal development', 'stemness', 'biostatistics', 'clinical pharmacology', 'nutrigenomics',
        'therapeutic antibodies', 'cell death', 'neurodegeneration', 'vascular biology',
        'endothelial cells', 'gene expression', 'protein folding', 'molecular chaperones',
        'transcription factors', 'chromatin remodeling', 'biomolecular engineering',
        'tissue homeostasis', 'population dynamics', 'invasive species', 'symbiosis',
        'biogeography', 'gene mapping', 'genetic counseling', 'genome editing', 'sustainable agriculture',
        'biopreservation', 'environmental genomics', 'quantum biology', 'agrobiology', 'astrobiology',
        'ecotoxicology', 'metagenomics', 'pathogenomics', 'viromics', 'phylodynamics',
        'synthetic genomics', 'cellular metabolism', 'neuroplasticity', 'translational research',
        'drug discovery', 'molecular diagnostics', 'biological rhythms', 'physiological stress',
        'bioengineering', 'transcriptional regulation', 'cellular communication', 'cytoskeleton',
        'viral oncology', 'host-pathogen interactions', 'nutritional genomics', 'biome',
        'ecosystem', 'biogeochemical cycles', 'organogenesis', 'telomere', 'extracellular matrix',
        'cellular respiration', 'glycolysis', 'apoptosome', 'autophagy', 'thermoregulation',
        'homeostasis'
    ]

    for attempt in range(retries):
        result = extract_text_content(url, biology_keywords)
        if result:
            # Save result to the output JSON file
            with open(output_file, 'w') as output_json:
                json.dump(result, output_json, indent=4)
            logging.info(f"Content from {url} extracted and saved to '{output_file}'.")
            break
        elif attempt < retries - 1:
            logging.info(f"Retrying {url} (Attempt {attempt + 2}/{retries})")
            time.sleep(2)  # Wait for 2 seconds before retrying
        else:
            logging.error(f"Failed to extract content from {url} after {retries} attempts.")

if __name__ == "__main__":
    url ="https://www.mdpi.com/1422-0067/24/9/7781"
    output_file = input("Enter the output JSON filename (default: 'extracted_content.json'): ") or 'extracted_content.json'
    extract_from_url(url, output_file)
