# RegexAI 

**Convert English descriptions to regex patterns using AI**

Never write complex regex patterns manually again! RegexAI uses OpenAI's GPT-4 to transform plain English descriptions into production-ready regular expressions.

## Features

- **English to Regex** - Describe what you want in plain English
- **Instant Results** - Get regex patterns in seconds
- **Built-in Testing** - Validate patterns against test strings
- **Common Patterns** - Database of frequently used regex patterns
- **Pattern Explanation** - Understand what your regex does
- **Developer-Friendly** - Simple CLI that fits your workflow

## Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/SteliosSpanos/regex-ai.git
cd regex-ai

# Install dependencies
pip install -r requirements.txt
```

### Setup

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a `.env` file:

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Basic Usage

```bash
# Generate regex for email addresses
regexai "email addresses"

# Test a pattern against a string
regexai "phone numbers" --test "(555) 123-4567"

# Explain how a pattern works
regexai "URLs starting with https" --explain

# See the AI prompt (debug mode)
regexai "dates in MM/DD/YYYY format" --dry-run
```

## Examples

### Email Addresses
```bash
$ regexai "email addresses"

Generated Regex:
   ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

Explanation:
   Matches standard email addresses with alphanumeric characters, dots, underscores, plus signs and hyphens

Example matches:
   - user@example.com
   - test.email+tag@domain.co.uk
   - simple@test.org
```

### Phone Numbers with Testing
```bash
$ regexai "US phone numbers" --test "(555) 123-4567"

Generated Regex:
   ^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$

Explanation:
   Matches US phone numbers in various formats with optional parentheses and separators

Example matches:
   - (555) 123-4567
   - 555-123-4567
   - 555.123.4567

Testing: '(555) 123-4567'
   Match found!
   Captured groups: ('555', '123', '4567')
   Matched text: '(555) 123-4567'
```

### Complex Patterns
```bash
$ regexai "IPv4 addresses"
$ regexai "credit card numbers"
$ regexai "hexadecimal color codes"
$ regexai "URLs with query parameters"
$ regexai "social security numbers"
$ regexai "file paths on Windows"
```

## Common Use Cases

RegexAI excels at generating patterns for:

- **Email validation** - Various email formats
- **Phone numbers** - International and domestic formats  
- **URLs and domains** - Web addresses, protocols
- **Dates and times** - Multiple date formats
- **IP addresses** - IPv4, IPv6 patterns
- **File paths** - Unix, Windows paths
- **Credit cards** - Various card formats
- **Social security** - SSN patterns
- **ZIP codes** - US, international postal codes
- **Hexadecimal** - Colors, hashes, IDs

## Command Options

```bash
regexai "description" [OPTIONS]

Options:
  --test, -t TEXT     Test the regex against a string
  --explain, -e       Explain the regex pattern components  
  --dry-run, -d       Show AI prompt without making request
  --version, -v       Show version information
  --help, -h          Show help message
```

## Quick Patterns

For common patterns, RegexAI includes a built-in database for instant results:

- `regexai "email"` - Email addresses
- `regexai "phone"` - Phone numbers
- `regexai "url"` - Web URLs  
- `regexai "ip"` - IPv4 addresses
- `regexai "date"` - MM/DD/YYYY dates

## Advanced Usage

### Custom Descriptions
Be specific to get better results:

```bash
# Good: Specific and clear
regexai "email addresses with subdomains"
regexai "US phone numbers with area codes"
regexai "URLs starting with https only"

# Better: Include format details  
regexai "dates in YYYY-MM-DD format"
regexai "credit card numbers with spaces"
regexai "hexadecimal colors with # prefix"
```

### Testing Multiple Strings
```bash
# Test the generated pattern
regexai "email addresses" --test "user@example.com"
regexai "email addresses" --test "invalid-email"
regexai "email addresses" --test "test@sub.domain.org"
```

### Understanding Patterns
```bash
# Get explanation of regex components
regexai "complex date formats" --explain
```

## Development

### Setup Development Environment
```bash
git clone https://github.com/SteliosSpanos/regexai.git
cd regexai

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black regexai.py

# Lint code
flake8 regexai.py
```

### Project Structure
```
regexai/
├── regexai.py          # Main CLI application
├── requirements.txt    # Dependencies
├── pyproject.toml     # Package configuration
├── .env               # API key (create this)
├── README.md          # Documentation
```

## Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
```bash
# Create .env file with your API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Or set environment variable
export OPENAI_API_KEY="your_key_here"
```

**"Invalid regex pattern"**
- Try rephrasing your description
- Be more specific about the format
- Check the `--dry-run` output to see the AI prompt

**"No match found" when testing**
- The pattern might be too strict
- Try different test strings
- Use `--explain` to understand the pattern better

### Getting Better Results

1. **Be specific** - "email addresses" vs "RFC 5322 compliant email addresses"
2. **Include examples** - "dates like MM/DD/YYYY or MM-DD-YYYY"  
3. **Mention constraints** - "phone numbers with exactly 10 digits"
4. **Specify format** - "URLs that start with https only"


## License

MIT License - see [LICENSE](LICENSE) file for details.




