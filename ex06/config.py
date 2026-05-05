num_of_steps = 3

report_template = """We made {num_observations} observations by tossing a coin: {tails} were tails and {heads} were heads.
The probabilities are {tail_prob:.2f}% and {head_prob:.2f}%, respectively.
Our forecast is that the next {num_steps} observations will be: {tail_forecast} tail(s) and {head_forecast} head(s)."""

TELEGRAM_WEBHOOK_URL = "YOUR_URL"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"