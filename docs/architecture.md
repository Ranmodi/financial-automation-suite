# Architecture

The suite follows a repeated operational automation pattern:

```text
Input files
    ↓
Normalization
    ↓
Business rules
    ↓
Excel/HTML output
    ↓
E-mail/logging layer
```

## Design principles

- Keep configuration outside the code.
- Use sample data for public repositories.
- Keep business rules explicit and auditable.
- Write logs for operational review.
- Avoid committing private files and credentials.
