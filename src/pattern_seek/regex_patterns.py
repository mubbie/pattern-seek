# define regex patterns for common patterns
    
# GUID/UUID Pattern
# Format: 8-4-4-4-12 hexadecimal digits, with optional hyphens
# - Word boundaries (\b) ensure we don't match partial GUIDs
# Examples: 550e8400-e29b-41d4-a716-446655440000, 550E8400E29B41D4A716446655440000
GUID_PATTERN = r'\b[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}\b'

# Email Pattern
# Format: local-part@domain
# - Local part can contain letters, numbers, dots, underscores, percent signs, plus signs, and hyphens
# - Domain must have at least one dot and end with a valid TLD (2+ letters)
# - No underscores allowed in domain part
# - Word boundaries (\b) ensure we don't match partial emails
EMAIL_PATTERN = r'\b[a-zA-Z0-9._%+-]+@(?!.*_)[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}\b'

# Date Pattern
# Supports multiple common date formats:
# - ISO format: YYYY-MM-DD (e.g., 2023-01-15)
# - US format: MM/DD/YYYY (e.g., 01/15/2023)
# - Europe format: DD/MM/YYYY (e.g., 15/01/2023)
# - Long format with month name: Jan 15, 2023, January 15 2023
# - Reverse long format: 15 Jan 2023
# Note: This pattern matches syntactically valid dates but doesn't validate semantic correctness
# (e.g., it would match Feb 30, 2023 even though that's not a valid date)
DATE_PATTERN = r'(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}|\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4})'

# URL Pattern
# Format: http://, https://, or www. followed by domain and optional path/query
# - Domain must have at least one dot and end with a valid TLD (2+ letters)
# - Can include paths, query parameters, fragments, etc.
# Examples: https://example.com, http://example.org/path, www.example.com
URL_PATTERN = r'(https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?::\d+)?(?:/[^\s]*)?'

# IPv4 Pattern
# Format: Four decimal octets separated by dots
# - Each octet is 0-255
# - Word boundaries (\b) ensure we don't match partial IPs
# Examples: 192.168.1.1, 10.0.0.1, 255.255.255.255
IPV4_PATTERN = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# IPv6 Pattern
# Complex pattern supporting various IPv6 formats:
# - Full form: 8 groups of 4 hex digits, separated by colons (2001:0db8:85a3:0000:0000:8a2e:0370:7334)
# - Compressed form: double colon (::) replaces consecutive zero groups (2001:db8::1)
# - Mixed IPv4/IPv6 notation (::ffff:192.0.2.1)
# - Interface identifiers (%eth0)
# Examples: 2001:0db8:85a3:0000:0000:8a2e:0370:7334, ::1, 2001:db8::1
IPV6_PATTERN = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
