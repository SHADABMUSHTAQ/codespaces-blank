import streamlit as st
from fpdf import FPDF

# --- PAGE CONFIG ---
st.set_page_config(page_title="RealtorAI Luxury", page_icon="🏢", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .main-header {font-size:32px; font-weight:bold; color:#FFFFFF; margin-bottom: 20px;}
    .sub-header {font-size:18px; color:#E2E8F0;}
    .stButton>button {width: 100%; border-radius: 8px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("RealtorAI 💎")
    st.caption("Premium Brochure Generator")
    st.markdown("---")
    st.write("Create high-end marketing materials in seconds.")

# --- HEADER ---
st.markdown('<p class="main-header">💎 Luxury Property Brochure Generator</p>', unsafe_allow_html=True)

# --- INPUT FORM ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏠 Property Info")
    property_type = st.selectbox("Property Type", ["Luxury Villa", "Modern Apartment", "Penthouse Suite", "Commercial Floor"])
    location = st.text_input("Location", value="Emaar Oceanfront, Karachi")
    price = st.text_input("Price (e.g. 8.5 Crore)", value="8.5 Crore")

with col2:
    st.markdown("### 🛋️ Specs")
    bedrooms = st.slider("Bedrooms", 2, 8, 4)
    bathrooms = st.slider("Bathrooms", 2, 8, 5)
    sq_ft = st.number_input("Area (Sq Ft)", 1000, 50000, 4500)

with col3:
    st.markdown("### 🌟 Features")
    parking = st.selectbox("Parking", ["2 Covered Spaces", "Multi-Car Garage", "Underground Parking"])
    furnishing = st.select_slider("Furnishing", options=["Shell Core", "Semi-Furnished", "Designer Furnished"])

features = st.text_area("✨ Key Highlights (Comma separated)", 
                        "Panoramic Sea View, Private Elevator, Italian Marble Flooring, Smart Home System")

tone = st.select_slider("🎭 Description Tone", options=["Professional", "Elegant/Luxury", "Urgent/Investment"])

# --- HELPER FUNCTION: TEXT CLEANER (Ye Error Rokega) ---
def clean_text(text):
    # Ye function har text ko check karega aur emojis/symbols hata dega
    if text:
        return text.encode('latin-1', 'ignore').decode('latin-1')
    return ""

# --- LOGIC ENGINE ---
def generate_luxury_text():
    openings = {
        "Elegant/Luxury": f"Experience unparalleled luxury in this exquisite {furnishing} {property_type} located in the prestigious {location}.",
        "Urgent/Investment": f"Prime Investment Opportunity! A rare {property_type} in {location} priced at {price} for immediate sale.",
        "Professional": f"We are privileged to present this premium {sq_ft} sq ft {property_type} situated in {location}."
    }
    opening_line = openings.get(tone, openings["Professional"])
    
    layout_desc = (f"Spanning an impressive {sq_ft} sq ft, this residence features {bedrooms} master suites and {bathrooms} designer bathrooms. "
                   f"It comes with {parking} and is offered {furnishing}.")
    
    amenities_desc = f"Exclusive highlights include: {features}."
    
    closing = f"Listing Price: {price}. Viewings by appointment only."
    
    return f"{opening_line}\n\n{layout_desc}\n\n{amenities_desc}\n\n{closing}"

# --- 🎨 ULTRA-ADVANCED PDF FUNCTION ---
def create_luxury_pdf(text, details):
    pdf = FPDF()
    pdf.add_page()
    
    # --- Colors Definition ---
    NAVY = (10, 25, 60)
    GOLD = (184, 134, 11)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (245, 245, 245)

    # 1. Top Branding Banner
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(*WHITE)
    pdf.set_y(10)
    pdf.cell(0, 10, "PREMIUM REALTY COLLECTION", align='C', ln=True)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 5, "Excellence in Every Square Foot", align='C')

    # 2. Placeholder Image
    try:
        # Agar image load na ho to crash na kare
        pdf.image("https://via.placeholder.com/800x400.png?text=Luxury+Property", x=10, y=40, w=190, h=85)
    except:
        pdf.set_fill_color(220, 220, 220)
        pdf.rect(10, 40, 190, 85, 'F')

    # 3. Property Title & Price Section
    pdf.set_y(130)
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(*NAVY)
    
    # SAFETY CLEANER APPLIED HERE
    title = f"{clean_text(details['type'])} in {clean_text(details['loc'])}"
    pdf.cell(130, 15, title, ln=False)
    
    # Price Accent
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(*GOLD)
    pdf.cell(60, 15, clean_text(details['price']), align='R', ln=True)

    # 4. Modern Info-Bar
    pdf.set_fill_color(*LIGHT_GRAY)
    pdf.set_draw_color(*WHITE)
    pdf.set_line_width(1)
    pdf.rect(10, 148, 190, 18, 'F')
    
    pdf.set_y(148)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(50, 50, 50)
    
    cell_w = 190 / 4
    pdf.set_x(10)
    # SAFETY CLEANER APPLIED HERE TOO
    pdf.cell(cell_w, 18, f"AREA: {details['area']} Sq Ft", align='C', border='R')
    pdf.cell(cell_w, 18, f"BEDS: {details['bed']}", align='C', border='R')
    pdf.cell(cell_w, 18, f"BATHS: {details['bath']}", align='C', border='R')
    pdf.cell(cell_w, 18, clean_text(details['park']), align='C')
    
    pdf.ln(25)

    # 5. Description Section
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "Property Details", ln=True)
    pdf.set_fill_color(*GOLD)
    pdf.rect(10, pdf.get_y(), 40, 1, 'F')
    pdf.ln(8)
    
    # Body Text
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(40, 40, 40)
    # SAFETY CLEANER APPLIED HERE
    pdf.multi_cell(0, 7, clean_text(text))

    # 6. Footer Section
    pdf.set_y(-30)
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 267, 210, 30, 'F')
    pdf.set_y(-22)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 10, "Contact Agent: +92 300 1234567 | www.youragency.com", align='C')

    return pdf.output(dest="S").encode("latin-1")

# --- ACTION BUTTONS ---
if st.button("💎 Generate Luxury Brochure", type="primary"):
    with st.spinner("Designing premium brochure..."):
        result = generate_luxury_text()
        
        st.success("Brochure Ready!")
        
        # Details Dictionary
        prop_details = {
            "loc": location, "price": price, "type": property_type,
            "area": sq_ft, "bed": bedrooms, "bath": bathrooms, "park": parking
        }
        
        # Generate & Download
        try:
            pdf_data = create_luxury_pdf(result, prop_details)
            
            col1, col2 = st.columns([2,1])
            with col1:
                 st.text_area("Description Preview:", value=result, height=150)
            with col2:
                st.info("👇 Download the final designed PDF below.")
                st.download_button("📄 Download Luxury PDF", data=pdf_data, file_name="Luxury_Brochure.pdf", mime="application/pdf", use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")