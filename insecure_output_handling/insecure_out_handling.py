import bleach
import html
from urllib.parse import quote
import json
import difflib

class InsecureOutputSanitizer:
    
    def __init__(self):
        """
        Allowed tags and allowed attributs for html sanitization is defined here
        """
        self.allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 
            'ol', 'strong', 'ul', 'p', 'br', 'div', 'span', 'h1', 'h2', 'h3', 
            'h4', 'h5', 'h6', 'img', 'table', 'th', 'tr', 'td'
        ]

        self.allowed_attributes = {
            'a': ['href', 'title'],
            'abbr': ['title'],
            'acronym': ['title'],
            'img': ['src', 'alt', 'title'],
            'table': ['border', 'cellpadding', 'cellspacing']
        }

    #HTML Encoding
    def html_encode(self, input_string):
        return html.escape(input_string)

    #CSS Encoding
    def css_encode(self, input_string):
        return input_string.translate(str.maketrans({
            '"': r'\0022',
            '\'': r'\0027',
            '>': r'\003E',
            '<': r'\003C',
            '&': r'\0026',
            '=': r'\003D'
        }))

    #URL Encoding
    def url_encode(self, input_string):
        return quote(input_string)

    #JS encoding
    def js_encode(self, input_string):
        return json.dumps(input_string)  

    #Final html sanitization
    def sanitize_html(self, input_string):
        return bleach.clean(input_string, tags=self.allowed_tags, attributes=self.allowed_attributes, strip=True)

    #Integrated all the encoding and sanitization
    def integrate_sanitization(self, input_string):
        sanitized_html = self.html_encode(input_string)
        encoded_url = self.url_encode(sanitized_html)
        encoded_css = self.css_encode(encoded_url)
        encoded_js = self.js_encode(encoded_css)
        final_html_sanitized = self.sanitize_html(encoded_js)
        return final_html_sanitized

    
    #For raw output text and sanitized output comparison
    def compare_texts(self, original, sanitized):
        differ = difflib.Differ()
        diff = list(differ.compare(original.splitlines(keepends=True), sanitized.splitlines(keepends=True)))
        changes = [line.strip() for line in diff if line.startswith('+ ') or line.startswith('- ')]
        return {
            'change_count': len(changes),
            'changes': changes
        }
    
    #For report of changes generation
    def generate_json_report(self, raw_output):
        sanitized = self.integrate_sanitization(raw_output)
        comparison = self.compare_texts(raw_output, sanitized)
        report = {
            'raw_content': raw_output,
            'sanitized_content': sanitized,
            'changes': comparison['changes'],
            'change_count': comparison['change_count']
        }
        return json.dumps(report, indent=4)


