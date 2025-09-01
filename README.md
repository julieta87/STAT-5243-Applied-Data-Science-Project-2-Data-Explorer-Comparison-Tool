# TechGear Solutions Shiny A/B Testing

This repository contains a Shiny for Python (shiny-py) application with two UI variants (A and B) and a lightweight chooser app that randomly redirects end-users (50/50) to one of them for A/B testing.

Application Link: https://5243project3.shinyapps.io/myapp/



## Repository Structure

```
myapp/
├── myapp_a/
│   └── app_a.py           # Variant A: Calm, single-page product detail + survey
├── myapp_b/
│   └── app_b.py           # Variant B: Multi-step preference sequence
├── myapp/
│   └── app.py             # Chooser redirect app (A/B flip)
├── GA_raw_data_and_data_cleaning/
│   ├── data-cleaning.py
│   ├── ABtest-VersionA.csv
│   ├── ABtest-VersionA_cleaned.csv
│   ├── ABtest-VersionB.csv
│   ├── ABtest-VersionB_cleaned.csv
|   ├── query_abtest.sql
├── requirements.txt       # Python dependencies for shiny-py
├── runtime.txt            # Python runtime version for deployment
└── README.md              # This file

```

## Variant A (app_a.py)

- **UI**: Single-page, calm layout with full customization controls, product details, reviews section.
- **Server**: `server_a` handles reactive state, price calculations, review submissions, and modals.

## Variant B (app_b.py)

- **UI**: Multi-step wizard-style sequence (color → band → size → extras → insights) using custom CSS/JS for step navigation.
- **Server**: `server_b` manages step index, selection handlers, validation, and summary modal.

## Chooser App (myapp/app.py)

A minimal Shiny-Py app whose only job is to load a small inline `<script>` that flips a JavaScript coin (`Math.random() < 0.5`) and redirects the browser to:

- Variant A: `https://<your-account>.shinyapps.io/myapp_a/`
- Variant B: `https://<your-account>.shinyapps.io/myapp_b/`

This ensures an unbiased 50/50 distribution for production users.

## Setup & Local Development

1. **Clone** this repo:
   ```bash
   git clone https://github.com/<your-org>/techgear-shiny-abtest.git
   cd techgear-shiny-abtest
   ```

2. **Create & activate** a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\\Scripts\\activate   # Windows PowerShell
   ```

3. **Install** dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run** any variant locally:
   ```bash
   # Variant A
   shiny run app_a.py

   # Variant B
   shiny run app_b.py

   # Chooser (will redirect immediately)
   shiny run myapp/app.py
   ```

## Deployment to shinyapps.io

Make sure you have the `rsconnect` CLI configured with your account, token, and secret.

1. **Deploy Variant A**
   ```bash
   cd path/to
   rsconnect add --server shinyapps.io --account techgearsolutions --name myapp_a --token <TOKEN> --secret <SECRET>
   rsconnect deploy shiny . --app-dir . --name myapp_a
   ```

2. **Deploy Variant B**
   ```bash
   cd path/to
   rsconnect add --server shinyapps.io --account techgearsolutions --name myapp_b --token <TOKEN> --secret <SECRET>
   rsconnect deploy shiny . --app-dir . --name myapp_b
   ```

3. **Deploy Chooser**
   ```bash
   cd myapp
   rsconnect add --server shinyapps.io --account techgearsolutions --name myapp --token <TOKEN> --secret <SECRET>
   rsconnect deploy shiny . --name myapp
   ```

Update the URLs in `myapp/app.py` to match the actual `myapp_a` and `myapp_b` endpoints.

## Customization & Testing

- To tweak the A/B flip logic, edit the inline script in `myapp/app.py`.
- To adjust static assets (CSS/JS), modify the `<head>` sections in each variant.

##  Google Analytics Data and Data Cleaning

The GA_raw_data_and_data_cleaning folder contains data gathered from Google Analytics (both raw and cleaned CSV files), a Python script for data preparation and cleaning, and an SQL script for querying the GA database (BigQuery).

## Contributing

1. Fork this repository
2. Create a new branch (`git checkout -b feature/...`)
3. Commit your changes
4. Open a Pull Request

## License

[MIT](LICENSE)

