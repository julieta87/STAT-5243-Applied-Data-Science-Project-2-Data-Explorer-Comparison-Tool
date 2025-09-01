from shiny import App, ui, render, reactive, Session

# =============================================================================
# Google Analytics Tag (Version B)
# =============================================================================
google_tag_b = ui.tags.head( 
    ui.tags.script({"async": "", "src": "https://www.googletagmanager.com/gtag/js?id=G-WLF68C4SWM"}), 
    ui.tags.script("""
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        // Anonymous user_id
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
        gtag('config', 'G-WLF68C4SWM');

        // Track page duration
        let enterTime = Date.now();
        document.addEventListener('visibilitychange', function () {
            if (document.visibilityState === 'hidden') {
                let leaveTime = Date.now();
                let duration = Math.round((leaveTime - enterTime) / 1000);
                gtag('event', 'page_duration', {
                    'event_category': 'engagement',
                    'event_label': 'version_b',
                    'value': duration,
                    'debug_mode': true
                });
            }
        });

        // DOM Ready
        document.addEventListener("DOMContentLoaded", function () {
            document.body.addEventListener("click", function (e) {
                let target = e.target;

                // Track color selections
                const colorElem = target.closest(".step-color-option");
                if (colorElem && (colorElem.classList.contains("color-swatch") || colorElem.querySelector(".color-swatch"))) {
                    const colorName = colorElem.getAttribute("data-color-name") ||
                                    colorElem.querySelector(".color-swatch")?.getAttribute("data-color-name") ||
                                    "unknown_color";
                    gtag('event', 'color_selected', {
                        'event_category': 'Customization',
                        'event_label': colorName,
                        'value': 1,
                        'debug_mode': true
                    });
                    return;
                }

                // Track material selections
                const materialElem = target.closest(".material-swatch");
                if (materialElem) {
                    const materialName = materialElem.getAttribute("data-material-name") || "unknown_material";
                    gtag('event', 'material_selected', {
                        'event_category': 'Customization',
                        'event_label': materialName,
                        'value': 1,
                        'debug_mode': true
                    });
                    return;
                }

                // Track button clicks
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

            // Track survey-type interactions
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
        });
    """)
)




# =============================================================================
# Version B UI Definition
# =============================================================================

version_b_ui = ui.page_fluid(

    # Google Analytics Tag
    google_tag_b,
    
    ui.tags.head(
        # Fonts
        ui.tags.link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap"),
        
        # Bootstrap CSS
        ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"),
        ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css"),
        
        # jQuery
        ui.tags.script(src="https://code.jquery.com/jquery-3.6.0.min.js"),
        
        # Inline CSS from app_css
        ui.tags.style("""
                body { background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; }
                .header { text-align: center; padding: 2em; background-color: #f8f9fa; margin-bottom: 2em; }
                .header h1 { font-family: 'Orbitron', sans-serif; font-size: 2.5em; margin: 0; }
                .main-container { padding: 2em; margin-bottom: 2em; }
                .homepage-text { font-size: 24px; font-weight: bold; margin-bottom: 1em; }
                .product-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 2em; margin: 2em auto; transition: transform 0.3s; cursor: pointer; max-width: 400px; text-align: center; }
                .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
                .product-image { width: 100%; height: auto; border-radius: 6px; margin-bottom: 1em; }
                .product-title { font-weight: bold; font-size: 1.5em; margin-bottom: 0.5em; }
                .product-price { color: #dc3545; font-weight: bold; font-size: 1.3em; margin-bottom: 1em; }
                .carousel-item img { width: 100%; height: auto; border-radius: 6px; }
                .product-details-container { display: flex; flex-wrap: wrap; gap: 2rem; }
                .product-details-left { flex: 1 1 500px; }
                .product-details-right { flex: 1 1 500px; }
                .big-buy-button { background-color: #0071e3; color: #fff; font-size: 1.2em; padding: 0.75em 1.5em; border-radius: 0.5em; border: none; cursor: pointer; }
                .big-buy-button:hover { background-color: #005bb5; }
                .feature-highlights { list-style: none; padding-left: 0; margin-bottom: 1em; } /* Base margin */
                .feature-highlights li { display: flex; align-items: center; padding: 8px 0; }
                .feature-highlights li i { font-size: 1.4em; margin-right: 10px; color: #0071e3; }
                .color-swatch { width: 36px; height: 36px; border-radius: 50%; cursor: pointer; border: 1px solid #ccc; display: inline-block; margin-right: 10px; vertical-align: middle; }
                /* Version B Step Styles */
                .step-container { max-width: 800px; margin: 2em auto; padding: 2em; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #fff; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
                .step-navigation { margin-top: 2em; display: flex; justify-content: space-between; border-top: 1px solid #eee; padding-top: 1.5em; }
                .step-content { min-height: 300px; }
                .step-color-option { display: flex; align-items: center; margin-bottom: 1rem; cursor: pointer; padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid #eee; transition: all 0.2s ease-in-out; }
                .step-color-option:hover { background-color: #f8f9fa; }
                .step-color-option.selected { border-color: #0071e3; background-color: #e7f3ff; font-weight: bold; }
                .step-color-option .color-swatch { flex-shrink: 0; }
                .step-color-option span { margin-left: 1rem; }
                .step-band-option { display: flex; align-items: center; margin-bottom: 1rem; cursor: pointer; padding: 1rem; border-radius: 8px; border: 1px solid #eee; transition: all 0.2s ease-in-out; }
                .step-band-option:hover { background-color: #f8f9fa; }
                .step-band-option img { width: 100px; height: 100px; object-fit: contain; margin-right: 1.5rem; flex-shrink: 0; }
                .step-band-option.selected { border-color: #0071e3; background-color: #e7f3ff; }
                .step-band-details h5 { margin-bottom: 0.25rem; }
                .step-band-details p { margin-bottom: 0; color: #6c757d; font-size: 0.9em; }
                .step-progress { margin-bottom: 1.5em; }
                /* Added bigger text in steps */
                .step-color-option span, .step-band-details h5, .step-band-details p, 
                .form-check-label, .shiny-input-container label { 
                    font-size: 1.2em; 
                }
                /* Make modal text bigger */
                .modal-body p, .modal-body h4 {
                    font-size: 1.2em;
                }
                .modal-title {
                    font-size: 1.5em;
                }
                /* Improve modal footer buttons */
                .modal-footer .btn {
                    font-size: 1.1em;
                    padding: 0.5em 1.2em;
                }
                .btn-success {
                    background-color: #0071e3;
                    border-color: #0071e3;
                }
                .btn-success:hover {
                    background-color: #005bb5;
                    border-color: #005bb5;
                }
                /* Modal animation */
                .modal.fade .modal-dialog {
                    transition: transform 0.3s ease-out;
                    transform: translate(0, -50px);
                }
                .modal.show .modal-dialog {
                    transform: none;
                }
        """),
        
        # Inline JavaScript from shared_js_b
        ui.tags.script({"src": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js", "defer": ""}),
        ui.tags.script("""
                        // Reload handler
                    Shiny.addCustomMessageHandler("reload", function(message) {
                        window.location.reload();
                    });

                    // Modal close handler
                    Shiny.addCustomMessageHandler("close_modal", function(message) {
                        // Find any open modals and close them
                        const modals = document.querySelectorAll('.modal.show');
                        if (modals.length > 0) {
                            for (const modal of modals) {
                                const modalInstance = bootstrap.Modal.getInstance(modal);
                                if (modalInstance) {
                                    modalInstance.hide();
                                }
                            }
                        }
                    });

                    // Helper function to select color/band visually in Version B
                    function selectBVariantItem(containerId, itemId, itemClass) {
                        const container = document.getElementById(containerId);
                        if (!container) return;
                        const items = container.querySelectorAll('.' + itemClass);
                        items.forEach(item => {
                            item.classList.remove('selected');
                            if (item.dataset.value === itemId) {
                                item.classList.add('selected');
                            }
                        });
                    }

                    // Register the handler for visual selection messages from the server
                    $(document).on('shiny:connected', function(event) {
                        if (typeof Shiny !== 'undefined' && Shiny.addCustomMessageHandler) {
                            Shiny.addCustomMessageHandler("js_select", function(message) {
                                if (typeof selectBVariantItem === 'function') {
                                    selectBVariantItem(message.container, message.value, message.item_class);
                                } else { console.error("JS Error: selectBVariantItem function not found."); }
                            });
                        } else { console.error("JS Error: Shiny or addCustomMessageHandler not ready."); }
                    });
        """)
    ),
    # Header
    ui.div(
        {"class": "header"},
        ui.img(src="https://i.imgur.com/Nwd6mZT.png", alt="Banner", style="width: 10%; height: auto; margin-bottom: 20px;"),
        ui.h1("TechGear Solutions"),
        ui.p("Innovative products for the modern lifestyle"),
        ui.input_action_button("join_waitlist", "Subscribe for Updates", class_="btn-primary btn-lg")
    ),
    # Main content area rendered by the server
    ui.output_ui("main_content"),
    # Placeholder for modals
    ui.output_ui("modal_output_placeholder")
)

# =============================================================================
# Server Logic (Version B)
# =============================================================================
def server_b(input, output, session: Session):

    # --- Add User ID to Google Analytics ---
    session.send_custom_message("ga_set_user", {"user_id": session.id})

    # --- Core Product Data ---
    product = { 
        "id": 1, 
        "name": "Smart Watch Pro X1", 
        "price": 199.99, 
        "description": "The ultimate smartwatch for fitness and productivity enthusiasts.", 
        "features": [
            "24/7 heart rate monitoring and sleep tracking",
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
                "premium": {"name": "Premium Apps", "price": 30}, 
                "warranty": {"name": "Extended Warranty", "price": 25}
            }, 
            "charging": {
                "standard": {"name": "Standard Charger", "price": 0}, 
                "fast": {"name": "Fast Charger", "price": 20}, 
                "wireless": {"name": "Wireless Dock", "price": 30}
            }, 
            "accessories": {
                "none": {"name": "Watch Only", "price": 0}, 
                "bundle": {"name": "Case + Band", "price": 25}, 
                "premium_bundle": {"name": "Case + Band + Charger", "price": 40}
            } 
        }, 
        "user_questions": { 
            "own_smartwatch": {
                "question": "Do you own a smartwatch?", 
                "options": {
                    "yes": {"label": "Yes"}, 
                    "no": {"label": "No"}, 
                    "used_to": {"label": "Used to"}
                }
            }, 
            "main_reason": {
                "question": "Main reason for smartwatch?", 
                "options": {
                    "fitness": {"label": "Fitness"}, 
                    "productivity": {"label": "Productivity"}, 
                    "health": {"label": "Health"}, 
                    "style": {"label": "Style"}, 
                    "other": {"label": "Other"}
                }
            }, 
            "price_range": {
                "question": "Comfortable price range?", 
                "options": {
                    "under_100": {"label": "<$100"}, 
                    "100_199": {"label": "$100–199"}, 
                    "200_299": {"label": "$200–299"}, 
                    "300_plus": {"label": "$300+"}
                }
            }, 
            "phone_type": {
                "question": "Which phone?", 
                "options": {
                    "iphone": {"label": "iPhone"}, 
                    "android": {"label": "Android"}, 
                    "other": {"label": "Other"}
                }
            } 
        } 
    }
    
    b_step_order = ["color", "band_material", "size", "additional_features", "charging", "accessories", "own_smartwatch", "main_reason", "price_range", "phone_type"]
    b_step_titles = { 
        "color": "Choose Watch Color", 
        "band_material": "Select Your Band", 
        "size": "Select Size", 
        "additional_features": "Add Extra Features", 
        "charging": "Choose Charging Option", 
        "accessories": "Select Accessories Bundle", 
        "own_smartwatch": product["user_questions"]["own_smartwatch"]["question"], 
        "main_reason": product["user_questions"]["main_reason"]["question"], 
        "price_range": product["user_questions"]["price_range"]["question"], 
        "phone_type": product["user_questions"]["phone_type"]["question"] 
    }

    # --- Reactive Values (Version B specific) ---
    current_view = reactive.Value("b_initial") # "main", "b_initial", "b_sequence"
    current_b_step_index = reactive.Value(-1)
    b_selected_color = reactive.Value(None)
    b_selected_band = reactive.Value("silicone") # Default
    b_selected_size = reactive.Value("small")    # Default
    b_selected_features = reactive.Value([])
    b_selected_charging = reactive.Value("standard") # Default
    b_selected_accessories = reactive.Value("none") # Default
    b_insight_answers = reactive.Value({})
    
    # Flag to track if a modal is currently open
    modal_is_open = reactive.Value(False)

    # --- Color Data & Images ---
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

    # --- Helper Calcs ---
    @reactive.Calc
    def watch_images():
        # Get watch images based on B's selection state
        col = b_selected_color.get()
        default_col = "black"
        return [color_data[col or default_col]["front"], color_data[col or default_col]["side"]]
        
    # --- Navigation ---
    @reactive.Effect
    @reactive.event(input.view_product, input.view_product_btn_redundant, ignore_none=True, ignore_init=True)
    def handle_view_product():
        current_view.set("b_initial")
        print("DEBUG B: Navigating to b_initial")

    @reactive.Effect
    @reactive.event(input.start_b_preferences)
    def start_b_sequence():
         current_b_step_index.set(0)
         current_view.set("b_sequence")
         print("DEBUG B: Starting sequence (view=b_sequence, step=0)")

    @reactive.Effect
    @reactive.event(input.back_to_main)
    def go_back_to_main():
        # If a modal is open, close it first
        if modal_is_open.get():
            close_all_modals()
            
        current_view.set("main")
        current_b_step_index.set(-1)
        # Reset all selections
        b_selected_color.set(None)
        b_selected_band.set("silicone")
        b_selected_size.set("small")
        b_selected_features.set([])
        b_selected_charging.set("standard")
        b_selected_accessories.set("none")
        b_insight_answers.set({})
        print("DEBUG B: Navigating back to main, resetting state")

    # --- Color and Band Selection Handlers ---
    @reactive.Effect
    @reactive.event(input.b_selected_color_trigger)
    def handle_color_selection():
        val = input.b_selected_color_trigger()
        if val:
            b_selected_color.set(val)
            session.send_custom_message("js_select", {"container": "b_step_color_container", "value": val, "item_class": "step-color-option"})
            print(f"DEBUG B: Color selected: {val}")
            
    @reactive.Effect
    @reactive.event(input.b_selected_band_trigger)
    def handle_band_selection():
        val = input.b_selected_band_trigger()
        if val:
            b_selected_band.set(val)
            session.send_custom_message("js_select", {"container": "b_step_band_container", "value": val, "item_class": "step-band-option"})
            print(f"DEBUG B: Band selected: {val}")
      
    # --- Version B Step Navigation ---
    @reactive.Effect
    @reactive.event(input.b_step_next)
    def handle_b_step_next():
        current_idx = current_b_step_index.get()
        if current_idx < 0: 
            return
        if current_idx >= len(b_step_order): 
            print(f"DEBUG B: ERROR - handle_b_step_next bad index {current_idx}")
            go_back_to_main()
            return
            
        current_step_key = b_step_order[current_idx]
        is_valid = True
        value_to_save = None
        
        if current_step_key == "color": 
            value_to_save = b_selected_color.get()
            is_valid = bool(value_to_save)
        elif current_step_key == "band_material": 
            value_to_save = b_selected_band.get()
            is_valid = bool(value_to_save)
        elif current_step_key == "size": 
            value_to_save = input.b_selected_size()
            b_selected_size.set(value_to_save)
            is_valid = bool(value_to_save)
            if is_valid: 
                session.send_custom_message("ga_size", {"size": value_to_save})
        elif current_step_key == "additional_features": 
            value_to_save = input.b_selected_features()
            b_selected_features.set(list(value_to_save) if value_to_save else [])
            if value_to_save: 
                for feature in value_to_save: 
                    session.send_custom_message("ga_feature", {"feature": feature})
        elif current_step_key == "charging": 
            value_to_save = input.b_selected_charging()
            b_selected_charging.set(value_to_save)
            is_valid = bool(value_to_save)
            if is_valid: 
                session.send_custom_message("ga_bundle", {"bundle": value_to_save})
        elif current_step_key == "accessories": 
            value_to_save = input.b_selected_accessories()
            b_selected_accessories.set(value_to_save)
            is_valid = bool(value_to_save)
            if is_valid: 
                session.send_custom_message("ga_accessories", {"accessories": value_to_save})
        elif current_step_key in product["user_questions"]:
            input_id = f"b_answer_{current_step_key}"
            value_to_save = getattr(input, input_id)()  # Use getattr instead of input.get()
            is_valid = bool(value_to_save)
            if is_valid: 
                current_answers = dict(b_insight_answers.get())
                current_answers[current_step_key] = value_to_save
                b_insight_answers.set(current_answers)
                session.send_custom_message("ga_insight", {"question": current_step_key, "answer": value_to_save})

        if not is_valid: 
            ui.notification_show("Please make a selection.", duration=3, type="warning")
            return

        print(f"DEBUG B: Step {current_step_key} valid. Value='{value_to_save}'")
        next_idx = current_idx + 1
        if next_idx < len(b_step_order): 
            current_b_step_index.set(next_idx)
            print(f"DEBUG B: Moving to step index {next_idx}")
        else: 
            show_final_confirmation_modal()
            print("DEBUG B: Reached end of sequence, showing confirmation.")

    @reactive.Effect
    @reactive.event(input.b_step_back)
    def handle_b_step_back():
        current_idx = current_b_step_index.get()
        print(f"DEBUG B: Back clicked, current_idx={current_idx}")
        if current_idx > 0: 
            current_b_step_index.set(current_idx - 1)
        elif current_idx == 0: 
            current_view.set("b_initial") 
            current_b_step_index.set(-1)

    # --- Main Content Rendering ---
    @output
    @render.ui
    def main_content():
        view = current_view.get()
        step_idx = current_b_step_index.get()
        print(f"DEBUG B: Rendering main_content, view='{view}', step_idx={step_idx}")

        # --- HOMEPAGE ---
        if view == "main":
            return ui.div(
                {"class": "main-container"},
                ui.p("Help Us Shape Our Next Product!", class_="homepage-text"),
                ui.p("Explore the product and give us your preferences.", class_="homepage-text"),
                ui.div(
                    {"class": "product-card", "onclick": "Shiny.setInputValue('view_product', Math.random(), {priority: 'event'});"}, 
                    ui.img(src=watch_images()[0], class_="product-image"), 
                    ui.div({"class": "product-title"}, product["name"]), 
                    ui.div({"class": "product-price"}, f"${product['price']:.2f}"), 
                    ui.p(product["description"]), 
                    ui.input_action_button("view_product_btn_redundant", "View Product", class_="btn-primary btn-view-product")
                )
            )

        # --- B: INITIAL PRODUCT PAGE ---
        elif view == "b_initial":
            imgs = watch_images()
            carousel_items = [ui.tags.div({"class": "carousel-item active"}, ui.tags.img(src=imgs[0], class_="d-block w-100", alt="Watch"))]
            carousel = ui.tags.div(
                {"id": "carouselB_initial", "class": "carousel slide"}, 
                ui.tags.div({"class": "carousel-inner"}, *carousel_items)
            )
            
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
                    ui.div({"class": "product-details-left"}, carousel), 
                    ui.div(
                        {"class": "product-details-right"}, 
                        ui.h2(product["name"]), 
                        ui.p(f"Base Price: ${product['price']:.2f}"), 
                        ui.tags.ul(
                            {"class": "feature-highlights"}, 
                            *[ui.tags.li(ui.tags.i({"class": icon}), " ", feat) 
                            for icon, feat in zip(
                                ["bi-heart-fill", "bi-droplet-fill", "bi-battery-full", "bi-geo-alt-fill", "bi-bell-fill"], 
                                product["features"]
                            )]
                        ), 
                        ui.p(product["description"], class_="mt-3"), 
                        ui.hr(), 
                        ui.input_action_button(
                            "start_b_preferences", 
                            "Select Preferences →", 
                            class_="btn btn-primary btn-lg mt-3"
                        ) 
                    )
                )
            )

        # --- B: STEP SEQUENCE ---
        elif view == "b_sequence" and step_idx >= 0:
            if step_idx >= len(b_step_order): 
                print(f"DEBUG B: Invalid step_idx {step_idx}. Resetting.")
                current_view.set("b_initial")
                current_b_step_index.set(-1)
                return ui.div("Error: Invalid step.")
                
            current_step_key = b_step_order[step_idx]
            step_content_ui = None

            # --- Generate Step UI ---
            if current_step_key == "color":
                step_content_ui = ui.div(
                    {"id": "b_step_color_container"},
                    *[ui.div(
                        {
                            "class": "step-color-option",
                            "data-value": color_id,
                            "onclick": f"Shiny.setInputValue('b_selected_color_trigger', '{color_id}', {{priority: 'event'}}); selectBVariantItem('b_step_color_container', '{color_id}', 'step-color-option');"
                        },
                        ui.span({
                            "class": "color-swatch",  # GA tracking class
                            "style": f"background-color: {data['hex']};",
                            "data-color-name": data["name"]  # GA tracking label
                        }),
                        ui.span(data['name'])
                    ) for color_id, data in color_data.items()]
                )

            elif current_step_key == "band_material":
                step_content_ui = ui.div(
                    {"id": "b_step_band_container"}, 
                    *[ui.div(
                        {
                            "class": "step-band-option material-swatch",   # GA tracking class
                            "data-material-name": band_data["name"],       # GA tracking label
                            "data-value": band_id,
                            "onclick": f"Shiny.setInputValue('b_selected_band_trigger', '{band_id}', {{priority: 'event'}}); selectBVariantItem('b_step_band_container', '{band_id}', 'step-band-option');"
                        },
                        ui.img(src=band_material_images[band_id]), 
                        ui.div(
                            {"class": "step-band-details"}, 
                            ui.h5(band_data["name"]),
                            ui.p(f"+${band_data['price']}")
                        )
                    ) for band_id, band_data in product["customizations"]["band_material"].items()]
                )


            # --- Other Steps ---
            elif current_step_key == "size": 
                step_content_ui = ui.input_radio_buttons(
                    "b_selected_size", None,
                    {k: v["label"] for k, v in product["customizations"]["size"].items()},
                    selected=b_selected_size(), 
                    inline=False
                )
            elif current_step_key == "additional_features": 
                # Removed "Select features:" text as requested
                step_content_ui = ui.input_checkbox_group(
                    "b_selected_features", "",
                    {k: f"{v['name']} (+${v['price']})" for k, v in product["customizations"]["additional_features"].items()},
                    selected=b_selected_features(), 
                    inline=False
                )
            elif current_step_key == "charging": 
                step_content_ui = ui.input_radio_buttons(
                    "b_selected_charging", None,
                    {k: f"{v['name']} (+${v['price']})" for k, v in product["customizations"]["charging"].items()},
                    selected=b_selected_charging(), 
                    inline=False
                )
            elif current_step_key == "accessories": 
                step_content_ui = ui.input_radio_buttons(
                    "b_selected_accessories", None,
                    {k: f"{v['name']} (+${v['price']})" for k, v in product["customizations"]["accessories"].items()},
                    selected=b_selected_accessories(), 
                    inline=False
                )
            elif current_step_key in product["user_questions"]: 
                q_data = product["user_questions"][current_step_key]
                input_id = f"b_answer_{current_step_key}"
                stored_answer = b_insight_answers.get().get(current_step_key, None)
                step_content_ui = ui.input_radio_buttons(
                    input_id, None,
                    {k: v["label"] for k, v in q_data["options"].items()},
                    selected=stored_answer, 
                    inline=False
                )

            # --- Assemble Step Page UI ---
            progress_text = f"Step {step_idx + 1} of {len(b_step_order)}"
            return ui.div(
                {"class": "step-container"}, 
                ui.div(
                    {"class": "step-progress text-muted"}, 
                    ui.tags.strong(progress_text), ": ", 
                    b_step_titles.get(current_step_key, "")
                ), 
                ui.h4(b_step_titles.get(current_step_key, "")), 
                ui.hr(), 
                ui.div({"class": "step-content"}, step_content_ui), 
                ui.div(
                    {"class": "step-navigation"}, 
                    ui.input_action_button("b_step_back", "← Back", class_="btn btn-secondary"), 
                    ui.input_action_button(
                        "b_step_next", 
                        "Next →" if step_idx < len(b_step_order) - 1 else "Finish", 
                        class_="btn btn-primary"
                    )
                )
            )

        # --- Fallback ---
        else: 
            print(f"DEBUG B: Fallback rendering, view='{view}'")
            return ui.div("Loading...")

    # --- Helper functions for modals ---
    def close_all_modals():
        """Explicitly close all modals using JavaScript."""
        session.send_custom_message("close_modal", {})
        modal_is_open.set(False)

    # --- Final Confirmation Modal Logic ---
    def show_final_confirmation_modal():
        try:
            # Gather data from B's reactive state
            sel_color = b_selected_color.get()
            sel_band = b_selected_band.get()
            sel_size = b_selected_size.get()
            sel_features_keys = b_selected_features.get()
            sel_charging = b_selected_charging.get()
            sel_accessories = b_selected_accessories.get()
            final_insight_answers = b_insight_answers.get()
            
            if not sel_color: 
                ui.notification_show("Error: Color missing.", duration=4, type="error")
                return
                
            # Calculate Price
            base = product["price"]
            mat_cost = product["customizations"]["band_material"].get(sel_band, {"price": 0})["price"]
            siz_cost = product["customizations"]["size"].get(sel_size, {"price": 0})["price"]
            add_cost = sum(product["customizations"]["additional_features"].get(f, {"price": 0})["price"] for f in sel_features_keys)
            chg_cost = product["customizations"]["charging"].get(sel_charging, {"price": 0})["price"]
            acc_cost = product["customizations"]["accessories"].get(sel_accessories, {"price": 0})["price"]
            total = base + mat_cost + siz_cost + add_cost + chg_cost + acc_cost
            
            # Format Summary
            feature_names = [
                product["customizations"]["additional_features"][f]["name"] 
                for f in sel_features_keys 
                if f in product["customizations"]["additional_features"]
            ]
            features_str = ", ".join(feature_names) if feature_names else "None"
            
            insight_summary_ui = [
                ui.p(
                    f"{product['user_questions'][q_key]['question']}: {product['user_questions'][q_key]['options'].get(ans, {}).get('label', 'N/A')}"
                ) for q_key, ans in final_insight_answers.items()
            ]
            
            # Create the modal with direct Bootstrap dismissal
            confirmation_modal = ui.modal(
                ui.h3("Preferences Summary"), 
                ui.p("Review your selections:"), 
                ui.h4("Customization:"), 
                ui.p(f"Color: {color_data[sel_color]['name']}"), 
                ui.p(f"Band: {product['customizations']['band_material'][sel_band]['name']}"), 
                ui.p(f"Size: {product['customizations']['size'][sel_size]['label']}"), 
                ui.p(f"Features: {features_str}"), 
                ui.p(f"Charging: {product['customizations']['charging'][sel_charging]['name']}"), 
                ui.p(f"Accessories: {product['customizations']['accessories'][sel_accessories]['name']}"), 
                ui.p(f"Total Price: ${total:.2f}"), 
                ui.hr(), 
                ui.h4("Your Insights:"), 
                *insight_summary_ui,
                title="Configuration Summary",
                footer=ui.div(
                    ui.tags.button(
                        "Submit Preferences", 
                        id="submit_button",
                        class_="btn btn-success",
                        # This will both dismiss the modal and trigger our event
                        onclick="$('.modal').modal('hide'); Shiny.setInputValue('submit_preferences_clicked', Math.random(), {priority: 'event'});"
                    ),
                    ui.tags.button(
                        "Close", 
                        id="close_button",
                        class_="btn btn-secondary ms-2",
                        # Simple Bootstrap dismiss
                        **{"data-bs-dismiss": "modal"}
                    )
                ),
                easy_close=True,
                size="lg"
            )
            
            # Update the modal output
            @output(id="modal_output_placeholder")
            @render.ui
            def _():
                return confirmation_modal
                
            # Show the modal
            ui.modal_show(confirmation_modal)
            
        except Exception as e:
            print(f"DEBUG B: Error showing confirmation modal: {str(e)}")
            ui.notification_show(f"Error: {str(e)}", duration=5, type="error")

    # Add a simple handler for submit preferences
    @reactive.Effect
    @reactive.event(input.submit_preferences_clicked)
    def handle_submit_preferences():
        # Show success message
        ui.notification_show(
            "Preferences submitted successfully! Thank you for your feedback.", 
            duration=4, 
            type="success"
        )
            
        # Reset the app state
        current_view.set("b_initial")
        current_b_step_index.set(-1)
        b_selected_color.set(None)
        b_selected_band.set("silicone")
        b_selected_size.set("small")
        b_selected_features.set([])
        b_selected_charging.set("standard")
        b_selected_accessories.set("none")
        b_insight_answers.set({})
        print("DEBUG B: Preferences submitted, app reset")
        
    # Update handlers to use new input values
    @reactive.Effect
    @reactive.event(input.finish_preferences)
    def handle_finish_preferences():
        # Just close modal and reset app
        ui.modal_remove()
        modal_is_open.set(False)
        
        # Show success message
        ui.notification_show(
            "Preferences submitted successfully! Thank you for your feedback.", 
            duration=4, 
            type="success"
        )
        
        # Reset the app state immediately
        current_view.set("b_initial")
        current_b_step_index.set(-1)
        b_selected_color.set(None)
        b_selected_band.set("silicone")
        b_selected_size.set("small")
        b_selected_features.set([])
        b_selected_charging.set("standard")
        b_selected_accessories.set("none")
        b_insight_answers.set({})
        print("DEBUG B: Preferences submitted, app reset")

    @reactive.Effect
    @reactive.event(input.cancel_preferences)
    def handle_cancel_preferences():
        # Just close the modal
        ui.modal_remove()
        modal_is_open.set(False)
        print("DEBUG B: Modal closed without submission")

    # --- Modal Events ---
    @reactive.Effect
    @reactive.event(input.submit_preferences_trigger)
    def handle_submit_preferences():
        # Close the modal
        close_all_modals()
        
        # Show success message
        ui.notification_show(
            "Preferences submitted successfully! Thank you for your feedback.", 
            duration=4, 
            type="success"
        )
        
        # Reset the app state
        def reset_app_after_delay():
            current_view.set("b_initial")
            current_b_step_index.set(-1)
            # Reset selection state to defaults
            b_selected_color.set(None)
            b_selected_band.set("silicone")
            b_selected_size.set("small")
            b_selected_features.set([])
            b_selected_charging.set("standard")
            b_selected_accessories.set("none")
            b_insight_answers.set({})
        
        @reactive.Effect
        @reactive.event(input.close_preferences_trigger)
        def handle_close_preferences_modal():
            # Just close the modal without resetting the flow
            close_all_modals()
    
    # --- Subscribe Modal ---
    @reactive.Effect
    @reactive.event(input.join_waitlist)
    def handle_join_waitlist():
        # Create the subscribe modal
        subscribe_modal = ui.modal(
            ui.h3("Subscribe for Updates"),
            ui.p("Sign up to receive news and special offers about our products."),
            ui.input_text("email_input", "Email Address", placeholder="your@email.com"),
            ui.input_checkbox("marketing_consent", "I agree to receive marketing emails", value=True),
            footer=ui.div(
                ui.input_action_button("submit_email", "Subscribe", class_="btn btn-primary"),
                ui.tags.button(  # Changed from input_action_button to tags.button
                    "Close", 
                    id="close_waitlist_modal",
                    class_="btn btn-secondary ms-2",
                    **{"data-bs-dismiss": "modal"}  # This is the key addition
                )
            ),
            easy_close=True,
            title="Stay Updated"
        )
        
        # Update the modal output
        @output(id="modal_output_placeholder")
        @render.ui
        def _():
            return subscribe_modal
        
        # Show the modal - pass the modal object as an argument
        ui.modal_show(subscribe_modal)
        modal_is_open.set(True)
    
    @reactive.Effect
    @reactive.event(input.submit_email)
    def handle_submit_email():
        email = input.email_input()
        
        # Validate email
        if email and "@" in email and "." in email:
            close_all_modals()
            ui.notification_show(
                "Thanks for subscribing! You'll receive updates on our latest products.", 
                duration=4, 
                type="success"
            )
        else:
            ui.notification_show(
                "Please enter a valid email address.", 
                duration=3, 
                type="warning"
            )
    
    @reactive.Effect
    @reactive.event(input.close_waitlist_modal)
    def handle_close_waitlist_modal():
        close_all_modals()

# =============================================================================
# App Definition (Version B)
# =============================================================================
app = App(ui=version_b_ui, server=server_b)