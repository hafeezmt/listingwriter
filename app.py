import gradio as gr
import ollama

MODEL = "gemma4:e2b-it-qat"

BASE_RULES = (
    "You are ListingWriter, a Nigerian real estate copywriter. "
    "Use ONLY the details given. Never invent features, amenities, "
    "estate names or prices. Keep the naira sign (₦) exactly as given. "
    "Output only the requested text, nothing else."
)

TASKS = {
    "full": (
        "Write a property listing of about 120 words. Format: a catchy headline "
        "on the first line, then a short description paragraph, then 4 to 6 "
        "bullet points using only the given details, then one closing line "
        "with the contact. No hashtags. No emojis."
    ),
    "whatsapp": (
        "Write ONE short WhatsApp broadcast message under 60 words. Include the "
        "property type, location, price, key features and the contact. "
        "Use 2 or 3 emojis. No hashtags."
    ),
    "instagram": (
        "Write ONE Instagram caption under 50 words with 3 or 4 emojis and a "
        "call to action. End with 8 relevant hashtags on one line. "
        "Do not write placeholders like [Link]."
    ),
}

LIMITS = {"full": 300, "whatsapp": 130, "instagram": 130}


def fix_price(price):
    price = price.strip()
    if price and price[0].isdigit():
        price = "₦" + price
    return price


def clean(text):
    return text.replace("«", "").replace("```", "").strip()


def ask(task, details, language):
    lang_note = ""
    if language == "Nigerian Pidgin":
        lang_note = " Write in simple Nigerian Pidgin English."
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": BASE_RULES + lang_note},
            {"role": "user",
             "content": TASKS[task] + "\n\nProperty details:\n" + details},
        ],
        options={
            "temperature": 0.6,
            "num_predict": LIMITS[task],
            "repeat_penalty": 1.15,
        },
    )
    return clean(response["message"]["content"])


def generate(prop_type, location, price, bedrooms, bathrooms,
             features, tone, language, agent_name, phone):
    if not location or not price:
        raise gr.Error("Please fill in at least the location and the price.")

    contact = " - ".join([x for x in [agent_name, phone] if x]) or "Not provided"
    details = (
        f"Property type: {prop_type}\n"
        f"Location: {location}\n"
        f"Price: {fix_price(price)}\n"
        f"Bedrooms: {int(bedrooms or 0)}\n"
        f"Bathrooms: {int(bathrooms or 0)}\n"
        f"Features: {features or 'Not given'}\n"
        f"Tone: {tone}\n"
        f"Contact: {contact}\n"
    )

    try:
        yield "Writing your listing...", "Waiting...", "Waiting..."
        full = ask("full", details, language)
        yield full, "Writing...", "Waiting..."
        wa = ask("whatsapp", details, language)
        yield full, wa, "Writing..."
        ig = ask("instagram", details, language)
        yield full, wa, ig
    except Exception as e:
        raise gr.Error(
            f"Could not reach Ollama. Is 'ollama serve' running? Details: {e}"
        )


def clear_all():
    return "", "", ""


# ---------- Design ----------
GREEN = "#0B5D3B"
GREEN_DARK = "#08432B"
GOLD = "#C8963E"
CREAM = "#F7F3EA"
INK = "#1C2B24"

theme = gr.themes.Base(
    primary_hue="emerald",
    neutral_hue="stone",
    radius_size=gr.themes.sizes.radius_lg,
    font=[gr.themes.GoogleFont("DM Sans"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill=CREAM,
    body_background_fill_dark=CREAM,
    body_text_color=INK,
    body_text_color_dark=INK,
    block_background_fill="#FFFFFF",
    block_background_fill_dark="#FFFFFF",
    block_border_color="#E7DFCF",
    block_border_color_dark="#E7DFCF",
    block_label_text_color=GREEN,
    block_label_text_color_dark=GREEN,
    block_label_background_fill="#FFFFFF",
    block_label_background_fill_dark="#FFFFFF",
    block_title_text_color=GREEN,
    block_title_text_color_dark=GREEN,
    input_background_fill="#FBF9F4",
    input_background_fill_dark="#FBF9F4",
    input_border_color="#E0D6C2",
    input_border_color_dark="#E0D6C2",
    input_border_color_focus=GREEN,
    input_border_color_focus_dark=GREEN,
    button_primary_background_fill=GREEN,
    button_primary_background_fill_dark=GREEN,
    button_primary_background_fill_hover=GREEN_DARK,
    button_primary_background_fill_hover_dark=GREEN_DARK,
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
    button_secondary_background_fill="#FFFFFF",
    button_secondary_background_fill_dark="#FFFFFF",
    button_secondary_text_color=GREEN,
    button_secondary_text_color_dark=GREEN,
    table_even_background_fill="#FFFFFF",
    table_even_background_fill_dark="#FFFFFF",
    table_odd_background_fill="#FBF9F4",
    table_odd_background_fill_dark="#FBF9F4",
    table_row_focus="#E6F2EB",
    table_row_focus_dark="#E6F2EB",
    table_text_color=INK,
    table_text_color_dark=INK,
    table_border_color="#E7DFCF",
    table_border_color_dark="#E7DFCF",
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

.gradio-container { max-width: 1120px !important; margin: 0 auto !important; }
footer { display: none !important; }

/* Hero */
#hero {
  background: linear-gradient(135deg, #0B5D3B 0%, #0E7A4D 60%, #148A58 100%);
  border-radius: 22px;
  padding: 36px 36px 30px 36px;
  margin: 8px 0 22px 0;
  position: relative;
  overflow: hidden;
}
#hero::after {
  content: "";
  position: absolute; right: -60px; top: -60px;
  width: 240px; height: 240px; border-radius: 50%;
  background: radial-gradient(circle, rgba(200,150,62,.55), rgba(200,150,62,0) 70%);
}
#hero h1 {
  font-family: 'Fraunces', Georgia, serif;
  color: #FFFFFF !important;
  font-size: 2.4rem; line-height: 1.1; margin: 0 0 10px 0;
}
#hero p { color: #D8EFE3 !important; font-size: 1.05rem; margin: 0 0 18px 0; max-width: 640px; }
#hero .chips span {
  display: inline-block; margin: 0 8px 8px 0; padding: 6px 14px;
  border-radius: 999px; font-size: .82rem; font-weight: 600;
  background: rgba(255,255,255,.14); color: #FFFFFF;
  border: 1px solid rgba(255,255,255,.28);
}
#hero .chips span.gold { background: #C8963E; border-color: #C8963E; color: #1C2B24; }

/* Section titles */
.step-title h3 {
  font-family: 'Fraunces', Georgia, serif;
  color: #0B5D3B !important; margin: 4px 0 8px 0 !important; font-size: 1.25rem;
}

/* Cards */
.card { border-radius: 18px !important; border: 1px solid #E7DFCF !important;
        box-shadow: 0 6px 20px rgba(11,93,59,.06); }

/* Output cards */
.out-card { border-radius: 18px !important; overflow: hidden;
            border: 1px solid #E7DFCF !important; border-top-width: 5px !important;
            box-shadow: 0 6px 20px rgba(11,93,59,.06); margin-bottom: 14px; }
.out-card.full { border-top-color: #0B5D3B !important; }
.out-card.wa   { border-top-color: #25D366 !important; }
.out-card.ig   { border-top-color: #D6249F !important; }
.out-card textarea { font-size: 0.98rem !important; line-height: 1.6 !important; }

/* Buttons */
#go-btn { font-size: 1.1rem !important; font-weight: 700 !important;
          padding: 14px 18px !important; border-radius: 14px !important;
          box-shadow: 0 8px 20px rgba(11,93,59,.28); }
#clear-btn { border-radius: 14px !important; }

/* Examples */
#examples-wrap { margin-top: 6px; }
#examples-wrap table { font-size: .85rem; }

#examples-wrap table, #examples-wrap .table-wrap { background: #FFFFFF !important; }
#examples-wrap td, #examples-wrap td * { background: #FFFFFF !important; color: #1C2B24 !important; }
#examples-wrap tr:nth-child(even) td { background: #FBF9F4 !important; }
#examples-wrap tr:hover td { background: #E6F2EB !important; cursor: pointer; }
#examples-wrap th { background: #F1EBDD !important; color: #0B5D3B !important; }

#footer-note { text-align: center; color: #7A7466; font-size: .88rem; margin: 18px 0 6px 0; }
"""

EXAMPLES = [
    ["Flat / Apartment", "Pantami, Gombe", "₦1,500,000 per year", 3, 2,
     "tiled floors, borehole, 24hr light, fenced, ample parking",
     "Professional", "English", "", ""],
    ["Duplex", "Maitama, Abuja", "₦120,000,000", 5, 6,
     "BQ, swimming pool, CCTV, smart home, gated estate",
     "Luxury", "English", "", ""],
    ["Land", "Billiri Road, Gombe", "₦3,000,000", 0, 0,
     "600 sqm, dry land, C of O, close to the road",
     "Friendly", "Nigerian Pidgin", "", ""],
]

with gr.Blocks(title="ListingWriter") as demo:
    gr.HTML(
        """
        <div id="hero">
          <h1>🏠 ListingWriter</h1>
          <p>Type the property details once. Get a full listing, a WhatsApp
          message and an Instagram caption, ready to post.</p>
          <div class="chips">
            <span class="gold">Runs on your computer</span>
            <span>Open-source AI</span>
            <span>English + Pidgin</span>
            <span>No data leaves your device</span>
          </div>
        </div>
        """
    )

    with gr.Row(equal_height=False):
        with gr.Column(scale=5):
            gr.Markdown("### 1. Property details", elem_classes=["step-title"])
            with gr.Group(elem_classes=["card"]):
                prop_type = gr.Dropdown(
                    ["House", "Flat / Apartment", "Duplex", "Bungalow",
                     "Land", "Shop / Office", "Hostel / Self-contain"],
                    value="Flat / Apartment", label="Property type",
                )
                location = gr.Textbox(label="Location",
                                      placeholder="e.g. Pantami, Gombe")
                price = gr.Textbox(label="Price",
                                   placeholder="e.g. ₦1,500,000 per year")
                with gr.Row():
                    bedrooms = gr.Number(label="Bedrooms", value=3, precision=0)
                    bathrooms = gr.Number(label="Bathrooms", value=2, precision=0)
                features = gr.Textbox(
                    label="Features",
                    lines=3,
                    placeholder="e.g. tiled floors, borehole, 24hr light, "
                                "fenced, ample parking, close to the road",
                )

            gr.Markdown("### 2. Style and contact", elem_classes=["step-title"])
            with gr.Group(elem_classes=["card"]):
                with gr.Row():
                    tone = gr.Dropdown(["Professional", "Friendly", "Luxury"],
                                       value="Professional", label="Tone")
                    language = gr.Dropdown(["English", "Nigerian Pidgin"],
                                           value="English", label="Language")
                with gr.Row():
                    agent_name = gr.Textbox(label="Agent name (optional)")
                    phone = gr.Textbox(label="Phone / WhatsApp (optional)")

            btn = gr.Button("✨ Generate listing", variant="primary",
                            elem_id="go-btn")
            clear_btn = gr.Button("Clear results", elem_id="clear-btn")

            with gr.Column(elem_id="examples-wrap"):
                gr.Markdown("**Try an example (click to fill the form)**")
                with gr.Row():
                    ex1 = gr.Button("🏢 Flat in Gombe", size="sm")
                    ex2 = gr.Button("🏰 Duplex in Abuja", size="sm")
                    ex3 = gr.Button("🌍 Land (Pidgin)", size="sm")
                _form = [prop_type, location, price, bedrooms, bathrooms,
                         features, tone, language, agent_name, phone]
                ex1.click(lambda: EXAMPLES[0], outputs=_form)
                ex2.click(lambda: EXAMPLES[1], outputs=_form)
                ex3.click(lambda: EXAMPLES[2], outputs=_form)

        with gr.Column(scale=6):
            gr.Markdown("### 3. Your posts", elem_classes=["step-title"])
            with gr.Group(elem_classes=["out-card", "full"]):
                out_full = gr.Textbox(label="📄 Full listing", lines=11,
                                      buttons=["copy"],
                                      placeholder="Your full listing will appear here...")
            with gr.Group(elem_classes=["out-card", "wa"]):
                out_wa = gr.Textbox(label="💬 WhatsApp message", lines=5,
                                    buttons=["copy"],
                                    placeholder="Your WhatsApp message will appear here...")
            with gr.Group(elem_classes=["out-card", "ig"]):
                out_ig = gr.Textbox(label="📸 Instagram caption", lines=5,
                                    buttons=["copy"],
                                    placeholder="Your Instagram caption will appear here...")

    gr.HTML(
        '<div id="footer-note">Built for the Hacktoberfest Open-Source AI '
        'Challenge · Powered by Gemma and Ollama · Review each post before you share it</div>'
    )

    btn.click(
        generate,
        inputs=[prop_type, location, price, bedrooms, bathrooms,
                features, tone, language, agent_name, phone],
        outputs=[out_full, out_wa, out_ig],
    )
    clear_btn.click(clear_all, outputs=[out_full, out_wa, out_ig])

if __name__ == "__main__":
    demo.launch(theme=theme, css=CSS)
