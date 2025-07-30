from xml.parsers.expat import model
import streamlit as st
import pytesseract
from PIL import Image
import time

# Set the Tesseract executable path (Windows example)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Try to import EasyOCR, fall back gracefully if not available
EASYOCR_AVAILABLE = False
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except:
    pass

# Tesseract maintenance flag
TESSERACT_MAINTENANCE = True

# Configure page
st.set_page_config(
    page_title="Image to Text Converter",
    page_icon="📝",
    layout="wide"
)

def show_maintenance_popup():
    """Show maintenance popup for Tesseract"""
    st.error("🚧 **Tesseract OCR is currently under maintenance**")
    st.warning("Please use EasyOCR for text extraction at the moment. We apologize for the inconvenience!")

def extract_text_tesseract(image, language='eng'):
    """Extract text using Tesseract OCR"""
    try:
        text = pytesseract.image_to_string(image, lang=language)
        return text
    except Exception as e:
        return f"Error extracting text with Tesseract: {str(e)}"

def extract_text_easyocr(image):
    """Extract text using EasyOCR"""
    if not EASYOCR_AVAILABLE:
        return None
    
    try:
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(img_byte_arr, detail=0)
        return ' '.join(result)
    except Exception as e:
        return f"Error extracting text with EasyOCR: {str(e)}"

def preprocess_image(image, enhance_contrast=False, resize_factor=1.0):
    """Preprocess image for better OCR results"""
    try:
        # Resize if needed
        if resize_factor != 1.0:
            new_size = (int(image.width * resize_factor), int(image.height * resize_factor))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to grayscale and enhance contrast if requested
        if enhance_contrast:
            if image.mode != 'L':
                image = image.convert('L')
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
        
        return image
    except Exception as e:
        st.error(f"Error preprocessing image: {str(e)}")
        return image

# Main app
def main():
    st.title("📝 Image to Text Converter")
    st.markdown("Upload an image and get the text instantly")
    t_model=None
    # Sidebar for options
    st.sidebar.header("⚙️ OCR Settings")
    
    # Engine selection with maintenance check
    if EASYOCR_AVAILABLE and not TESSERACT_MAINTENANCE:
        # Normal operation - both engines available
        ocr_engine = st.sidebar.selectbox(
            "Choose OCR Engine:",
            ["EasyOCR", "Tesseract", "Both"],
            help="EasyOCR: Better for complex images | Tesseract: Faster processing"
        )
    elif EASYOCR_AVAILABLE and TESSERACT_MAINTENANCE:
        # Tesseract under maintenance - only EasyOCR available
        ocr_engine = st.sidebar.selectbox(
            "Choose OCR Engine:",
            ["EasyOCR","Tesseract (Maintenance)"],
            help="EasyOCR: Better for complex images"
        )
        if ocr_engine == "Tesseract (Maintenance)":
            st.sidebar.info("Tesseract is currently under maintenance. Please use EasyOCR for text extraction.(Continuing with EasyOCR)")
            t_model = "Tesseract (maintenance)"
            ocr_engine = "EasyOCR"

        
        # Show maintenance notice in sidebar
        with st.sidebar.expander("⚠️ Maintenance Notice"):
            st.markdown("""
            **Tesseract OCR is temporarily unavailable**
            
            We're performing maintenance to improve performance. 
            Please use EasyOCR for now.
            
            Expected resolution: Soon
            """)
            
    elif not EASYOCR_AVAILABLE and TESSERACT_MAINTENANCE:
        # Both unavailable - show error
        st.sidebar.error("❌ No OCR engines available")
        st.sidebar.markdown("Both Tesseract (maintenance) and EasyOCR (not installed) are unavailable")
        ocr_engine = None
        
    elif not EASYOCR_AVAILABLE and not TESSERACT_MAINTENANCE:
        # Only Tesseract available
        ocr_engine = "Tesseract"
        st.sidebar.info("💡 Only Tesseract is available")
        st.sidebar.markdown("To enable EasyOCR, install Visual C++ Redistributable")
    
    # Language selection (only show if Tesseract is available and not in maintenance)
    if ocr_engine in ["Tesseract", "Both"] and not TESSERACT_MAINTENANCE:
        language_options = {
            'English': 'eng',
            'Arabic': 'ara',
            'French': 'fra',
            'German': 'deu',
            'Spanish': 'spa',
            'Hindi': 'hin',
            'Urdu': 'urd'
        }
        
        selected_lang = st.sidebar.selectbox(
            "Language (Tesseract):",
            list(language_options.keys()),
            index=0
        )

    # OCR engine information
    if EASYOCR_AVAILABLE:
        st.sidebar.markdown(
            "<p style='font-size: 12px;'>EasyOCR takes more time but handles complex images better. Tesseract is faster for simpler text and well-structured documents.</p>",
            unsafe_allow_html=True
        )
    
    # Image enhancement options
    st.sidebar.subheader("🖼️ Image Enhancement")
    enhance_contrast = st.sidebar.checkbox("Enhance Contrast", value=False)
    resize_factor = st.sidebar.slider("Resize Factor", 0.5, 2.0, 1.0, 0.1)
    
    # Developer credit
    st.sidebar.markdown(
        """
        <div style='text-align: center; padding-top: 15px;'>
            <hr style='border: 0.5px solid #ccc;'/>
            <p style='font-size: 20px; font-weight: 500; color: #ccc;'>Developed by <strong>Raza Khan</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Check if no OCR engines are available
    if ocr_engine is None:
        st.error("🚫 **No OCR engines are currently available**")
        st.markdown("""
        **Current Status:**
        - 🚧 Tesseract OCR: Under maintenance
        - ❌ EasyOCR: Not installed
        
        Please try again later or contact support.
        """)
        return

    # Simple file uploader
    uploaded_file = st.file_uploader(
        "Drop your image here or click to browse",
        type=['png', 'jpg', 'jpeg', 'tiff', 'bmp']
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Image", width=400)
        
        # Check if trying to use Tesseract during maintenance
        if TESSERACT_MAINTENANCE and ocr_engine in ["Tesseract", "Both"]:
            show_maintenance_popup()
            return
        
        # Process image based on settings
        with st.spinner("Extracting text..."):
            # Apply preprocessing
            processed_image = preprocess_image(
                image, 
                enhance_contrast=enhance_contrast,
                resize_factor=resize_factor
            )
            
            # Extract text based on selected engine
            if ocr_engine == "EasyOCR" and EASYOCR_AVAILABLE:
                text = extract_text_easyocr(processed_image)
                if text and not text.startswith("Error extracting"):
                    st.success("✅ EasyOCR extraction completed!")
                else:
                    st.error("❌ EasyOCR failed, please try with different settings")
                    text = None
                    
            elif ocr_engine == "Tesseract" and not TESSERACT_MAINTENANCE:
                text = extract_text_tesseract(processed_image, language_options[selected_lang])
                if text and not text.startswith("Error extracting"):
                    st.success("✅ Tesseract extraction completed!")
                else:
                    st.error("❌ Could not extract text")
                    text = None
                    
            elif ocr_engine == "Both" and EASYOCR_AVAILABLE and not TESSERACT_MAINTENANCE:
                # Show both results
                st.markdown("### 🤖 EasyOCR Results")
                easyocr_text = extract_text_easyocr(processed_image)
                if easyocr_text and not easyocr_text.startswith("Error extracting"):
                    st.text_area("EasyOCR Text:", easyocr_text, height=150, key="easy")
                else:
                    st.error("EasyOCR failed")
                
                st.markdown("### 🔤 Tesseract Results")
                tesseract_text = extract_text_tesseract(processed_image, language_options[selected_lang])
                if tesseract_text and not tesseract_text.startswith("Error extracting"):
                    st.text_area("Tesseract Text:", tesseract_text, height=150, key="tess")
                else:
                    st.error("Tesseract failed")
                
                # Download buttons for both
                col1, col2 = st.columns(2)
                if easyocr_text and not easyocr_text.startswith("Error extracting"):
                    with col1:
                        st.download_button("📄 Download EasyOCR", easyocr_text, "easyocr_text.txt")
                if tesseract_text and not tesseract_text.startswith("Error extracting"):
                    with col2:
                        st.download_button("📄 Download Tesseract", tesseract_text, "tesseract_text.txt")
                return
            
            # Show single result
            if text and not text.startswith("Error extracting"):
                st.text_area(
                    "Extracted Text:",
                    text,
                    height=200,
                    help="Copy this text or download it as a file"
                )
                
                st.download_button(
                    "📄 Download as Text File",
                    data=text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )
            else:
                st.info("💡 Try adjusting the settings in the sidebar for better results")
    
    else:
        # Show helpful message when no image is uploaded
        st.info("👆 Upload an image to get started")
        
        # Show maintenance notice prominently if Tesseract is down
        if TESSERACT_MAINTENANCE and t_model == "Tesseract (maintenance)":
            st.warning("🚧 **Notice:** Tesseract OCR is currently under maintenance. Please use EasyOCR for text extraction.")
        
        # Simple examples section
        with st.expander("📋 What images work best?"):
            st.markdown("""
            **Good images for text extraction:**
            - Screenshots of documents or websites
            - Photos of printed text (books, signs, papers)
            - Clear, well-lit images
            - High contrast between text and background
            
            **Supported formats:** PNG, JPG, JPEG, TIFF, BMP
            """)

if __name__ == "__main__":
    main()