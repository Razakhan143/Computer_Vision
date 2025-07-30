import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av

# Page configuration
st.set_page_config(
    page_title="AI Color Detection Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .color-preview {
        width: 100%;
        height: 100px;
        border-radius: 10px;
        border: 3px solid #fff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 0.5rem 0;
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .metric-card p {
        margin: 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .detection-info {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f8f9ff;
        border-radius: 10px;
    }
    
    .detection-status {
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .status-active {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    
    .status-inactive {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def get_limits(color):
    """
    Calculate HSV limits for color detection with improved red hue handling
    """
    # Convert BGR to RGB for proper color conversion
    color_rgb = [color[2], color[1], color[0]]  # BGR to RGB
    c = np.uint8([[color_rgb]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_RGB2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around with improved ranges
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 50, 50], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 50, 50], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 50, 50], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

class VideoProcessor:
    def __init__(self, target_color):
        self.target_color = target_color
        self.detection_count = 0
        self.frame_count = 0
    
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Flip frame horizontally for mirror effect
        img = cv2.flip(img, 1)
        
        # Convert to HSV
        hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Get color limits
        lowerLimit, upperLimit = get_limits(color=self.target_color)
        
        # Create mask
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        
        # Find contours for better detection
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detection_found = False
        
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Only process if area is significant
            if area > 500:
                detection_found = True
                self.detection_count += 1
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Draw enhanced bounding box
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                
                # Add detection label
                label = f"Color Detected! Area: {int(area)}"
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
                
                # Draw contour
                cv2.drawContours(img, [largest_contour], -1, (255, 255, 0), 2)
        
        self.frame_count += 1
        
        # Add frame info
        info_text = f"Frame: {self.frame_count} | Detections: {self.detection_count}"
        cv2.putText(img, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 2)
        
        # Add color info
        color_text = f"Target: RGB({self.target_color[2]}, {self.target_color[1]}, {self.target_color[0]})"
        cv2.putText(img, color_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 AI Color Detection Studio</h1>
        <p>Advanced Real-time Color Detection & Tracking System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### 🔧 Detection Configuration")
        
        # Camera selection
        st.markdown("#### 📹 Camera Settings")
        camera_id = st.selectbox(
            "Select Camera Device",
            options=[0, 1, 2, 3],
            index=0,
            help="Choose your camera device (0 is usually the default camera)"
        )
        
        st.markdown("#### 🎨 Color Selection")
        
        # Color input methods
        color_method = st.radio(
            "Choose color input method:",
            ["RGB Sliders", "Color Picker", "Preset Colors"]
        )
        
        if color_method == "RGB Sliders":
            st.markdown("**RGB Values (0-255)**")
            r = st.slider("Red", 0, 255, 255, key="red_slider")
            g = st.slider("Green", 0, 255, 0, key="green_slider")
            b = st.slider("Blue", 0, 255, 0, key="blue_slider")
            target_color = [b, g, r]  # BGR format for OpenCV
            
        elif color_method == "Color Picker":
            color_hex = st.color_picker("Pick a color", "#FF0000")
            # Convert hex to RGB
            r = int(color_hex[1:3], 16)
            g = int(color_hex[3:5], 16)
            b = int(color_hex[5:7], 16)
            target_color = [b, g, r]  # BGR format for OpenCV
            
        else:  # Preset Colors
            preset_colors = {
                "Red": [0, 0, 255],
                "Green": [0, 255, 0],
                "Blue": [255, 0, 0],
                "Yellow": [0, 255, 255],
                "Orange": [0, 165, 255],
                "Purple": [128, 0, 128],
                "Pink": [203, 192, 255],
                "Cyan": [255, 255, 0]
            }
            
            selected_preset = st.selectbox(
                "Select preset color:",
                list(preset_colors.keys())
            )
            target_color = preset_colors[selected_preset]
            r, g, b = target_color[2], target_color[1], target_color[0]
        
        # Color preview
        st.markdown("#### 🎯 Target Color Preview")
        color_preview = f"""
        <div class="color-preview" style="background-color: rgb({r}, {g}, {b});"></div>
        """
        st.markdown(color_preview, unsafe_allow_html=True)
        
        # Color information
        st.markdown(f"""
        <div class="detection-info">
            <h4 style="margin-top: 0;">Color Information</h4>
            <p><strong>RGB:</strong> ({r}, {g}, {b})</p>
            <p><strong>Hex:</strong> #{r:02x}{g:02x}{b:02x}</p>
            <p><strong>BGR (OpenCV):</strong> ({target_color[0]}, {target_color[1]}, {target_color[2]})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detection settings
        st.markdown("#### ⚙️ Detection Settings")
        sensitivity = st.selectbox(
            "Detection Sensitivity",
            ["Low", "Medium", "High"],
            index=1,
            help="Higher sensitivity detects more variations of the target color"
        )
        
        show_mask = st.checkbox("Show Detection Mask", False)
        
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📸 Live Camera Feed")
        
        # WebRTC configuration
        rtc_configuration = RTCConfiguration({
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        })
        
        # Initialize session state for video processor
        if 'video_processor' not in st.session_state:
            st.session_state.video_processor = VideoProcessor(target_color)
        else:
            # Update target color
            st.session_state.video_processor.target_color = target_color
        
        # Start video stream
        webrtc_ctx = webrtc_streamer(
            key="color-detection",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=rtc_configuration,
            video_processor_factory=lambda: VideoProcessor(target_color),
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        
        # Detection status
        if webrtc_ctx.state.playing:
            status_class = "status-active"
            status_text = "🟢 Detection Active"
        else:
            status_class = "status-inactive"
            status_text = "🔴 Detection Inactive"
        
        st.markdown(f"""
        <div class="detection-status {status_class}">
            {status_text}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Detection Statistics")
        
        if 'video_processor' in st.session_state:
            processor = st.session_state.video_processor
            
            # Detection metrics
            if processor.frame_count > 0:
                detection_rate = (processor.detection_count / processor.frame_count) * 100
            else:
                detection_rate = 0
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{processor.detection_count}</h3>
                <p>Total Detections</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{processor.frame_count}</h3>
                <p>Frames Processed</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{detection_rate:.1f}%</h3>
                <p>Detection Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Instructions
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. **Select Camera**: Choose your camera device from the sidebar
        2. **Pick Color**: Use sliders, color picker, or presets to select target color
        3. **Start Detection**: The system will automatically detect the selected color
        4. **View Results**: See real-time detection with bounding boxes and statistics
        """)
        
        # Tips
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        - **Good Lighting**: Ensure adequate lighting for better detection
        - **Solid Colors**: Use objects with solid, uniform colors
        - **Stable Background**: Avoid busy backgrounds for accurate detection
        - **Distance**: Keep objects at moderate distance from camera
        """)
        
        # Reset button
        if st.button("🔄 Reset Statistics"):
            if 'video_processor' in st.session_state:
                st.session_state.video_processor.detection_count = 0
                st.session_state.video_processor.frame_count = 0
                st.success("Statistics reset successfully!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Built with Streamlit & OpenCV | Advanced Computer Vision Technology</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()