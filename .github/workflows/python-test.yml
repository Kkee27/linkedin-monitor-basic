name: LinkedIn Monitor

on:
  workflow_dispatch:  # Manual trigger
  schedule:
    - cron: '0 */4 * * *'  # Run every 4 hours

jobs:
  monitor-linkedin:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Explicitly grant write permission
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4
      
      - name: Run LinkedIn Monitor
        env:
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
        run: python linkedin_monitor.py
      
      - name: Commit changes
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add -A
          git diff --quiet && git diff --staged --quiet || git commit -m "Update LinkedIn check data"
          git push
