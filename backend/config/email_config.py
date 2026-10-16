"""Contact form email settings — committed and deployed with the code.

Edit these values here; environment variables no longer override them.
The only secret, EMAIL_HOST_PASSWORD, stays in backend/.env (never commit it).
"""

# Where contact form (and chat) submissions are delivered. Matches the address
# shown on the Contact Us page, plus the sales inbox.
CONTACT_EMAIL_TO = "it.support@urbanrupee.com"
CONTACT_EMAIL_CC = ("rajeev@urbanrupee.com",)

# Google Workspace SMTP. The sending mailbox must exist in Workspace, and
# Gmail rewrites the From address to it unless it is a verified alias.
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "noreply@urbanrupee.com"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
