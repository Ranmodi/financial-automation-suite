# -*- coding: utf-8 -*-
"""Public-safe HTML e-mail sender for Outlook."""

from __future__ import annotations

import argparse
from pathlib import Path


def send_or_display_outlook_email(html_body: str, to: str, subject: str, send: bool = False, send_from: str | None = None):
    try:
        import win32com.client as win32
    except ImportError as exc:
        raise ImportError("pywin32 is required for Outlook automation.") from exc

    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = to
    mail.Subject = subject
    mail.HTMLBody = html_body

    if send_from:
        try:
            for account in outlook.Session.Accounts:
                if str(account.SmtpAddress).lower() == send_from.lower():
                    mail.SendUsingAccount = account
                    break
        except Exception:
            pass

    if send:
        mail.Send()
    else:
        mail.Display()


def parse_args():
    parser = argparse.ArgumentParser(description="Create or send an HTML Outlook e-mail.")
    parser.add_argument("--html", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", default="Automated Financial Report")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--send-from", default="")
    return parser.parse_args()


def main():
    args = parse_args()
    html_body = Path(args.html).read_text(encoding="utf-8", errors="replace")
    send_or_display_outlook_email(
        html_body=html_body,
        to=args.to,
        subject=args.subject,
        send=args.send,
        send_from=args.send_from or None,
    )


if __name__ == "__main__":
    main()
