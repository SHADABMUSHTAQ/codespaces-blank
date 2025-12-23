import streamlit as st
import random

# Page Config
st.set_page_config(page_title="RealtorAI - Listing Generator", page_icon="🏠")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.info("No API Key Required! This runs on Logic.")
    st.markdown("---")
    st.write("Designed for Global Real Estate Agents")

# Main Heading
st.title("🏠 AI Real Estate Description Generator")
st.subheader("Turn property details into a selling story in seconds.")

# --- INPUT FORM ---
col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox("Property Type", ["Apartment", "House/Villa", "Office Space", "Condo"])
    bedrooms = st.slider("Number of Bedrooms", 1, 10, 3)
    bathrooms = st.slider("Number of Bathrooms", 1, 10, 2)

with col2:
    location = st.text_input("Location (e.g., Downtown Dubai, NYC)", value="Karachi, DHA")
    sq_ft = st.number_input("Area (Sq Ft)", min_value=100, value=1500)
    price = st.text_input("Price (Optional)", value="2 Crore")

# Key Features
features = st.text_area("Key Features (comma separated)", 
                        "Swimming pool, Modern Kitchen, Near Metro Station, Hardwood floors, Balcony view")

# Tone Selection
tone = st.select_slider("Select Tone", options=["Urgent", "Professional", "Luxury", "Cozy/Family", "Witty"])

# --- LOGIC (BINA API KE) ---
def generate_description_logic():
    # Hum yahan template use karenge bajaye AI ke
    
    # 1. Opening Lines based on Tone
    openings = {
        "Urgent": f"Don't miss out on this incredible {property_type} in the heart of {location}!",
        "Professional": f"Presenting a premium {property_type} located in the prestigious area of {location}.",
        "Luxury": f"Experience the pinnacle of elegance with this stunning {property_type} in {location}.",
        "Cozy/Family": f"Welcome home! A beautiful, family-friendly {property_type} awaits you in {location}.",
        "Witty": f"Tired of looking at boring houses? Check out this {property_type} in {location} before someone else snags it!"
    }
    
    opening_line = openings.get(tone, openings["Professional"])

    # 2. Body Paragraph
    body = (f"This spacious property spans {sq_ft} sq ft and features {bedrooms} bedrooms and {bathrooms} bathrooms. "
            f"Listed at a competitive price of {price}, it offers the perfect blend of comfort and style. "
            f"Whether you are looking for an investment or a dream home, this checks all the boxes.")

    # 3. Features Formatting
    feature_list = [f.strip() for f in features.split(',')]
    feature_bullets = "\n".join([f"- ✨ {f}" for f in feature_list])

    # 4. Final Text Construction
    full_text = f"""
{opening_line}

{body}

**Key Highlights:**
{feature_bullets}

📞 Contact us today for a viewing!
    """
    return full_text

# --- ACTION BUTTON ---
if st.button("✨ Generate Listing Description", type="primary"):
    with st.spinner('Writing description...'):
        result = generate_description_logic()
        
    if result:
        st.markdown("### Copy Your Description:")
        st.text_area("Generated Text", value=result, height=300)
        st.success("Description generated successfully!")

# Footer
st.markdown("---")
st.caption("Built for flipping on MicroAcquire.")