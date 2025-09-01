# myapp-chooser/app.py
from shiny import App, ui

# Replace these with your real shinyapps.io URLs
URL_A = "https://techgearsolutions.shinyapps.io/myapp_a/"
URL_B = "https://techgearsolutions.shinyapps.io/myapp_b/"

app = App(
    ui=ui.page_fluid(
        # Immediately run this script on load:
        ui.tags.script(f"""
          (function() {{
            // 50/50 coin flip
            const variant = Math.random() < 0.5 ? 'A' : 'B';
            const dest = (variant === 'A') ? '{URL_A}' : '{URL_B}';
            window.location.replace(dest);
          }})();
        """)
    ),
    server=lambda input, output, session: None
)