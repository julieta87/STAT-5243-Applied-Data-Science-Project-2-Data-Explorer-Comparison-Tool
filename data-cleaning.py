import pandas as pd

# Load Version B data
df = pd.read_csv(r"Your Local Path\ABtest-VersionB.csv")

# Keep only button_click events with label "Submit Preferences" or "Subscribe for Updates"
df = df[(df['event_name'] != 'button_click') | 
        (df['event_label'].isin(['Submit Preferences', 'Subscribe for Updates']))]

# Create a new column for event_option
df['event_option'] = ''

# Extract option category from event_label if it contains ": "
mask = (df['event_name'] == 'option_selected') & (df['event_label'].str.contains(": "))
df.loc[mask, 'event_option'] = df.loc[mask, 'event_label'].str.split(": ").str[0]
df.loc[mask, 'event_label'] = df.loc[mask, 'event_label'].str.split(": ").str[1]

# Convert color_selected to option_selected
mask_color = df['event_name'] == 'color_selected'
df.loc[mask_color, 'event_option'] = 'color_selected'
df.loc[mask_color, 'event_name'] = 'option_selected'

# Convert material_selected to option_selected
mask_material = df['event_name'] == 'material_selected'
df.loc[mask_material, 'event_option'] = 'material_selected'
df.loc[mask_material, 'event_name'] = 'option_selected'

# Remove b_selected_ and b_answer_ prefixes from event_option
df['event_option'] = df['event_option'].str.replace(r"^b_selected_|^b_answer_", "", regex=True)

# Save cleaned data
df.to_csv(r"Your Local Path", index=False)
