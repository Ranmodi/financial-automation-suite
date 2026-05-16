# Security Review

This repository was prepared for public portfolio use.

## Removed from public version

- Real e-mails;
- Real client and advisor data;
- Internal file paths;
- Private spreadsheets;
- Production credentials;
- API keys;
- Provider-specific sensitive settings;
- Generated logs from real workflows.

## Never commit

```text
.env
credentials
real Excel files
real client data
API keys
SMTP passwords
Outlook account details
logs with sensitive information
```

## Recommended workflow

1. Use `.env.example` as a template.
2. Create a private `.env` locally.
3. Keep real inputs in an ignored `input/` folder.
4. Keep outputs in an ignored `output/` folder.
5. Review generated files before sharing.
