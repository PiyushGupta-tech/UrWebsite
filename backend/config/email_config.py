"""Contact form email settings — committed and deployed with the code.

Edit these values here; environment variables no longer override them.
The only secret, EMAIL_HOST_PASSWORD, stays in backend/.env (never commit it).
"""

# Where contact form submissions are delivered.
CONTACT_EMAIL_TO = "rajeev@urbanrupee.com"

# Google Workspace SMTP. The sending mailbox must exist in Workspace, and
# Gmail rewrites the From address to it unless it is a verified alias.
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "noreply@urbanrupee.com"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
