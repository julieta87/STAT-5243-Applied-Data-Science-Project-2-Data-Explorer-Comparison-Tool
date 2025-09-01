from shiny import App, ui, render, reactive, Session

# =============================================================================
# Google Analytics Tag (Version A)
# =============================================================================
google_tag_a = ui.tags.head( 
    ui.tags.script({"async": "", "src": "https://www.googletagmanager.com/gtag/js?id=G-4H1K1FPFDX"}), 
    ui.tags.script("""
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        // Generate anonymous user_id and set it
        function getAnonymousUserId() {
            const key = 'anonymous_user_id';
            let uid = localStorage.getItem(key);
            if (!uid) {
                uid = 'uid_' + Math.random().toString(36).substring(2, 15);
                localStorage.setItem(key, uid);
            }
            return uid;
        }
        const anonymousId = getAnonymousUserId();
        gtag('set', { 'user_id': anonymousId });
        gtag('config', 'G-4H1K1FPFDX');

        // Track page duration
        let enterTime = Date.now();
        document.addEventListener('visibilitychange', function () {
            if (document.visibilityState === 'hidden') {
                let leaveTime = Date.now();
                let duration = Math.round((leaveTime - enterTime) / 1000);
                gtag('event', 'page_duration', {
                    'event_category': 'engagement',
                    'event_label': 'version_a',
                    'value': duration,
                    'debug_mode': true
                });
            }
        });

        // Track buttons, form options, and color selections
        document.addEventListener("DOMContentLoaded", function () {
            // Button click tracker
            document.body.addEventListener("click", function (e) {
                let target = e.target;
                if (target.tagName === "BUTTON" || target.type === "button" || target.classList.contains("btn")) {
                    const label = target.innerText || target.id || "unnamed_button";
                    gtag('event', 'button_click', {
                        'event_category': 'Button',
                        'event_label': label,
                        'value': 1,
                        'debug_mode': true
                    });
                }
            });

            // Survey options tracker (radio, checkbox, select)
            document.body.addEventListener("change", function (e) {
                let target = e.target;
                if (target.type === "radio" || target.type === "checkbox" || target.tagName === "SELECT") {
                    const question = target.name || target.id || "unknown_question";
                    let answer = "unknown_answer";

                    if (target.tagName === "SELECT") {
                        answer = target.options[target.selectedIndex]?.text || "unknown_option";
                    } else {
                        answer = target.value || target.labels?.[0]?.innerText || target.id || "unknown";
                    }

                    gtag('event', 'option_selected', {
                        'event_category': 'Survey',
                        'event_label': question + ": " + answer,
                        'value': 1,
                        'debug_mode': true
                    });
                }
            });

            // Color selection tracker (via .color-swatch divs)
            document.body.addEventListener("click", function (e) {
                let target = e.target;
                if (target.classList.contains("color-swatch")) {
                    const colorName = target.getAttribute("data-color-name") || "unknown_color";
                    gtag('event', 'color_selected', {
                        'event_category': 'Customization',
                        'event_label': colorName,
                        'value': 1,
                        'debug_mode': true
                    });
                }
            });
        });
    """)
)







# ----------------------------
#    Version A UI (Calm)
# ----------------------------
version_a_ui = ui.page_fluid(

    # Google Analytics Tag
    google_tag_a,
    
    # Include Orbitron font from Google Fonts for a tech-savvy look
    ui.tags.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap"
    ),
    # Bootstrap CSS & Bootstrap Icons
    ui.tags.link(
        rel="stylesheet", 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
    ),
    ui.tags.link(
        rel="stylesheet", 
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css"
    ),
    # Custom CSS for Version A
    ui.tags.style("""
        body {
            background-color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
        }
        .header {
            text-align: center;
            padding: 2em;
            background-color: #f8f9fa;
            margin-bottom: 2em;
        }
        .header h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5em;
            margin: 0;
        }
        .main-container {
            padding: 2em;
            margin-bottom: 2em;
        }
        .homepage-text {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 1em;
        }
        .product-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 2em;
            margin: 2em auto;
            transition: transform 0.3s;
            cursor: pointer;
            max-width: 400px;
            text-align: center;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .product-image {
            width: 100%;
            height: auto;
            border-radius: 6px;
            margin-bottom: 1em;
        }
        .product-title {
            font-weight: bold;
            font-size: 1.5em;
            margin-bottom: 0.5em;
        }
        .product-price {
            color: #dc3545;
            font-weight: bold;
            font-size: 1.3em;
            margin-bottom: 1em;
        }
        .carousel-item img {
            width: 100%;
            height: auto;
            border-radius: 6px;
        }
        .product-details-container {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
        }
        .product-details-left {
            flex: 1 1 500px;
        }
        .product-details-right {
            flex: 1 1 500px;
        }
        .big-buy-button {
            background-color: #0071e3;
            color: #fff;
            font-size: 1.2em;
            padding: 0.75em 1.5em;
            border-radius: 0.5em;
            border: none;
            cursor: pointer;
        }
        .big-buy-button:hover {
            background-color: #005bb5;
        }
        .feature-highlights {
            list-style: none;
            padding-left: 0;
            margin-bottom: 2em;
        }
        .feature-highlights li {
            display: flex;
            align-items: center;
            padding: 10px 0;
        }
        .feature-highlights li i {
            font-size: 1.5em;
            margin-right: 10px;
            color: #0071e3;
        }
        .feature-divider {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 0;
        }
        .customization-section {
            border-top: 1px solid #dee2e6;
            padding-top: 1em;
        }
        .customization-option {
            margin-bottom: 1em;
        }
        .customization-option h5 {
            margin-bottom: 0.5em;
        }
        .band-selection-container {
            margin-bottom: 1em;
        }
        .band-images {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-top: 1em;
        }
        .band-images div {
            text-align: center;
        }
        .band-material-image {
            width: 300px;
            height: 300px;
            object-fit: contain;
            margin-bottom: 0.5em;
        }
        .color-swatch {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
        }
        .color-swatch:hover {
            outline: 2px solid #0071e3;
            outline-offset: 2px;
        }
        .color-label {
            font-size: 0.8em;
        }
        .reviews-section {
            background-color: #f8f9fa;
            padding: 2em;
            border-radius: 8px;
            margin-top: 2em;
        }
        .reviews-collapse-header {
            cursor: pointer;
            padding: 1em;
            background-color: #e9ecef;
            border-radius: 5px;
            margin-bottom: 1em;
        }
        .reviews-collapse-header h3 {
            margin: 0;
        }
        .reviews-container {
            margin-top: 1em;
        }
        .review-card {
            background-color: white;
            padding: 1em;
            margin-bottom: 1em;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    """),
    ui.tags.script({"src": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js", "defer": ""}),
    ui.tags.script("""
        Shiny.addCustomMessageHandler("reload", function(message) {
            window.location.reload();
        });
    """),
    ui.div(
        {"class": "header"},
        ui.img(src="https://i.imgur.com/Nwd6mZT.png", alt="Banner Image", 
               style="width: 10%; height: auto; margin-bottom: 20px;"),
        ui.h1("TechGear Solutions"),
        ui.p("Innovative products for the modern lifestyle"),
        ui.input_action_button("join_waitlist", "Subscribe for Updates", class_="btn-primary btn-lg")
    ),
    ui.output_ui("main_content"),
    ui.output_ui("modal_output_placeholder")
)

# ----------------------------
#    Server Logic
# ----------------------------
def server_a(input, output, session: Session):
    print("DEBUG A: server_a is being called")

    # --- Core Product Data ---
    product = {
        "id": 1,
        "name": "Smart Watch Pro X1",
        "price": 199.99,
        "description": "The ultimate smartwatch for fitness and productivity enthusiasts.",
        "features": [
            "24/7 heart rate and sleep tracking",
            "Water resistant up to 50m",
            "7-day battery life",
            "Built-in GPS and workout tracking",
            "Notification and call management"
        ],
        "customizations": {
            "band_material": {
                "silicone": {"name": "Silicone", "price": 0},
                "leather": {"name": "Leather", "price": 30},
                "metal": {"name": "Stainless Steel", "price": 50}
            },
            "size": {
                "small": {"label": "Small (38mm)", "price": 0},
                "medium": {"label": "Medium (42mm) +$40", "price": 40},
                "large": {"label": "Large (46mm) +$80", "price": 80}
            },
            "additional_features": {
                "cellular": {"name": "Cellular Connectivity", "price": 50},
                "premium": {"name": "Premium Apps Package", "price": 30},
                "warranty": {"name": "Extended Warranty", "price": 25}
            },
            "charging": {
                "standard": {"name": "Standard Charger", "price": 0},
                "fast": {"name": "Fast Charger", "price": 20},
                "wireless": {"name": "Wireless Dock", "price": 30}
            },
            "accessories": {
                "none": {"name": "Watch Only", "price": 0},
                "bundle": {"name": "Travel Case + Extra Band", "price": 25},
                "premium_bundle": {"name": "Case + Extra Band + Charger", "price": 40}
            }
        },
        "user_questions": {
            "own_smartwatch": {
                "question": "Do you currently own a smartwatch?",
                "options": {
                    "yes": {"label": "Yes"},
                    "no": {"label": "No"},
                    "used_to": {"label": "I used to, but not anymore"}
                }
            },
            "main_reason": {
                "question": "What's your main reason for using (or wanting) a smartwatch?",
                "options": {
                    "fitness": {"label": "Fitness tracking"},
                    "productivity": {"label": "Productivity / notifications"},
                    "health": {"label": "Health monitoring"},
                    "style": {"label": "Style / fashion"},
                    "other": {"label": "Other"}
                }
            },
            "price_range": {
                "question": "What price range are you most comfortable with?",
                "options": {
                    "under_100": {"label": "Under $100"},
                    "100_199": {"label": "$100–$199"},
                    "200_299": {"label": "$200–$299"},
                    "300_plus": {"label": "$300+"}
                }
            },
            "phone_type": {
                "question": "Which phone do you use?",
                "options": {
                    "iphone": {"label": "iPhone"},
                    "android": {"label": "Android"},
                    "other": {"label": "Other"}
                }
            }
        }
    }

    # --- Reactive Values ---
    selected_color = reactive.Value(None)

    # --- Color Selection Logic ---
    color_data = {
        "black": {"name": "Black Sesame", "hex": "#333436", "front": "https://i.imgur.com/5ZBmQ95.png", "side": "https://i.imgur.com/OgU4x1W.png"},
        "green": {"name": "Mint Chocolate Green", "hex": "#c8dace", "front": "https://i.imgur.com/LHRrs89.png", "side": "https://i.imgur.com/d8FQedI.png"},
        "pink": {"name": "Cotton Candy Pink", "hex": "#ebe3e0", "front": "https://i.imgur.com/hx8pKt2.png", "side": "https://i.imgur.com/3U7gACw.png"}
    }
    band_material_images = {
        "silicone": "https://i.imgur.com/skeHDtq.png",
        "leather": "https://i.imgur.com/wChoZnu.png",
        "metal": "https://i.imgur.com/s0p72xn.png"
    }

    @reactive.Calc
    def color_label():
        col = selected_color.get()
        return "Please Select a Color" if col is None else color_data[col]['name']

    @reactive.Calc
    def watch_images():
        col = selected_color.get()
        default_col = "black" # Default image if none selected
        return [color_data[col or default_col]["front"], color_data[col or default_col]["side"]]

    @reactive.Effect
    @reactive.event(input.color_clicked)
    def update_color_clicked():
        val = input.color_clicked()
        if val in color_data:
            selected_color.set(val)
            session.send_custom_message("ga_color", {"color": color_data[val]["name"]})

    @output
    @render.text
    def display_color_label():
        return color_label()

    # --- Main Content Rendering ---
    @output
    @render.ui
    def main_content():
        print("DEBUG A: Rendering main_content for Variant A")
        # VERSION A: PRODUCT DETAIL PAGE
        imgs = watch_images()
        carousel_items = [
            ui.tags.div({"class": "carousel-item active" if i == 0 else "carousel-item"},
                        ui.tags.img(src=img, class_="d-block w-100", alt=f"Watch Image {i+1}"))
            for i, img in enumerate(imgs)
        ]
        carousel = ui.tags.div(
            {"id": "carouselExampleControls", "class": "carousel slide", "data-bs-ride": "carousel"},
            ui.tags.div({"class": "carousel-inner"}, *carousel_items),
            ui.tags.button({"class": "carousel-control-prev", "type": "button", "data-bs-target": "#carouselExampleControls", "data-bs-slide": "prev"},
                            ui.tags.span({"class": "carousel-control-prev-icon", "aria-hidden": "true"}),
                            ui.tags.span({"class": "visually-hidden"}, "Previous")),
            ui.tags.button({"class": "carousel-control-next", "type": "button", "data-bs-target": "#carouselExampleControls", "data-bs-slide": "next"},
                            ui.tags.span({"class": "carousel-control-next-icon", "aria-hidden": "true"}),
                            ui.tags.span({"class": "visually-hidden"}, "Next"))
        )

        bands_row = ui.div(
            {"class": "band-images"},
            ui.div(
                ui.img(src=band_material_images["silicone"], class_="band-material-image"),
                ui.tags.p("Silicone", style="margin:0;")
            ),
            ui.div(
                ui.img(src=band_material_images["leather"], class_="band-material-image"),
                ui.tags.p("Leather", style="margin:0;")
            ),
            ui.div(
                ui.img(src=band_material_images["metal"], class_="band-material-image"),
                ui.tags.p("Stainless Steel", style="margin:0;")
            )
        )

        # Right column: Customization options, including color swatches.
        return ui.div(
            {"class": "main-container"},
            # Added message header with styling
            ui.div(
                {"class": "alert alert-info mb-4 text-center", "style": "background-color: #e7f3ff; border-color: #0071e3;"},
                ui.h4("Help Us Shape Our Next Product!", style="color: #0071e3; margin-bottom: 0.5rem;"),
                ui.p("Explore the product and give us your preferences.", style="margin-bottom: 0;")
            ),
            ui.div(
                {"class": "product-details-container"},
                ui.div(
                    {"class": "product-details-left"},
                    carousel,
                    ui.div({"class": "mt-4"}, bands_row)
                ),
                ui.div(
                    {"class": "product-details-right"},
                    ui.h2(product["name"]),
                    ui.p("From $199 or $16.67/month for 12 months"),
                    ui.tags.ul(
                        {"class": "feature-highlights"},
                        *[ui.tags.li(ui.tags.i({"class": icon}), ui.tags.span(" " + feat))
                        for icon, feat in zip(
                            ["bi-heart-fill", "bi-droplet-fill", "bi-battery-full", "bi-geo-alt-fill", "bi-bell-fill"],
                            product["features"]
                        )]
                    ),
                    ui.p(product["description"], class_="mt-3"),
                    # Color options
                    ui.div(
                        {"class": "customization-option"},
                        ui.h5("Choose Watch Color:"),
                        ui.div(
                            {"class": "d-flex gap-3"},
                            ui.tags.div({
                                "class": "color-swatch",
                                "style": "background-color: " + color_data["black"]["hex"] + ";",
                                "data-color-name": color_data["black"]["name"],
                                "onclick": "Shiny.setInputValue('color_clicked','black',{priority:'event'});"
                            }),
                            ui.tags.div({
                                "class": "color-swatch",
                                "style": "background-color: " + color_data["green"]["hex"] + ";",
                                "data-color-name": color_data["green"]["name"],
                                "onclick": "Shiny.setInputValue('color_clicked','green',{priority:'event'});"
                            }),
                            ui.tags.div({
                                "class": "color-swatch",
                                "style": "background-color: " + color_data["pink"]["hex"] + ";",
                                "data-color-name": color_data["pink"]["name"],
                                "onclick": "Shiny.setInputValue('color_clicked','pink',{priority:'event'});"
                            })
                        ),
                        ui.tags.p(
                            {"style": "font-size: 0.8em; margin-top: 5px;"},
                            "Selected: ",
                            ui.output_text("display_color_label")
                        )
                    ),

                    ui.br(),
                    # Band selection radio buttons
                    ui.div(
                        {"class": "customization-option"},
                        ui.h5("Select Your Band:"),
                        ui.input_radio_buttons("band_material", None,
                                                 {"silicone": "Silicone (+$0)", "leather": "Leather (+$30)", "metal": "Stainless Steel (+$50)"},
                                                 selected="silicone",
                                                 inline=True
                        )
                    ),
                    ui.br(),
                    ui.h5("Size:"),
                    ui.input_radio_buttons("size", None,
                                             {k: v["label"] for k, v in product["customizations"]["size"].items()},
                                             selected=list(product["customizations"]["size"].keys())[0],
                                             inline=True
                    ),
                    ui.div(
                        {"class": "customization-option"},
                        ui.h5("Additional Features:"),
                        ui.input_checkbox_group("additional_features", None,
                                                  {"cellular": "Cellular Connectivity (+$50)",
                                                   "premium": "Premium Apps Package (+$30)",
                                                   "warranty": "Extended Warranty (+$25)"},
                                                  selected=[],
                                                  inline=True
                        )
                    ),
                    ui.br(),
                    # Charging options
                    ui.div(
                        {"class": "customization-option"},
                        ui.h5("Charging Options:"),
                        ui.input_radio_buttons("charging_option", None,
                                                 {"standard": "Standard Charger (+$0)",
                                                  "fast": "Fast Charger (+$20)",
                                                  "wireless": "Wireless Dock (+$30)"},
                                                 selected="standard",
                                                 inline=True
                        )
                    ),
                    ui.br(),
                    # Accessories options
                    ui.div(
                        {"class": "customization-option"},
                        ui.h5("Accessories Bundle:"),
                        ui.input_radio_buttons("accessories_option", None,
                                                 {"none": "Watch Only (+$0)",
                                                  "bundle": "Travel Case + Extra Band (+$25)",
                                                  "premium_bundle": "Case + Extra Band + Charger (+$40)"},
                                                 selected="none",
                                                 inline=True
                        )
                    ),
                    ui.br(),
                    # User Insights Section
                    ui.div(
                        {"class": "customization-option"},
                        ui.h4("User Insights"),
                        ui.p("Help us understand your preferences better by answering a few questions:"),
                        ui.br(),
                        # Smartwatch ownership question
                        ui.div(
                            {"class": "mb-4"},
                            ui.h5(product["user_questions"]["own_smartwatch"]["question"]),
                            ui.input_radio_buttons("own_smartwatch", None,
                                                 {k: v["label"] for k, v in product["user_questions"]["own_smartwatch"]["options"].items()},
                                                 selected=None,
                                                 inline=True
                            )
                        ),
                        # Main reason question
                        ui.div(
                            {"class": "mb-4"},
                            ui.h5(product["user_questions"]["main_reason"]["question"]),
                            ui.input_radio_buttons("main_reason", None,
                                                 {k: v["label"] for k, v in product["user_questions"]["main_reason"]["options"].items()},
                                                 selected=None,
                                                 inline=True
                            )
                        ),
                        # Price range question
                        ui.div(
                            {"class": "mb-4"},
                            ui.h5(product["user_questions"]["price_range"]["question"]),
                            ui.input_radio_buttons("price_range", None,
                                                 {k: v["label"] for k, v in product["user_questions"]["price_range"]["options"].items()},
                                                 selected=None,
                                                 inline=True
                            )
                        ),
                        # Phone type question
                        ui.div(
                            {"class": "mb-4"},
                            ui.h5(product["user_questions"]["phone_type"]["question"]),
                            ui.input_radio_buttons("phone_type", None,
                                                 {k: v["label"] for k, v in product["user_questions"]["phone_type"]["options"].items()},
                                                 selected=None,
                                                 inline=True
                            )
                        )
                    ),
                    ui.br(),
                    ui.div(
                        {"class": "d-flex align-items-center gap-2"},
                        ui.input_action_button("purchase", "Submit Preferences", class_="big-buy-button")
                    ),
                    ui.output_text("total_price")
                )
            ),
            ui.hr(),
            ui.div(
                {"class": "reviews-section mt-4"},
                ui.h3("Submit Your Review"),
                ui.row(
                    ui.column(12, ui.input_text("reviewer_name", "Your Name"))
                ),
                ui.input_text_area("review_text", "Your Review", rows=5, placeholder="Share your experience with the product..."),
                ui.input_action_button("submit_review", "Submit Review", class_="btn-primary mt-3")
            )
        )

    @output
    @render.text
    def total_price():
        try:
            base_price = product["price"]
            
            material = input.band_material() or "silicone"
            material_cost = product["customizations"]["band_material"].get(material, {"price": 0})["price"]
            
            feature_cost = 0
            additional = input.additional_features() or []
            for feat in additional:
                if feat in product["customizations"]["additional_features"]:
                    feature_cost += product["customizations"]["additional_features"][feat]["price"]
                    
            size = input.size() or "small"
            size_cost = product["customizations"]["size"].get(size, {"price": 0})["price"]
            
            charging = input.charging_option() or "standard"
            charging_cost = product["customizations"]["charging"].get(charging, {"price": 0})["price"]
            
            accessories = input.accessories_option() or "none"
            accessories_cost = product["customizations"]["accessories"].get(accessories, {"price": 0})["price"]
            
            total = base_price + material_cost + feature_cost + size_cost + charging_cost + accessories_cost
            return f"Total Price: ${total:.2f}"
        except Exception as e:
            print(f"Error calculating price: {e}")
            return "Error calculating price."

    # --- Purchase/Submit Logic ---
    @reactive.Effect
    @reactive.event(input.purchase)
    def handle_purchase():
        try:
            if selected_color.get() is None:
                ui.notification_show("Please select a color before proceeding.", duration=5)
                return
            
            material = input.band_material() or "silicone"
            size = input.size() or "small"
            additional = input.additional_features() or []
            charging = input.charging_option() or "standard"
            accessories = input.accessories_option() or "none"
            
            # Get user insights
            own_smartwatch = input.own_smartwatch()
            main_reason = input.main_reason()
            price_range = input.price_range()
            phone_type = input.phone_type()
            
            # Validate user insights
            if not own_smartwatch or not main_reason or not price_range or not phone_type:
                ui.notification_show("Please answer all user insight questions before submitting.", duration=5, type="warning")
                return
            
            feature_names = []
            for f in additional:
                if f in product["customizations"]["additional_features"]:
                    feature_names.append(product["customizations"]["additional_features"][f]["name"])
            features_str = ", ".join(feature_names) if feature_names else "None"
            
            base_price = product["price"]
            material_cost = product["customizations"]["band_material"].get(material, {"price": 0})["price"]
            feature_cost = sum(product["customizations"]["additional_features"].get(f, {"price": 0})["price"] for f in additional)
            size_cost = product["customizations"]["size"].get(size, {"price": 0})["price"]
            charging_cost = product["customizations"]["charging"].get(charging, {"price": 0})["price"]
            accessories_cost = product["customizations"]["accessories"].get(accessories, {"price": 0})["price"]
            total = base_price + material_cost + feature_cost + size_cost + charging_cost + accessories_cost

            ui.modal_show(
                ui.modal(
                    ui.h3("Thank you for your preferences!"),
                    ui.p("We'll use your feedback to improve our product."),
                    ui.h4("Product Customization:"),
                    ui.p(f"Selected Color: {color_data[selected_color.get()]['name']}"),
                    ui.p(f"Selected Band: {product['customizations']['band_material'][material]['name']}"),
                    ui.p(f"Selected Size: {product['customizations']['size'][size]['label']}"),
                    ui.p(f"Selected Features: {features_str}"),
                    ui.p(f"Selected Charging: {product['customizations']['charging'][charging]['name']}"),
                    ui.p(f"Selected Accessories: {product['customizations']['accessories'][accessories]['name']}"),
                    ui.p(f"Estimated Price: ${total:.2f}"),
                    ui.h4("User Insights:"),
                    ui.p(f"Smartwatch Ownership: {product['user_questions']['own_smartwatch']['options'][own_smartwatch]['label']}"),
                    ui.p(f"Main Reason: {product['user_questions']['main_reason']['options'][main_reason]['label']}"),
                    ui.p(f"Preferred Price Range: {product['user_questions']['price_range']['options'][price_range]['label']}"),
                    ui.p(f"Phone Type: {product['user_questions']['phone_type']['options'][phone_type]['label']}"),
                    footer=ui.div(
                        ui.input_action_button("ok_confirm", "OK", class_="btn-primary")
                    )
                )
            )
        except Exception as e:
            ui.notification_show("There was an issue processing your preferences. Please try again.", duration=5, type="error")
            print(f"Purchase error: {str(e)}")
    

    # --- Review Submission Logic ---
    @reactive.Effect
    @reactive.event(input.submit_review)
    def submit_review():
        if not input.reviewer_name() or not input.review_text():
            ui.notification_show("Please fill out all fields to submit a review.", duration=5)
        else:
            ui.notification_show("Thank you for your review! It will be posted after moderation.", duration=5)
            ui.update_text("reviewer_name", value="")
            ui.update_text_area("review_text", value="")

    @reactive.Effect
    @reactive.event(input.ok_confirm)
    async def ok_confirm():
        ui.modal_remove()
        await session.send_custom_message("reload", {})

    # --- Subscribe Modal ---
    @reactive.Effect
    @reactive.event(input.join_waitlist)
    def handle_join_waitlist():
        ui.modal_show(
            ui.modal(
                ui.h3("Subscribe for Updates"),
                ui.p("Be the first to know when new products are available!"),
                ui.input_text("waitlist_name", "Your Name"),
                ui.input_text("waitlist_email", "Your Email"),
                footer=ui.div(
                    ui.input_action_button("submit_waitlist", "Submit", class_="btn-primary"),
                    ui.tags.button(  # Changed from input_action_button to tags.button
                        "Close", 
                        id="close_waitlist_modal",
                        class_="btn btn-secondary",
                        **{"data-bs-dismiss": "modal"}  # This is the key addition
                    )
                )
            )
        )

    @reactive.Effect
    @reactive.event(input.close_waitlist_modal)
    def handle_close_waitlist_modal():
        ui.modal_remove()

    @reactive.Effect
    @reactive.event(input.submit_waitlist)
    def submit_waitlist():
        if not input.waitlist_name() or not input.waitlist_email():
            ui.notification_show("Please fill out all fields to join the waitlist.", duration=5)
            return
        ui.modal_remove()
        ui.notification_show("Thank you for joining our waitlist! We'll notify you when new products are available.", duration=5)

    @reactive.Effect
    @reactive.event(input.back_to_main)
    def go_back_to_main():
        ui.notification_show("This is a standalone app, can't go back to home page here.", duration=5)



# ----------------------------
#    Create & Run the App
# ----------------------------
app = App(ui=version_a_ui, server=server_a)