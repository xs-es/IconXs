import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import sys
import math
from main import resize_image
import re
from datetime import datetime
import time

class ImageResizerApp:
    # Class-level cache for images
    _image_cache = {}

    def __init__(self, root):
        self.root = root
        self.root.title("Image Dimension Converter")
        
        # Initially set a larger size to fit everything
        self.root.geometry("1200x800")
        self.root.minsize(1100, 750)
        
        # Allow resizing but we'll make it unnecessary on startup
        self.root.resizable(True, True)
        
        self.selected_image_path = None
        self.output_folder = "resized_images"
        self.sizes = [16, 24, 32, 48, 64, 128, 256, 512]
        
        # Set enhanced futuristic theme colors
        self.bg_color = "#121212"  # Darker background
        self.panel_bg = "#1E1E1E"  # Panel background
        self.accent_color = "#007BFF"  # Brighter blue accent
        self.accent_secondary = "#00B8D4"  # Cyan accent for highlights
        self.text_color = "#FFFFFF"  # Brighter white text
        self.highlight_color = "#333333"  # Darker highlights/borders
        self.button_hover = "#0069D9"  # Darker blue when hovering
        self.preview_bg = "#161616"  # Darker grey for preview
        self.success_color = "#00C853"  # Brighter green for success
        self.warning_color = "#FF9100"  # Orange for warnings
        self.error_color = "#FF1744"  # Red for errors
        
        # Configure the root window background
        self.root.configure(background=self.bg_color)
        
        # Add a touch of animation
        self.animation_frame = 0
        
        # Set up custom styles for futuristic metal theme
        self.setup_styles()
        self.setup_ui()
        
        # Adjust window size after UI is created to fit content exactly
        self.root.update_idletasks()  # Update geometry information
        self.update_window_size()
        
        # Start animations
        self.animate_elements()

    def animate_elements(self):
        """Add subtle animations with optimized performance"""
        # Limit frame rate for better performance
        animation_interval = 50  # ms between frames
        
        self.animation_frame = (self.animation_frame + 1) % 100
        pulse_factor = 0.5 + math.sin(self.animation_frame / 15) * 0.05
        
        # Cache widget references to improve performance
        if not hasattr(self, '_cached_widgets'):
            self._cached_widgets = {}
            
            # Find and cache the footer text widget
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Label) and "Ready" in str(widget):
                    self._cached_widgets['footer'] = widget
                    break
        
        # Animate only if the cached widget exists
        if 'footer' in self._cached_widgets:
            r = int(min(160, max(100, 130 + pulse_factor * 30)))
            g = int(min(160, max(100, 130 + pulse_factor * 30)))
            b = int(min(190, max(130, 160 + pulse_factor * 30)))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self._cached_widgets['footer'].configure(foreground=color)
        
        # Schedule the next animation frame
        self.root.after(animation_interval, self.animate_elements)

    def setup_styles(self):
        """Setup custom ttk styles for a futuristic metal look with enhanced visual effects"""
        style = ttk.Style()
        
        # Configure main styles with improved metal theme
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color)
        
        # Panel frames with subtle gradient-like effect
        style.configure("Panel.TFrame", background=self.panel_bg)
        
        # Enhanced Label frames with metallic borders and better styling
        style.configure("TLabelframe", 
                       background=self.panel_bg, 
                       borderwidth=1, 
                       relief="solid")
        style.configure("TLabelframe.Label", 
                       background=self.panel_bg, 
                       foreground=self.accent_color,  # Use accent color for better visibility
                       font=("Arial", 10, "bold"))
        
        # Stylish button styles with metallic look
        style.configure("TButton", 
                       background=self.accent_color, 
                       foreground="white",
                       font=("Arial", 9, "bold"))
        
        # Fix button styling issues with improved hover effects
        style.map("TButton",
                 background=[("active", self.button_hover)],
                 foreground=[("active", "white")])
        
        # Advanced entry fields with better visibility and focus effects
        style.configure("TEntry", 
                       fieldbackground="#111111", 
                       foreground="#FFFFFF",
                       insertcolor="#00AAFF",  # Brighter cursor color
                       borderwidth=1)
        
        # Improved Checkbutton style 
        style.configure("TCheckbutton", 
                      background=self.panel_bg,
                      foreground="#FFFFFF")  # White text for checkboxes
        
        style.map("TCheckbutton",
                background=[("active", self.panel_bg)],
                foreground=[("active", "#00AAFF")])  # Brighter accent on hover
        
        # Enhanced Scrollbar style for better visibility
        style.configure("TScrollbar", 
                      background=self.panel_bg,
                      troughcolor="#151515",  # Darker trough
                      bordercolor=self.highlight_color,
                      arrowcolor=self.accent_color)  # Use accent color for arrows
        
        # Add a new style for highlighted titles
        style.configure("Title.TLabel", 
                       font=("Arial", 12, "bold"),
                       foreground=self.accent_color,
                       background=self.panel_bg)
        
        # Style for section headers
        style.configure("SectionHeader.TLabel", 
                       font=("Arial", 10, "bold"),
                       foreground="#00AAFF",
                       background=self.panel_bg)
        
        # Style for preview panel
        style.configure("Preview.TFrame", background=self.preview_bg)
    
    def setup_ui(self):
        # Use a grid layout with compact spacing
        self.root.grid_columnconfigure(0, weight=2)  # Left panel gets 2/5 of width
        self.root.grid_columnconfigure(1, weight=3)  # Right panel gets 3/5 of width
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header with sleek gradient
        header_frame = ttk.Frame(self.root, style="Panel.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx=10, pady=(5, 2))
        
        # Create a canvas for gradient background
        header_canvas = tk.Canvas(header_frame, highlightthickness=0, background=self.panel_bg, height=60)
        header_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add gradient to canvas
        def create_gradient(canvas, color1, color2, width, height):
            for i in range(height):
                # Calculate color for this line
                r1, g1, b1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
                r2, g2, b2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
                
                r = int(r1 + (r2-r1) * i/height)
                g = int(g1 + (g2-g1) * i/height)
                b = int(b1 + (b2-b1) * i/height)
                
                color = f'#{r:02x}{g:02x}{b:02x}'
                canvas.create_line(0, i, width, i, fill=color)
        
        # Schedule gradient creation after canvas is visible
        self.root.after(50, lambda: create_gradient(header_canvas, "1e1e1e", "151515", header_canvas.winfo_width(), 60))
        
        # Add modern title with glow effect
        title_text = "IMAGE DIMENSION CONVERTER"
        title_x = 75  # Position for text
        title_y = 30
        
        # Add subtle glow effect behind text
        header_canvas.create_text(title_x+1, title_y+1, text=title_text, font=("Segoe UI", 22, "bold"), 
                               fill="#004080", anchor=tk.W)
        # Main text
        header_canvas.create_text(title_x, title_y, text=title_text, font=("Segoe UI", 22, "bold"), 
                                fill=self.accent_color, anchor=tk.W)
        
        # App icon with tech symbol
        header_canvas.create_text(40, 30, text="⚙️", font=("Segoe UI", 24), fill=self.accent_color)
        
        # Version tag
        header_canvas.create_text(header_canvas.winfo_width()-20, 15, text="v2.0", 
                               font=("Segoe UI", 10), fill="#666666", anchor=tk.E)
        
        # Instructions with modern tech font in a centered container
        instructions_frame = ttk.Frame(header_frame, style="Panel.TFrame")
        instructions_frame.pack(fill=tk.X, padx=20, pady=(5, 10))
        
        instructions = ttk.Label(
            instructions_frame,
            text="Transform images to multiple dimensions with precision",
            font=("Arial", 11),
            background=self.panel_bg,
            foreground=self.text_color
        )
        instructions.pack(pady=5)
        
        # Left panel - Control console (row 1, column 0)
        left_frame = ttk.Frame(self.root, style="Panel.TFrame")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(5, 10))
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Create a frame for controls - no scrolling needed
        controls_frame = ttk.Frame(left_frame, style="Panel.TFrame")
        controls_frame.pack(fill=tk.BOTH, expand=True)
        controls_frame.grid_columnconfigure(0, weight=1)
        
        # Create a frame for the two-column layout in the left panel
        compact_controls = ttk.Frame(controls_frame, style="Panel.TFrame")
        compact_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        compact_controls.grid_columnconfigure(0, weight=1)
        compact_controls.grid_columnconfigure(1, weight=1)
        
        # First column - Image Source & Output
        left_column = ttk.Frame(compact_controls, style="Panel.TFrame")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_column.grid_columnconfigure(0, weight=1)
        
        # Second column - Dimensions & Formats
        right_column = ttk.Frame(compact_controls, style="Panel.TFrame")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_column.grid_columnconfigure(0, weight=1)
        
        # Image selection console
        select_frame = ttk.LabelFrame(left_column, text="IMAGE SOURCE", padding="10")
        select_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        select_frame.grid_columnconfigure(0, weight=1)
        
        # Image path - use tk.Entry directly instead of ttk for more reliable styling
        self.path_var = tk.StringVar()
        self.path_var.set("No image selected")
        path_entry = tk.Entry(
            select_frame, 
            textvariable=self.path_var,
            bg="#111111",
            fg="white",
            insertbackground="white",
            relief=tk.SUNKEN,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground="#444444"
        )
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        
        # Browse button with improved styling
        browse_btn = tk.Button(
            select_frame, 
            text="SELECT IMAGE",
            command=self.browse_image,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )
        self.beautify_button(browse_btn, "#444444", "#555555", "#333333")
        browse_btn.grid(row=0, column=1, pady=5)
        
        # Output configuration console
        output_frame = ttk.LabelFrame(left_column, text="OUTPUT DESTINATION", padding="10")
        output_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Output folder display
        ttk.Label(output_frame, text="Target Directory:", background=self.panel_bg).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        output_entry_frame = ttk.Frame(output_frame, style="Panel.TFrame")
        output_entry_frame.grid(row=1, column=0, sticky="ew")
        output_entry_frame.grid_columnconfigure(0, weight=1)
        
        # Output folder - use tk.Entry directly instead of ttk
        self.output_var = tk.StringVar()
        self.output_var.set(self.output_folder)
        output_entry = tk.Entry(
            output_entry_frame, 
            textvariable=self.output_var,
            bg="#111111",
            fg="white",
            insertbackground="white",
            relief=tk.SUNKEN,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground="#444444"
        )
        output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        
        # Output browse button with enhanced styling
        output_browse_btn = tk.Button(
            output_entry_frame, 
            text="BROWSE", 
            command=self.browse_output_folder,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )
        self.beautify_button(output_browse_btn, "#444444", "#555555", "#333333")
        output_browse_btn.grid(row=0, column=1, pady=5)
        
        # Dimension configuration console
        sizes_frame = ttk.LabelFrame(right_column, text="DIMENSION PROFILES", padding="10")
        sizes_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        sizes_frame.grid_columnconfigure(0, weight=1)
        
        # Information about dimensions with tech styling
        size_info = ttk.Label(
            sizes_frame,
            text="Select target dimensions to generate:",
            wraplength=350,
            background=self.panel_bg
        )
        size_info.pack(anchor=tk.W, pady=(0, 10))
        
        # Quick selection controls with improved styling
        select_buttons_frame = ttk.Frame(sizes_frame, style="Panel.TFrame")
        select_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        select_all_btn = tk.Button(
            select_buttons_frame,
            text="SELECT ALL",
            command=self.select_all_sizes,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )
        self.beautify_button(select_all_btn, "#444444", "#555555", "#333333")
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        deselect_all_btn = tk.Button(
            select_buttons_frame,
            text="DESELECT ALL",
            command=self.deselect_all_sizes,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )
        self.beautify_button(deselect_all_btn, "#444444", "#555555", "#333333")
        deselect_all_btn.pack(side=tk.LEFT)
        
        # Dimension selection with a 4-column grid for compactness
        sizes_grid_frame = ttk.Frame(sizes_frame, style="Panel.TFrame")
        sizes_grid_frame.pack(fill=tk.X)
        
        self.size_vars = {}
        for i, size in enumerate(self.sizes):
            var = tk.BooleanVar(value=True)
            self.size_vars[size] = var
            
            # Calculate row and column (4 columns)
            row = i // 4
            col = i % 4
            
            checkbox_frame = ttk.Frame(sizes_grid_frame, style="Panel.TFrame")
            checkbox_frame.grid(row=row, column=col, sticky="w", padx=5, pady=3)
            
            # Use tk.Checkbutton with more compact styling
            cb = tk.Checkbutton(
                checkbox_frame, 
                text=f"{size}x{size}",
                variable=var,
                bg=self.panel_bg,
                fg="white",
                selectcolor="#222222",  # Darker color for the check
                activebackground=self.panel_bg,
                activeforeground=self.accent_secondary,
                font=("Segoe UI", 9)
            )
            cb.pack(side=tk.LEFT)
        
        # Naming options console
        naming_frame = ttk.LabelFrame(left_column, text="NAMING OPTIONS", padding="10")
        naming_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        naming_frame.grid_columnconfigure(0, weight=1)
        
        # Custom naming checkbox with better styling
        self.custom_naming_var = tk.BooleanVar(value=False)
        custom_naming_frame = ttk.Frame(naming_frame, style="Panel.TFrame")
        custom_naming_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        custom_naming_cb = tk.Checkbutton(
            custom_naming_frame,
            text="Enable custom file naming",
            variable=self.custom_naming_var,
            bg=self.panel_bg,
            fg="#00AAFF",  # Bright blue text for emphasis
            selectcolor="#333333",
            activebackground=self.panel_bg,
            activeforeground="#00CCFF",
            font=("Arial", 10, "bold"),
            command=self.toggle_naming_options
        )
        custom_naming_cb.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add a small info icon and tooltip effect
        info_label = ttk.Label(
            custom_naming_frame,
            text="ⓘ",  # Info symbol
            foreground="#00AAFF",
            background=self.panel_bg,
            font=("Arial", 10, "bold")
        )
        info_label.pack(side=tk.LEFT)
        
        # Tooltip effect on hover
        def show_tooltip(event):
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
            tip_frame = ttk.Frame(tooltip, style="Panel.TFrame", padding=5)
            tip_frame.pack(fill=tk.BOTH, expand=True)
            ttk.Label(
                tip_frame, 
                text="Customize how your files are named\nwith sequential numbering",
                background=self.panel_bg,
                foreground="white",
                font=("Arial", 9),
                justify=tk.LEFT
            ).pack()
            
            # Store reference and schedule destruction
            info_label.tooltip = tooltip
            self.root.after(3000, tooltip.destroy)
            
        def hide_tooltip(event):
            if hasattr(info_label, "tooltip"):
                info_label.tooltip.destroy()
                
        info_label.bind("<Enter>", show_tooltip)
        info_label.bind("<Leave>", hide_tooltip)
        
        # Pattern input container with enhanced styling
        pattern_frame = ttk.Frame(naming_frame, style="Panel.TFrame")
        pattern_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        pattern_frame.grid_columnconfigure(1, weight=1)
        
        # Pattern label with icon
        pattern_label_frame = ttk.Frame(pattern_frame, style="Panel.TFrame")
        pattern_label_frame.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        ttk.Label(
            pattern_label_frame, 
            text="📝", 
            background=self.panel_bg
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(
            pattern_label_frame, 
            text="Pattern:", 
            background=self.panel_bg,
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT)
        
        # Pattern entry with placeholders and enhanced styling
        self.pattern_var = tk.StringVar(value="{name}_{num}")
        pattern_entry = tk.Entry(
            pattern_frame,
            textvariable=self.pattern_var,
            bg="#111111",
            fg="#00CCFF",  # Bright blue text
            insertbackground="white",
            relief=tk.SUNKEN,
            highlightthickness=2,  # Thicker highlight for better effect
            highlightcolor=self.accent_color,
            highlightbackground="#444444",
            font=("Consolas", 10),  # Monospace font for code-like appearance
            state=tk.DISABLED
        )
        pattern_entry.grid(row=0, column=1, sticky="ew")
        
        # Pattern help with better styling
        pattern_help_frame = ttk.Frame(naming_frame, style="Panel.TFrame", padding=(15, 0, 0, 0))
        pattern_help_frame.grid(row=2, column=0, sticky="w", pady=(0, 10))
        
        pattern_help = ttk.Label(
            pattern_help_frame,
            text="• {name} = original filename\n• {num} = sequential number",
            font=("Arial", 8),
            foreground="#BBBBBB",
            background=self.panel_bg,
            justify=tk.LEFT
        )
        pattern_help.pack(anchor=tk.W)
        
        # Starting number container with better styling
        number_frame = ttk.Frame(naming_frame, style="Panel.TFrame")
        number_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        number_frame.grid_columnconfigure(1, weight=1)
        
        # Starting number label with icon
        number_label_frame = ttk.Frame(number_frame, style="Panel.TFrame")
        number_label_frame.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        ttk.Label(
            number_label_frame, 
            text="🔢", 
            background=self.panel_bg
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(
            number_label_frame, 
            text="Start from:", 
            background=self.panel_bg,
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT)
        
        # Starting number spinbox with enhanced styling
        self.start_number_var = tk.IntVar(value=1)
        start_number_spinbox = tk.Spinbox(
            number_frame,
            from_=1,
            to=1000,
            textvariable=self.start_number_var,
            bg="#111111",
            fg="#00CCFF",  # Bright blue text
            buttonbackground="#333333",
            relief=tk.SUNKEN,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground="#444444",
            width=5,
            font=("Consolas", 10),  # Monospace font
            state=tk.DISABLED
        )
        start_number_spinbox.grid(row=0, column=1, sticky="w", padx=(0, 10))
        
        # Include dimensions checkbox with enhanced styling
        dimensions_frame = ttk.Frame(naming_frame, style="Panel.TFrame", padding=(15, 0, 0, 0))
        dimensions_frame.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.include_dimensions_var = tk.BooleanVar(value=True)
        include_dimensions_cb = tk.Checkbutton(
            dimensions_frame,
            text="Include dimensions in filename",
            variable=self.include_dimensions_var,
            bg=self.panel_bg,
            fg="white",
            selectcolor="#333333",
            activebackground=self.panel_bg,
            activeforeground=self.accent_color,
            font=("Arial", 9),
            state=tk.DISABLED
        )
        include_dimensions_cb.pack(anchor=tk.W)
        
        # Preview sample name
        preview_frame = ttk.Frame(naming_frame, style="Panel.TFrame", padding=(0, 5, 0, 5))
        preview_frame.grid(row=5, column=0, sticky="ew", pady=(5, 0))
        preview_frame.grid_columnconfigure(0, weight=1)
        
        preview_label_frame = ttk.Frame(preview_frame, style="Panel.TFrame")
        preview_label_frame.grid(row=0, column=0, sticky="w")
        
        ttk.Label(
            preview_label_frame,
            text="Preview: ",
            background=self.panel_bg,
            foreground="#BBBBBB",
            font=("Arial", 9)
        ).pack(side=tk.LEFT)
        
        self.naming_preview_label = ttk.Label(
            preview_label_frame,
            text="sample_1_64x64.png",
            background=self.panel_bg,
            foreground="#00CCFF",
            font=("Consolas", 10)
        )
        self.naming_preview_label.pack(side=tk.LEFT)
        
        # Test pattern button with enhanced look
        test_pattern_btn = tk.Button(
            preview_frame,
            text="TEST",
            command=self.test_naming_pattern,
            font=("Arial", 8, "bold"),
            cursor="hand2"
        )
        self.beautify_button(test_pattern_btn, "#444444", "#555555", "#333333")
        test_pattern_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Store reference to the test button
        self.test_pattern_btn = test_pattern_btn
        self.test_pattern_btn.config(state=tk.DISABLED)
        
        # Add trace to pattern_var to update preview
        self.pattern_var.trace_add("write", self.update_naming_preview)
        self.start_number_var.trace_add("write", self.update_naming_preview)
        self.include_dimensions_var.trace_add("write", self.update_naming_preview)
        
        # Store references for enabling/disabling
        self.pattern_entry = pattern_entry
        self.start_number_spinbox = start_number_spinbox
        self.include_dimensions_cb = include_dimensions_cb
        
        # Format selection console
        format_frame = ttk.LabelFrame(right_column, text="OUTPUT FORMAT", padding="10")
        format_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        format_frame.grid_columnconfigure(0, weight=1)
        
        # Format selection header
        format_header_frame = ttk.Frame(format_frame, style="Panel.TFrame")
        format_header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(
            format_header_frame,
            text="Save images as:",
            background=self.panel_bg,
            font=("Arial", 9)
        ).pack(anchor=tk.W)
        
        # Format radio buttons container
        format_options_frame = ttk.Frame(format_frame, style="Panel.TFrame")
        format_options_frame.grid(row=1, column=0, sticky="ew")
        format_options_frame.grid_columnconfigure(0, weight=1)
        format_options_frame.grid_columnconfigure(1, weight=1)
        
        # Available formats with descriptions
        self.formats = [
            {"value": None, "text": "Original Format", "desc": "Keep original file format"},
            {"value": "PNG", "text": "PNG", "desc": "Best for transparency"},
            {"value": "JPEG", "text": "JPG", "desc": "Smaller file size"},
            {"value": "GIF", "text": "GIF", "desc": "Limited colors"},
            {"value": "ICO", "text": "ICO", "desc": "Windows icons"},
            {"value": "WEBP", "text": "WEBP", "desc": "Web optimized"}
        ]
        
        # Format radio button variable
        self.format_var = tk.StringVar(value="ORIGINAL")
        
        # Create radio buttons for formats in a two-column grid
        for i, format_info in enumerate(self.formats):
            row = i // 2
            col = i % 2
            
            format_option_frame = ttk.Frame(format_options_frame, style="Panel.TFrame")
            format_option_frame.grid(row=row, column=col, sticky="w", padx=5, pady=3)
            
            # Set value for the radio button - convert None to "ORIGINAL" for UI
            rb_value = "ORIGINAL" if format_info["value"] is None else format_info["value"]
            
            rb = tk.Radiobutton(
                format_option_frame,
                text=format_info["text"],
                variable=self.format_var,
                value=rb_value,
                bg=self.panel_bg,
                fg="#00CCFF",
                selectcolor="#333333",
                activebackground=self.panel_bg,
                activeforeground=self.accent_color,
                font=("Arial", 9, "bold")
            )
            rb.pack(side=tk.LEFT, padx=(0, 5))
            
            # Format description
            ttk.Label(
                format_option_frame, 
                text=f"({format_info['desc']})",
                font=("Arial", 8),
                foreground="#AAAAAA",
                background=self.panel_bg
            ).pack(side=tk.LEFT)
        
        # Right panel - Preview console (row 1, column 1)
        right_frame = ttk.Frame(self.root, style="Panel.TFrame")
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(5, 10))
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)
        
        # Preview console with tech border
        preview_frame = ttk.LabelFrame(right_frame, text="IMAGE PREVIEW", padding="15")
        preview_frame.grid(row=0, column=0, sticky="nsew")
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        # Container for preview with tech-themed background
        self.preview_container = ttk.Frame(preview_frame, style="Preview.TFrame")
        self.preview_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create a special style for the preview container
        style = ttk.Style()
        style.configure("Preview.TFrame", background=self.preview_bg)
        
        # Preview message with tech font
        self.preview_msg = ttk.Label(
            self.preview_container,
            text="Select image file to preview\nand process dimensions",
            font=("Arial", 12),
            foreground=self.text_color,
            background=self.preview_bg,
            justify=tk.CENTER
        )
        self.preview_msg.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Preview image on dark background
        self.preview_label = ttk.Label(self.preview_container, background=self.preview_bg)
        self.preview_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.preview_label.lower()  # Initially keep it behind the message
        
        # Command console - prominent convert button
        command_frame = ttk.Frame(self.root, padding="10 15 10 15", style="Panel.TFrame")
        command_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        command_frame.grid_columnconfigure(0, weight=1)
        
        # Create a beautifully styled convert button
        convert_btn = tk.Button(
            command_frame,
            text="CONVERT DIMENSIONS",
            command=self.process_image,
            font=("Arial", 14, "bold"),
            cursor="hand2"
        )
        self.beautify_button(convert_btn, self.success_color, "#00C060", "#009348")
        convert_btn.grid(row=0, column=0, pady=5, padx=20, sticky="ew")
        
        # System status footer
        footer_frame = ttk.Frame(self.root, style="Panel.TFrame")
        footer_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator - pulsing dot
        self.status_indicator = tk.Canvas(footer_frame, width=8, height=8, bg=self.bg_color, highlightthickness=0)
        self.status_indicator.grid(row=0, column=0, padx=(20, 5))
        self.status_indicator.create_oval(0, 0, 8, 8, fill="#00B050", outline="")
        
        # System status text
        self.status_text = ttk.Label(
            footer_frame,
            text="Dimension Converter v1.0 | System Ready", 
            font=("Arial", 8),
            foreground="#888888",
            background=self.bg_color
        )
        self.status_text.grid(row=0, column=1, sticky="w")
        
        # Right-aligned build info
        build_info = ttk.Label(
            footer_frame,
            text="build 1.0.228", 
            font=("Arial", 7),
            foreground="#666666",
            background=self.bg_color
        )
        build_info.grid(row=0, column=2, sticky="e", padx=20)
        
        # Add subtle shadow effect to panels
        def add_shadow_effect(panel):
            try:
                # Create a shadow canvas behind the panel
                shadow = tk.Canvas(
                    panel.master, 
                    highlightthickness=0, 
                    bg="#151515"  # Dark shadow color
                )
                
                # Get the panel's position and size
                x = panel.winfo_x()
                y = panel.winfo_y()
                width = panel.winfo_width()
                height = panel.winfo_height()
                
                # Position shadow slightly offset
                shadow.place(x=x+5, y=y+5, width=width, height=height)
                
                # Make sure shadow is behind the panel
                panel.lift()
                
                return shadow
            except Exception as e:
                print(f"Shadow effect error: {e}")
                return None
        
        # Schedule shadow creation after panels are fully rendered
        self.root.after(200, lambda: add_shadow_effect(self.preview_container))
        
        # Add a subtle separator between the controls and preview
        separator = ttk.Separator(self.root, orient="vertical")
        separator.grid(row=1, column=0, sticky="nes", padx=(0, 2), pady=10)
    
    def select_all_sizes(self):
        """Select all size options"""
        for var in self.size_vars.values():
            var.set(True)
    
    def deselect_all_sizes(self):
        """Deselect all size options"""
        for var in self.size_vars.values():
            var.set(False)
    
    def browse_image(self):
        filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.path_var.set(file_path)
            self.update_preview()
            
            # Manage cache size
            self.manage_image_cache()
    
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(
            title="Select Output Folder"
        )
        
        if folder_path:
            self.output_folder = folder_path
            self.output_var.set(folder_path)
    
    def update_preview(self):
        if not self.selected_image_path:
            return
        
        try:
            # Check if image is already in cache
            cache_key = self.selected_image_path
            
            if cache_key in self.__class__._image_cache:
                # Use cached photo
                photo = self.__class__._image_cache[cache_key]
                
                # Update label
                self.preview_label.config(image=photo)
                self.preview_label.image = photo  # Keep a reference
                
                # Hide the message and raise the image
                self.preview_msg.place_forget()
                self.preview_label.lift()
                
                # Display cached image info
                filename = os.path.basename(self.selected_image_path)
                dimensions = self.__class__._image_cache.get(f"{cache_key}_dimensions", "Unknown dimensions")
                self.update_preview_title(f"IMAGE PREVIEW - ORIGINAL: {dimensions} PIXELS")
                self.status_text.config(text=f"Image loaded: {filename} (cached)")
                return
            
            # Open image and create thumbnail for preview
            img = Image.open(self.selected_image_path)
            
            # Calculate the aspect ratio
            width, height = img.size
            aspect_ratio = width / height
            
            # Store dimensions for caching
            dimensions = f"{width}x{height}"
            self.__class__._image_cache[f"{cache_key}_dimensions"] = dimensions
            
            # Maximum preview size
            max_width = 400  # Larger preview
            max_height = 400
            
            # Determine new dimensions while maintaining aspect ratio
            if aspect_ratio > 1:  # Wider than tall
                new_width = min(width, max_width)
                new_height = int(new_width / aspect_ratio)
            else:  # Taller than wide
                new_height = min(height, max_height)
                new_width = int(new_height * aspect_ratio)
            
            # Resize for preview - use LANCZOS for better quality
            img_preview = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage and cache it
            photo = ImageTk.PhotoImage(img_preview)
            self.__class__._image_cache[cache_key] = photo
            
            # Update label
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # Keep a reference
            
            # Hide the message and raise the image
            self.preview_msg.place_forget()
            self.preview_label.lift()
            
            # Update window title with image name
            filename = os.path.basename(self.selected_image_path)
            self.root.title(f"Image Dimension Converter - {filename}")
            
            # Show image dimensions in the preview frame title
            dimensions = f"IMAGE PREVIEW - ORIGINAL: {width}x{height} PIXELS"
            self.update_preview_title(dimensions)
            
            # Update status
            self.status_text.config(text=f"Image loaded: {filename}")
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error loading preview: {e}")
    
    def update_preview_title(self, new_title):
        """Update the preview frame title dynamically"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and "PREVIEW" in str(child) or "Preview" in str(child):
                        child.configure(text=new_title)
                        return
    
    def toggle_naming_options(self):
        """Enable or disable naming options based on checkbox"""
        if self.custom_naming_var.get():
            # Enable fields
            self.pattern_entry.config(state=tk.NORMAL)
            self.start_number_spinbox.config(state=tk.NORMAL)
            self.include_dimensions_cb.config(state=tk.NORMAL)
            
            # Add glow effect to pattern entry
            self.start_entry_glow(self.pattern_entry)
            
            # Update status
            self.status_text.config(text="Custom naming enabled")
            
            # Enable the test button
            if hasattr(self, "test_pattern_btn"):
                self.test_pattern_btn.config(state=tk.NORMAL)
            
            # Update the preview
            self.update_naming_preview()
        else:
            # Disable fields
            self.pattern_entry.config(state=tk.DISABLED)
            self.start_number_spinbox.config(state=tk.DISABLED)
            self.include_dimensions_cb.config(state=tk.DISABLED)
            
            # Stop glow effect
            self.stop_entry_glow(self.pattern_entry)
            
            # Disable the test button
            if hasattr(self, "test_pattern_btn"):
                self.test_pattern_btn.config(state=tk.DISABLED)
            
            # Update status
            self.status_text.config(text="Custom naming disabled")
    
    def start_entry_glow(self, entry):
        """Add a subtle glowing effect to the entry widget"""
        if not hasattr(self, "_glow_frame"):
            current_color = "#444444"
            next_color = self.accent_color
            
            def pulse_border():
                nonlocal current_color, next_color
                # Pulse between accent color and darker color
                if current_color == self.accent_color:
                    next_color = "#444444"
                else:
                    next_color = self.accent_color
                    
                # Update border color
                entry.config(highlightbackground=current_color)
                current_color = next_color
                
                # Schedule next pulse if still enabled
                if entry['state'] == tk.NORMAL:
                    self._glow_frame = self.root.after(800, pulse_border)
            
            # Start pulsing
            pulse_border()
    
    def stop_entry_glow(self, entry):
        """Stop the glowing effect"""
        if hasattr(self, "_glow_frame"):
            self.root.after_cancel(self._glow_frame)
            delattr(self, "_glow_frame")
        entry.config(highlightbackground="#444444")
    
    def process_image(self):
        if not self.selected_image_path:
            messagebox.showwarning("No Image", "Please select an image first.")
            return
        
        # Get output folder
        output_folder = self.output_var.get()
        
        # Get selected sizes
        selected_sizes = [size for size, var in self.size_vars.items() if var.get()]
        
        if not selected_sizes:
            messagebox.showwarning("No Sizes", "Please select at least one dimension to convert.")
            return
        
        # Get custom naming options
        naming_pattern = None
        start_number = 1
        include_dimensions = True
        
        if self.custom_naming_var.get():
            naming_pattern = self.pattern_var.get()
            start_number = self.start_number_var.get()
            include_dimensions = self.include_dimensions_var.get()
        
        # Get output format
        output_format = self.format_var.get()
        if output_format == "ORIGINAL":
            output_format = None
        
        # Show processing indicator with improved animation
        self.root.config(cursor="wait")
        self.status_text.config(text="Converting dimensions... Please wait")
        
        # Start a pulsing animation on the indicator
        if hasattr(self, "_pulse_animation"):
            self.root.after_cancel(self._pulse_animation)
        
        def pulse_indicator():
            if not hasattr(self, "_pulse_phase"):
                self._pulse_phase = 0
            
            colors = ["#FFA500", "#FFB52E", "#FFC65C", "#FFB52E", "#FFA500"]
            self.status_indicator.itemconfig(1, fill=colors[self._pulse_phase % len(colors)])
            self._pulse_phase += 1
            
            self._pulse_animation = self.root.after(150, pulse_indicator)
            
        pulse_indicator()
        self.root.update()
        
        try:
            # Process the image with naming options and format
            success = resize_image(
                self.selected_image_path, 
                output_folder, 
                selected_sizes,
                naming_pattern,
                start_number,
                include_dimensions,
                output_format
            )
            
            # Stop the pulsing animation
            if hasattr(self, "_pulse_animation"):
                self.root.after_cancel(self._pulse_animation)
                delattr(self, "_pulse_phase")
            
            # Reset cursor
            self.root.config(cursor="")
            
            if success:
                # Show success animation
                def success_animation(count=0):
                    if count < 6:
                        colors = ["#00B050", "#00C060", "#00B050"]
                        self.status_indicator.itemconfig(1, fill=colors[count % 3])
                        self.root.after(100, lambda: success_animation(count + 1))
                    else:
                        self.status_indicator.itemconfig(1, fill="#00B050")
                        
                success_animation()
                
                # Show format info in status text
                format_info = output_format if output_format else "original format"
                self.status_text.config(text=f"Converted {len(selected_sizes)} images to {format_info}")
                
                messagebox.showinfo(
                    "Conversion Complete", 
                    f"Successfully created {len(selected_sizes)} image dimensions in {output_folder}"
                )
            else:
                self.status_text.config(text="Conversion failed")
                self.status_indicator.itemconfig(1, fill="#FF0000")  # Red for error
                
                messagebox.showerror(
                    "Conversion Failed",
                    "An error occurred during dimension conversion."
                )
        except Exception as e:
            # Stop the pulsing animation
            if hasattr(self, "_pulse_animation"):
                self.root.after_cancel(self._pulse_animation)
                delattr(self, "_pulse_phase")
                
            self.root.config(cursor="")
            self.status_text.config(text="Error: Conversion failed")
            self.status_indicator.itemconfig(1, fill="#FF0000")  # Red for error
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_naming_preview(self, *args):
        """Update the naming preview as the user types"""
        if hasattr(self, "naming_preview_label") and self.custom_naming_var.get():
            # Get the current pattern
            pattern = self.pattern_var.get()
            
            # Get a sample filename (use the loaded one or a placeholder)
            if self.selected_image_path:
                original_name = os.path.splitext(os.path.basename(self.selected_image_path))[0]
            else:
                original_name = "sample"
            
            # Replace placeholders
            preview = pattern.replace("{name}", original_name)
            preview = preview.replace("{num}", str(self.start_number_var.get()))
            
            # Add dimensions if selected
            ext = ".png"
            if self.include_dimensions_var.get():
                preview = f"{preview}_64x64{ext}"
            else:
                preview = f"{preview}{ext}"
            
            # Update the preview label
            self.naming_preview_label.config(text=preview)

    def test_naming_pattern(self):
        """Show a dialog with example filenames using current pattern"""
        if not self.custom_naming_var.get():
            return
            
        pattern = self.pattern_var.get()
        start_num = self.start_number_var.get()
        include_dims = self.include_dimensions_var.get()
        
        # Check if pattern is valid
        if not pattern or not re.search(r"\{name\}|\{num\}", pattern):
            messagebox.showerror(
                "Invalid Pattern", 
                "Pattern must include at least one placeholder:\n{name} or {num}"
            )
            return
            
        # Create a test dialog
        test_dialog = tk.Toplevel(self.root)
        test_dialog.title("Naming Pattern Test")
        test_dialog.geometry("500x320")
        test_dialog.configure(background=self.panel_bg)
        test_dialog.grab_set()  # Modal dialog
        
        # Make it look consistent with main window
        test_dialog.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ttk.Frame(test_dialog, style="Panel.TFrame", padding=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Label(
            header_frame,
            text="Sample Filenames Preview",
            font=("Arial", 12, "bold"),
            foreground=self.accent_color,
            background=self.panel_bg
        ).pack()
        
        # Pattern info
        info_frame = ttk.Frame(test_dialog, style="Panel.TFrame", padding=10)
        info_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ttk.Label(
            info_frame,
            text=f"Pattern: {pattern}",
            font=("Consolas", 10),
            foreground="#00CCFF",
            background=self.panel_bg
        ).pack(anchor=tk.W)
        
        # Sample files frame
        samples_frame = ttk.Frame(test_dialog, style="Panel.TFrame", padding=10)
        samples_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        samples_frame.grid_columnconfigure(0, weight=1)
        test_dialog.grid_rowconfigure(2, weight=1)
        
        # Create a canvas with scrollbar for samples
        canvas = tk.Canvas(samples_frame, background=self.panel_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(samples_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Panel.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Generate sample filenames
        sample_names = ["logo", "icon", "banner", "thumbnail", "profile"]
        sizes = [16, 32, 64, 128, 256]
        
        for i, name in enumerate(sample_names):
            frame = ttk.Frame(scrollable_frame, style="Panel.TFrame")
            frame.pack(fill=tk.X, padx=5, pady=3)
            
            # Generate name using pattern
            current_num = start_num + i
            custom_name = pattern.replace("{name}", name)
            custom_name = custom_name.replace("{num}", str(current_num))
            
            if include_dims:
                sample_size = sizes[i % len(sizes)]
                filename = f"{custom_name}_{sample_size}x{sample_size}.png"
            else:
                filename = f"{custom_name}.png"
            
            # Sample icon
            icon_label = ttk.Label(
                frame,
                text="🖼️",
                background=self.panel_bg,
                foreground="#AAAAAA"
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Filename
            filename_label = ttk.Label(
                frame,
                text=filename,
                font=("Consolas", 10),
                foreground="white",
                background=self.panel_bg
            )
            filename_label.pack(side=tk.LEFT)
            
        # Close button with enhanced styling
        button_frame = ttk.Frame(test_dialog, style="Panel.TFrame", padding=10)
        button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        close_btn = tk.Button(
            button_frame,
            text="CLOSE",
            command=test_dialog.destroy,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.beautify_button(close_btn, self.accent_color, "#0088E8", "#0064C0")
        close_btn.pack()

    def update_window_size(self):
        """Calculate and set the optimal window size for a clean fit without scrolling"""
        # Get desired widget sizes after all widgets are properly laid out
        self.root.update_idletasks()
        
        # Set a fixed, optimized size that fits all elements
        window_width = 1200  # Wider to accommodate two columns
        window_height = 800  # Taller to fit all components
        
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Make sure the window fits on the screen
        if window_height > screen_height - 100:
            window_height = screen_height - 100
            
        if window_width > screen_width - 100:
            window_width = screen_width - 100
        
        # Apply the optimized window size and center it
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Update one more time to confirm all widgets are properly displayed
        self.root.update_idletasks()

    def beautify_button(self, button, base_color, hover_color, active_color=None):
        """Add beautiful hover effects to a tkinter button"""
        if active_color is None:
            active_color = hover_color
            
        def on_enter(e):
            button['background'] = hover_color
            
        def on_leave(e):
            button['background'] = base_color
            
        def on_press(e):
            button['background'] = active_color
            
        def on_release(e):
            button['background'] = hover_color
            
        # Bind events
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<ButtonPress-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)
        
        # Apply initial styling
        button.config(
            bg=base_color,
            fg="white",
            relief=tk.RAISED,
            borderwidth=1,
            padx=10,
            pady=5
        )
        
        return button

    def manage_image_cache(self, max_items=10):
        """Keep the image cache from growing too large"""
        cache = self.__class__._image_cache
        
        # If cache is getting too large, remove oldest items
        if len(cache) > max_items * 2:  # Account for dimension entries too
            # Get keys excluding dimension entries
            image_keys = [k for k in cache.keys() if not k.endswith("_dimensions")]
            
            # Sort by recently used (if we tracked that) or just remove first ones
            if len(image_keys) > max_items:
                for old_key in image_keys[:len(image_keys) - max_items]:
                    if old_key in cache:
                        del cache[old_key]
                    if f"{old_key}_dimensions" in cache:
                        del cache[f"{old_key}_dimensions"]

def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
