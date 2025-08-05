import re
import os

class CSSToQSSConverter:
    def __init__(self):
        # Mapeo de colores OKLCH a valores hexadecimales
        self.oklch_colors = {
            # Modo claro
            "oklch(1.0000 0 0)": "#ffffff",              # Blanco
            "oklch(0.2167 0.0015 197.0424)": "#191a1a",  # Negro personalizado para modo oscuro
            "oklch(0.9851 0 0)": "#fafbfc",              # Blanco casi puro
            "oklch(0.9702 0 0)": "#f8f9fa",              # Gris muy claro
            "oklch(0.9219 0 0)": "#e4e7ec",              # Gris claro (bordes)
            "oklch(0.5555 0 0)": "#8e929e",              # Gris medio
            "oklch(0.7090 0 0)": "#b5b9c4",              # Gris claro medio
            
            # Modo oscuro
            "oklch(0.2686 0 0)": "#2a2b2b",              # Secondary oscuro
            "oklch(0.2768 0 0)": "#3a3b3b",              # Bordes oscuros
            "oklch(0.3250 0 0)": "#2a2b2b",              # Input oscuro
            "oklch(0.3715 0 0)": "#5e6369",              # Accent oscuro
            "oklch(0.4386 0 0)": "#70757c",              # Ring oscuro
            "oklch(0.5786 0.2242 26.6169)": "#e01b24",   # Primary rojo personalizado
            "oklch(0.8232 0.1625 169.0750)": "#5dade2",  # Sidebar primary azul
            "oklch(0.7516 0.2509 326.9361)": "#e74c3c",  # Destructive rojo
        }
    
    def load_css_variables(self, css_file_path, dark_mode=False):
        """Carga las variables CSS del archivo y las convierte a valores hexadecimales"""
        variables = {}
        
        if not os.path.exists(css_file_path):
            return self.get_default_variables(dark_mode)
        
        try:
            with open(css_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Buscar variables en :root o .dark según el modo
            if dark_mode:
                section_match = re.search(r'\.dark\s*\{([^}]+)\}', content, re.DOTALL)
            else:
                section_match = re.search(r':root\s*\{([^}]+)\}', content, re.DOTALL)
            
            if section_match:
                section_content = section_match.group(1)
                
                # Buscar variables con valores OKLCH
                var_pattern = r'--([^:]+):\s*oklch\([^)]+\);'
                matches = re.findall(var_pattern, section_content)
                
                for var_name in matches:
                    # Extraer el valor OKLCH completo
                    value_pattern = rf'--{re.escape(var_name)}:\s*(oklch\([^)]+\));'
                    value_match = re.search(value_pattern, section_content)
                    if value_match:
                        oklch_value = value_match.group(1)
                        hex_value = self.oklch_colors.get(oklch_value, "#000000")
                        variables[var_name] = hex_value
            
            return variables
        
        except Exception as e:
            print(f"Error leyendo archivo CSS: {e}")
            return self.get_default_variables(dark_mode)
    
    def get_default_variables(self, dark_mode=False):
        """Variables por defecto si no se puede leer el archivo CSS"""
        if dark_mode:
            return {
                'background': '#191a1a',
                'foreground': '#fafbfc', 
                'primary': '#e01b24',
                'primary-foreground': '#fafbfc',
                'secondary': '#2a2b2b',
                'border': '#3a3b3b',
                'input': '#2a2b2b',
                'muted-foreground': '#b5b9c4',
            }
        else:
            return {
                'background': '#ffffff',
                'foreground': '#363a47', 
                'primary': '#363a47',
                'primary-foreground': '#fafbfc',
                'secondary': '#f8f9fa',
                'border': '#e4e7ec',
                'input': '#e4e7ec',
                'muted-foreground': '#8e929e',
            }
    
    def generate_qss(self, css_file_path, dark_mode=False):
        """Genera QSS basado en las variables CSS"""
        variables = self.load_css_variables(css_file_path, dark_mode)
        
        # Extraer colores principales
        background = variables.get('background', '#ffffff' if not dark_mode else '#191a1a')
        foreground = variables.get('foreground', '#363a47' if not dark_mode else '#fafbfc')
        primary = variables.get('primary', '#363a47' if not dark_mode else '#e01b24')
        primary_foreground = variables.get('primary-foreground', '#fafbfc' if not dark_mode else '#fafbfc')
        secondary = variables.get('secondary', '#f8f9fa' if not dark_mode else '#2a2b2b')
        border = variables.get('border', '#e4e7ec' if not dark_mode else '#3a3b3b')
        disabled = variables.get('muted-foreground', '#8e929e' if not dark_mode else '#b5b9c4')
        
        # Colores específicos para hover y pressed
        if dark_mode:
            hover_color = "#f72c3a"  # Un poco más claro que el rojo
            pressed_color = "#c1151d"  # Un poco más oscuro que el rojo
        else:
            hover_color = "#2c3036"
            pressed_color = "#404550"
        
        qss = f"""
            QWidget {{
                background-color: {background};
                color: {foreground};
                font-family: 'AR One Sans', 'Segoe UI', system-ui, sans-serif;
                font-size: 14px;
            }}
            
            QLabel {{
                color: {foreground};
                font-weight: 500;
                padding: 4px 0px;
            }}
            
            QLineEdit {{
                background-color: {background};
                border: 2px solid {border};
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 14px;
                color: {foreground};
                min-height: 20px;
            }}
            
            QLineEdit:focus {{
                border-color: {primary};
                outline: none;
            }}
            
            QPushButton {{
                background-color: {primary};
                color: {primary_foreground};
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 20px;
                min-width: 100px;
            }}
            
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            
            QPushButton:disabled {{
                background-color: {disabled};
                color: #ffffff;
            }}
            
            QProgressBar {{
                border: 2px solid {border};
                border-radius: 10px;
                background-color: {secondary};
                text-align: center;
                font-weight: 600;
                height: 30px;
            }}
            
            QProgressBar::chunk {{
                background-color: {primary};
                border-radius: 8px;
                margin: 2px;
            }}
            
            QLabel#statusLabel {{
                background-color: {secondary};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 12px;
                font-weight: 500;
            }}
            
            QPushButton#themeToggle {{
                background-color: {secondary};
                color: {foreground};
                border: 2px solid {border};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 500;
                min-width: 80px;
            }}
            
            QPushButton#themeToggle:hover {{
                background-color: {border};
            }}
        """
        
        return qss
