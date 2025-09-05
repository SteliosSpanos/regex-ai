import argparse
import openai
import os
import re
import sys
from dotenv import load_dotenv

class RegexAI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("❌ Error: OPENAI_API_KEY not found in environment")
            print("💡 Create a .env file with: OPENAI_API_KEY=your_key_here")
            sys.exit(1)
        openai.api_key = self.api_key

    def generate(self, description, test_string=None, dry_run=False, explain=False):
        """Generate regex pattern from english description"""
        common_pattern = self._check_common_patterns(description)
        if common_pattern and not dry_run:
            self._display_result(
                common_pattern["pattern"],
                common_pattern["explanation"],
                common_pattern["examples"]
            )
            print("💡 Found in common patterns database!")

            if test_string:
                self._test_pattern(common_pattern["pattern"], test_string)
            return

        prompt = self._buil_prompt(description)

        if dry_run:
            print(f"🔍 Prompt that would be sent to AI:\n")
            print("=" * 50)
            print(prompt)
            print("=" * 50)
            return

        print(f"🤖 Generating regex for: {description}")

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role" : "user", "content" : prompt}],
                max_tokens=400,
                temperature=0.2
            )

            result = response.choices[0].message.content.strip()
            pattern, explanation, examples = self._parse_response(result)

            if pattern:
                self._display_result(pattern, explanation, examples)

                if test_string:
                    self._test_pattern(pattern, test_string)

                if explain:
                    self._explain_pattern(pattern)
            else:
                print("❌ Failed to generate valid regex pattern")
        except Exception as e:
            print(f"❌ Error generating regex: {e}")

    def check_common_patterns(self, description):
        """Check if description matches common patterns"""
        common_patterns = {
            "email" : {
                "pattern" : r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "explanation" : "Matches standard email addresses with alphanumeric characters, dots, underscores, plus signs and hyphens",
                "examples" : ["user@example.com", "test.email+tag@domain.co.uk", "simple@test.org"]
            },
            "phone" : {
                "pattern" : r"^\+?[1-9]\d{1, 14}$",
                "explanation" : "Matches international phone numbers with optional plus sign and 2-15 digits",
                "examples" : ["+1234567890", "1234567890", "+441234567890"]
            },
            "url" : {
                "pattern" : r"^https?://[^\s]+$",
                "explanation" : "Matches HTTP and HTTPS URLs",
                "examples" : ["https://example.com", "http://test.org/path", "https://sub.domain.com/page?query=value"]
            },
            "ip" : {
                "pattern" : r"^(?:[0-9]{1, 3}\.){3}[0-9]{1, 3}$",
                "explanation" : "Matches IPv4 addresses (basic format validation)",
                "examples" : ["192.168.1.1", "10.0.0.1", "172.16.254.1"]
            },
            "date" : {
                "pattern" : r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$",
                "explanation" : "Matches dates in MM/DD/YYYY format",
                "examples" : ["01/15/2024", "12/31/2023", "06/08/1990"]
            }
        }

        desc_lower = description.lower()
        for key, pattern_info in common_patterns.items():
            if key in desc_lower or any(variant in desc_lower for variant in [
                f"{key} address", f"{key} addresses", f"{key} number", f"{key} numbers"
            ]):
                return pattern_info

        return None

    def _build_prompt(self, description):
        """Build optimized prompt for AI"""
        return f"""You are a regex expert. Generate a precise, production-ready regular expression for: "{description}"
Requirements:
- Must be accurate and handle common edge cases
- Should be efficient (avoid catastrophic backtracking)
- Use standard regex syntax that works across languages
- Focus on practical, real-world usage

Respond in this EXACT format:
PATTERN: [the regex pattern only]
EXPLANATION: [clear explanation of what it matches]
EXAMPLES: [3-5 realistic examples separated by |]

Common reference patterns:
- Email: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$
- Phone: ^\\+?[1-9]\\d{{1,14}}$
- URL: ^https?:\\/\\/[^\\s]+$
- IPv4: ^(?:[0-9]{{1,3}}\\.){{3}}[0-9]{{1,3}}$
- Date (MM/DD/YYYY): ^(0[1-9]|1[0-2])\\/(0[1-9]|[12][0-9]|3[01])\\/\\d{{4}}$

Generate for: {description}"""

    def _parse_response(self, result):
        """Parse AI response into components"""
        lines = result.split("\n")
        pattern = ""
        explanation = ""
        examples = []

        for line in lines:
            line = line.strip()
            if line.startswith("PATTERN:"):
                pattern = line.replace("PATTERN:", "").strip()
            elif line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
            elif line.startswith("EXAMPLES:"):
                examples_text = line.replace("EXAMPLES:", "").strip()
                examples = [ex.strip() for ex in examples_text.split("|") if ex.strip()]

        return pattern, explanation, examples

    def _display_result(self, pattern, explanation, examples):
        """Display the generated regex result"""
        print(f"\n🎯 Generated Regex:")
        print(f"   {pattern}")

        if explanation:
            print(f"\n📝 Explanation:")
            print(f"   {explanation}")

        if examples:
            print(f"\n✅ Example matches:")
            for example in examples:
                print(f"   - {example}")

    def _test_pattern(self, pattern, test_string):
        """Test the pattern against a string"""
        print(f"\n🧪 Testing: '{test_string}'")

        try:
            match = re.search(pattern, test_string)
            if match:
                print("   ✅ Match found!")
                if match.groups():
                    print(f"   📋 Captured groups: {match.groups()}")
                print(f"   🎯 Matched text: '{match.group()}'")
            else:
                print("   ❌ No match found")
        except re.error as e:
            print(f"   ❌ Invalid regex pattern: {e}")

    def _explain_pattern(self, pattern):
        """Provide detailed explanation of regex components"""
        print(f"\n🔍 Pattern Breakdown:")
        print(f"   Pattern: {pattern}")

        components = []
        if "^" in pattern:
            components.append("^ = Start of string")
        if "$" in pattern:
            components.append("$ = End of string")
        if "+" in pattern:
            components.append("+ = One or more of preceding element")
        if "*" in pattern:
            components.append("* = Zero or more of preceding element")
        if "?" in pattern:
            components.append("? = Zero or one of preceding element")
        if "[" in pattern and "]" in pattern:
            components.append("[] = Characters class (match any character inside)")
        if "\\d" in pattern:
            components.append("\\d = Any digit (0-9)")
        if "\\w" in pattern:
            components.append("\\w = Any word character (a-z, A-Z, 0-9, _)")
        if "\\s" in pattern:
            components.append("\\s = Any whitespace character")

        for component in components:
            print(f"   - {component}")

def main():
    parser = argparse.ArgumentParser(
        description="RegexAI - Convert English to Regx using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  regexai "email addresses"
  regexai "phone numbers" --test "(555) 123-4567"
  regexai "URLs starting with https" --explain
  regexai "dates in MM/DD/YYYY format" --dry-run

Common patterns:
  • email, email addresses
  • phone, phone numbers  
  • url, urls, website addresses
  • ip, ip addresses, ipv4
  • date, dates in MM/DD/YYYY"""
    )

    parser.add_argument("description", help="English description of the pattern you need")
    parser.add_argument("--test", "-t", help="Test string to validate the regex against")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Show the AI prompt without making a request")
    parser.add_argument("--explain", "-e", action="store_true", help="Explain the regex pattern components")
    parser.add_argument("--version", "-v", action="version", version="RegexAI 1.0.0")

    args = parser.parse_args()

    print("🚀 RegexAI - English to Regex Generator")
    print("=" * 40)

    regexai = RegexAI()
    regexai.generate(args.description, args.test, args.dry_run, args.explain)

if __name__ == "__main__":
    main()