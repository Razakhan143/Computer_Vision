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

# Configure page
st.set_page_config(
    page_title="Image to Text Converter",
    page_icon="📝",
    layout="wide"
)

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
    
    # Sidebar for options
    st.sidebar.header("⚙️ OCR Settings")
    
    # Engine selection
    if EASYOCR_AVAILABLE:
        ocr_engine = st.sidebar.selectbox(
            "Choose OCR Engine:",
            ["EasyOCR", "Tesseract", "Both"],
            help="EasyOCR: Better for complex images | Tesseract: Faster processing"
            
        )
    else:
        ocr_engine = "Tesseract"
        st.sidebar.info("💡 Only Tesseract is available")
        st.sidebar.markdown("To enable EasyOCR, install Visual C++ Redistributable")
    # Language selection (for Tesseract)
    if ocr_engine in ["Tesseract", "Both"]:
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


    st.sidebar.markdown(
    "<p style='font-size: 12px;'>EasyOCR takes more time but handles complex images better. Tesseract is faster for simpler text but well-structured.</p>",
    unsafe_allow_html=True
)
    # Image enhancement options
    st.sidebar.subheader("🖼️ Image Enhancement")
    enhance_contrast = st.sidebar.checkbox("Enhance Contrast", value=False)
    resize_factor = st.sidebar.slider("Resize Factor", 0.5, 2.0, 1.0, 0.1)
    st.sidebar.markdown(
    """
    <div style='text-align: center; padding-top: 15px;'>
        <hr style='border: 0.5px solid #ccc;'/>
        <p style='font-size: 20px; font-weight: 500; color: #ccc;'>Developed by <strong>Raza Khan</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)

    # Simple file uploader
    uploaded_file = st.file_uploader(
        "Drop your image here or click to browse",
        type=['png', 'jpg', 'jpeg', 'tiff', 'bmp']
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Image", width=400)
        
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
                    st.error("❌ EasyOCR failed, try Tesseract")
                    text = None
                    
            elif ocr_engine == "Tesseract":
                text = extract_text_tesseract(processed_image, 'eng')
                if text and not text.startswith("Error extracting"):
                    st.success("✅ Tesseract extraction completed!")
                else:
                    print(text)
                    st.error("❌ Could not extract text")
                    text = None
                    
            elif ocr_engine == "Both" and EASYOCR_AVAILABLE:
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