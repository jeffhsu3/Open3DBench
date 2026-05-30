import os
import re
import sys
import subprocess
import urllib.request

# Paths setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASAP7_DIR = os.path.join(SCRIPT_DIR, 'asap7')
ASAP7_3D_DIR = os.path.join(SCRIPT_DIR, 'asap7_3D')

# Remote URL base
BASE_URL = "https://raw.githubusercontent.com/The-OpenROAD-Project/asap7sc7p5t_27/main"

# 2D LEF files mapping (remote_path: local_filename)
LEF_FILES = {
    "techlef_misc/asap7_tech_4x_201209.lef": "asap7_tech.lef",
    "LEF/scaled/asap7sc7p5t_27_L_4x_201211.lef": "asap7sc7p5t_27_L_4x_201211.lef",
    "LEF/scaled/asap7sc7p5t_27_R_4x_201211.lef": "asap7sc7p5t_27_R_4x_201211.lef",
    "LEF/scaled/asap7sc7p5t_27_SL_4x_201211.lef": "asap7sc7p5t_27_SL_4x_201211.lef",
    "LEF/scaled/asap7sc7p5t_27_SRAM_4x_201211.lef": "asap7sc7p5t_27_SRAM_4x_201211.lef",
}

# 2D Liberty files to download
LIB_FILES = [
    "asap7sc7p5t_INVBUF_RVT_TT_nldm_201020.lib",
    "asap7sc7p5t_SIMPLE_RVT_TT_nldm_201020.lib",
    "asap7sc7p5t_AO_RVT_TT_nldm_201020.lib",
    "asap7sc7p5t_OA_RVT_TT_nldm_201020.lib",
    "asap7sc7p5t_SEQ_RVT_TT_nldm_201020.lib",
]

def download_file(url, dest_path):
    print(f"Downloading {url} -> {dest_path}")
    urllib.request.urlretrieve(url, dest_path)

def extract_7z(archive_path, extract_dir):
    print(f"Extracting {archive_path} -> {extract_dir}")
    for cmd in ['7z', '7za']:
        try:
            subprocess.run(
                [cmd, 'x', '-y', f'-o{extract_dir}', archive_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    raise RuntimeError("Failed to extract: neither 7z nor 7za is available or working.")

def parse_tech_lef(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    if 'END PROPERTYDEFINITIONS' in content:
        header_match = re.search(r'^(.*?\bEND PROPERTYDEFINITIONS\b\s*)', content, re.DOTALL)
    else:
        header_match = re.search(r'^(.*?)(?=\bLAYER\b)', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''
    
    layers = {}
    layer_iter = re.finditer(r'\bLAYER\s+(\S+)\b(.*?)\bEND\s+\1\b', content, re.DOTALL)
    for m in layer_iter:
        layers[m.group(1)] = m.group(2)
        
    vias = {}
    via_iter = re.finditer(r'\bVIA\s+(\S+)\b(.*?)\bEND\s+\1\b', content, re.DOTALL)
    for m in via_iter:
        vias[m.group(1)] = m.group(2)
        
    viarules = {}
    viarule_iter = re.finditer(r'\bVIARULE\s+(\S+)\b(.*?)\bEND\s+\1\b', content, re.DOTALL)
    for m in viarule_iter:
        viarules[m.group(1)] = m.group(2)
        
    spacing_match = re.search(r'\bSPACING\b(.*?)\bEND\s+SPACING\b', content, re.DOTALL)
    spacing_content = spacing_match.group(1) if spacing_match else ''
    
    sites = []
    site_iter = re.finditer(r'\bSITE\s+(\S+)\b(.*?)\bEND\s+\1\b', content, re.DOTALL)
    for m in site_iter:
        sites.append((m.group(1), m.group(2)))
        
    return header, layers, vias, viarules, spacing_content, sites

def generate_3d_tech():
    input_file = os.path.join(ASAP7_DIR, 'asap7_tech.lef')
    output_file = os.path.join(ASAP7_3D_DIR, 'lef', 'asap7_3D.tech.lef')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Generating 3D tech LEF -> {output_file}")
    header, layers, vias, viarules, spacing_content, sites = parse_tech_lef(input_file)
    
    bottom_layer_names = [
        'nwell', 'pwell', 'Gate', 'Active', 'V0',
        'M1', 'V1', 'M2', 'V2', 'M3', 'V3', 'M4', 'V4', 'M5', 'V5', 'M6', 'V6', 'M7', 'V7', 'M8', 'V8', 'M9'
    ]
    
    out = [header]
    
    # Write bottom layers
    for lname in bottom_layer_names:
        if lname in layers:
            out.append(f"LAYER {lname}\n{layers[lname]}\nEND {lname}\n")
            
    # Add hb_layer (hybrid bond cut layer)
    out.append("""LAYER hb_layer
  TYPE CUT ;
  SPACING 0.228 ;
  WIDTH 0.16 ;
  RESISTANCE 0.01 ;
END hb_layer
""")
    
    # Top layers remapping
    top_layers_ordered = [
        ('M9', 'M10'), ('V8', 'V10'),
        ('M8', 'M11'), ('V7', 'V11'),
        ('M7', 'M12'), ('V6', 'V12'),
        ('M6', 'M13'), ('V5', 'V13'),
        ('M5', 'M14'), ('V4', 'V14'),
        ('M4', 'M15'), ('V3', 'V15'),
        ('M3', 'M16'), ('V2', 'V16'),
        ('M2', 'M17'), ('V1', 'V17'),
        ('M1', 'M18')
    ]
    
    for orig, target in top_layers_ordered:
        block = layers[orig]
        if target.startswith('M'):
            # Alternate layer routing directions
            if 'DIRECTION VERTICAL' in block:
                block = block.replace('DIRECTION VERTICAL', 'DIRECTION TEMP_DIR')
                block = block.replace('DIRECTION HORIZONTAL', 'DIRECTION VERTICAL')
                block = block.replace('DIRECTION TEMP_DIR', 'DIRECTION HORIZONTAL')
            elif 'DIRECTION HORIZONTAL' in block:
                block = block.replace('DIRECTION HORIZONTAL', 'DIRECTION TEMP_DIR')
                block = block.replace('DIRECTION VERTICAL', 'DIRECTION HORIZONTAL')
                block = block.replace('DIRECTION TEMP_DIR', 'DIRECTION VERTICAL')
        out.append(f"LAYER {target}\n{block}\nEND {target}\n")
        
    # Write bottom vias
    bottom_via_names = [
        'VIA12', 'VIA23', 'VIA34', 'VIA45', 'VIA56', 'VIA67', 'VIA78', 'VIA89'
    ]
    for vname in bottom_via_names:
        for full_vname in vias:
            if full_vname.startswith(vname):
                out.append(f"VIA {full_vname}\n{vias[full_vname]}\nEND {full_vname}\n")
                
    # Add hb_layer_0 via
    out.append("""VIA hb_layer_0 DEFAULT
  LAYER M9 ;
    RECT -0.08 -0.08 0.08 0.08 ;
  LAYER M10 ;
    RECT -0.08 -0.08 0.08 0.08 ;
  LAYER hb_layer ;
    RECT -0.08 -0.08 0.08 0.08 ;
END hb_layer_0
""")
    
    # Add top vias
    via_mappings = [
        ('VIA89', 'VIA1011', 'M8', 'M11', 'M9', 'M10', 'V8', 'V10'),
        ('VIA78', 'VIA1112', 'M7', 'M12', 'M8', 'M11', 'V7', 'V11'),
        ('VIA67', 'VIA1213', 'M6', 'M13', 'M7', 'M12', 'V6', 'V12'),
        ('VIA56', 'VIA1314', 'M5', 'M14', 'M6', 'M13', 'V5', 'V13'),
        ('VIA45', 'VIA1415', 'M4', 'M15', 'M5', 'M14', 'V4', 'V14'),
        ('VIA34', 'VIA1516', 'M3', 'M16', 'M4', 'M15', 'V3', 'V15'),
        ('VIA23', 'VIA1617', 'M2', 'M17', 'M3', 'M16', 'V2', 'V16'),
        ('VIA12', 'VIA1718', 'M1', 'M18', 'M2', 'M17', 'V1', 'V17')
    ]
    
    for orig_v, target_v, l1_orig, l1_targ, l2_orig, l2_targ, lc_orig, lc_targ in via_mappings:
        for full_vname in vias:
            if full_vname.startswith(orig_v):
                target_full = full_vname.replace(orig_v, target_v)
                block = vias[full_vname]
                block = block.replace(f"LAYER {l1_orig}", f"LAYER {l1_targ}")
                block = block.replace(f"LAYER {l2_orig}", f"LAYER {l2_targ}")
                block = block.replace(f"LAYER {lc_orig}", f"LAYER {lc_targ}")
                out.append(f"VIA {target_full}\n{block}\nEND {target_full}\n")
                
    # Write viarules
    bottom_viarule_names = [
        'M9_M8', 'M8_M7', 'M7_M6', 'M6_M5', 'M2_M1'
    ]
    for vrname in viarules:
        if any(vrname.startswith(x) for x in bottom_viarule_names):
            out.append(f"VIARULE {vrname}\n{viarules[vrname]}\nEND {vrname}\n")
            
    # Add top viarules
    viarule_mappings = [
        ('M9_M8', 'M10_M11', 'M8', 'M11', 'M9', 'M10', 'V8', 'V10'),
        ('M8_M7', 'M11_M12', 'M7', 'M12', 'M8', 'M11', 'V7', 'V11'),
        ('M7_M6', 'M12_M13', 'M6', 'M13', 'M7', 'M12', 'V6', 'V12'),
        ('M6_M5', 'M13_M14', 'M5', 'M14', 'M6', 'M13', 'V5', 'V13'),
        ('M2_M1', 'M17_M18', 'M1', 'M18', 'M2', 'M17', 'V1', 'V17')
    ]
    for orig_vr, target_vr, l1_orig, l1_targ, l2_orig, l2_targ, lc_orig, lc_targ in viarule_mappings:
        for full_vrname in viarules:
            if full_vrname.startswith(orig_vr):
                target_full = full_vrname.replace(orig_vr, target_vr)
                block = viarules[full_vrname]
                block = block.replace(f"LAYER {l1_orig}", f"LAYER {l1_targ}")
                block = block.replace(f"LAYER {l2_orig}", f"LAYER {l2_targ}")
                block = block.replace(f"LAYER {lc_orig}", f"LAYER {lc_targ}")
                out.append(f"VIARULE {target_full}\n{block}\nEND {target_full}\n")
                
    # Add SPACING block
    out.append("""SPACING
  SAMENET M1 M1 0.072 ;
  SAMENET M2 M2 0.072 ;
  SAMENET M3 M3 0.072 ;
  SAMENET M4 M4 0.072 ;
  SAMENET M5 M5 0.072 ;
  SAMENET M6 M6 0.072 ;
  SAMENET M7 M7 0.072 ;
  SAMENET M8 M8 0.072 ;
  SAMENET M9 M9 0.16 ;
  SAMENET M10 M10 0.16 ;
  SAMENET M11 M11 0.072 ;
  SAMENET M12 M12 0.072 ;
  SAMENET M13 M13 0.072 ;
  SAMENET M14 M14 0.072 ;
  SAMENET M15 M15 0.072 ;
  SAMENET M16 M16 0.072 ;
  SAMENET M17 M17 0.072 ;
  SAMENET M18 M18 0.072 ;
  SAMENET V1 V1 0.072 ;
  SAMENET V2 V2 0.072 ;
  SAMENET V3 V3 0.072 ;
  SAMENET V4 V4 0.072 ;
  SAMENET V5 V5 0.072 ;
  SAMENET V6 V6 0.072 ;
  SAMENET V7 V7 0.072 ;
  SAMENET V8 V8 0.16 ;
  SAMENET hb_layer hb_layer 0.228 ;
  SAMENET V10 V10 0.16 ;
  SAMENET V11 V11 0.072 ;
  SAMENET V12 V12 0.072 ;
  SAMENET V13 V13 0.072 ;
  SAMENET V14 V14 0.072 ;
  SAMENET V15 V15 0.072 ;
  SAMENET V16 V16 0.072 ;
  SAMENET V17 V17 0.072 ;
  SAMENET V1 V2 0.0 STACK ;
  SAMENET V2 V3 0.0 STACK ;
  SAMENET V3 V4 0.0 STACK ;
  SAMENET V4 V5 0.0 STACK ;
  SAMENET V5 V6 0.0 STACK ;
  SAMENET V6 V7 0.0 STACK ;
  SAMENET V7 V8 0.0 STACK ;
  SAMENET V8 hb_layer 0.0 STACK ;
  SAMENET hb_layer V10 0.0 STACK ;
  SAMENET V10 V11 0.0 STACK ;
  SAMENET V11 V12 0.0 STACK ;
  SAMENET V12 V13 0.0 STACK ;
  SAMENET V13 V14 0.0 STACK ;
  SAMENET V14 V15 0.0 STACK ;
  SAMENET V15 V16 0.0 STACK ;
  SAMENET V16 V17 0.0 STACK ;
END SPACING
""")
    
    # Write SITES
    for sname, sblock in sites:
        out.append(f"SITE {sname}\n{sblock}\nEND {sname}\n")
        
    out.append("END LIBRARY\n")
    
    with open(output_file, 'w') as f:
        f.write("".join(out))
    print("Successfully generated 3D tech LEF.")

def get_macro_names(content):
    return set(re.findall(r'\bMACRO\s+(\S+)\b', content))

def process_lef_bottom(content, macro_names):
    for mname in macro_names:
        content = re.sub(rf'\b{re.escape(mname)}\b', f'{mname}_bottom', content)
    return content

def process_lef_upper(content, macro_names):
    for mname in macro_names:
        content = re.sub(rf'\b{re.escape(mname)}\b', f'{mname}_upper', content)
    
    layer_map = {
        'M1': 'M18', 'M2': 'M17', 'M3': 'M16', 'M4': 'M15',
        'M5': 'M14', 'M6': 'M13', 'M7': 'M12', 'M8': 'M11', 'M9': 'M10'
    }
    for orig, target in layer_map.items():
        content = re.sub(rf'\bLAYER\s+{orig}\b', f'LAYER {target}', content)
    return content

def generate_3d_cells():
    bottom_dir = os.path.join(ASAP7_3D_DIR, 'lef_bottom')
    upper_dir = os.path.join(ASAP7_3D_DIR, 'lef_upper')
    os.makedirs(bottom_dir, exist_ok=True)
    os.makedirs(upper_dir, exist_ok=True)
    
    print("Generating 3D cell LEF files...")
    files = [f for f in os.listdir(ASAP7_DIR) if f.endswith('.lef') and f != 'asap7_tech.lef']
    
    for fname in files:
        filepath = os.path.join(ASAP7_DIR, fname)
        with open(filepath, 'r') as f:
            content = f.read()
            
        macro_names = get_macro_names(content)
        
        # Bottom
        content_bottom = process_lef_bottom(content, macro_names)
        out_fname_bottom = fname.replace('.lef', '.bottom.lef')
        with open(os.path.join(bottom_dir, out_fname_bottom), 'w') as f:
            f.write(content_bottom)
            
        # Upper
        content_upper = process_lef_upper(content, macro_names)
        out_fname_upper = fname.replace('.lef', '.upper.lef')
        with open(os.path.join(upper_dir, out_fname_upper), 'w') as f:
            f.write(content_upper)

def process_lib_bottom(content):
    content = re.sub(r'\blibrary\s*\(\s*([a-zA-Z0-9_]+)\s*\)', r'library (\1_bottom)', content)
    content = re.sub(r'\bcell\s*\(\s*([a-zA-Z0-9_]+)\s*\)', r'cell (\1_bottom)', content)
    return content

def process_lib_upper(content):
    content = re.sub(r'\blibrary\s*\(\s*([a-zA-Z0-9_]+)\s*\)', r'library (\1_upper)', content)
    content = re.sub(r'\bcell\s*\(\s*([a-zA-Z0-9_]+)\s*\)', r'cell (\1_upper)', content)
    return content

def generate_3d_libs():
    bottom_dir = os.path.join(ASAP7_3D_DIR, 'lib_bottom')
    upper_dir = os.path.join(ASAP7_3D_DIR, 'lib_upper')
    os.makedirs(bottom_dir, exist_ok=True)
    os.makedirs(upper_dir, exist_ok=True)
    
    print("Generating 3D cell Liberty files...")
    files = [f for f in os.listdir(ASAP7_DIR) if f.endswith('.lib')]
    
    for fname in files:
        filepath = os.path.join(ASAP7_DIR, fname)
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Bottom
        content_bottom = process_lib_bottom(content)
        out_fname_bottom = fname.replace('.lib', '.bottom.lib')
        with open(os.path.join(bottom_dir, out_fname_bottom), 'w') as f:
            f.write(content_bottom)
            
        # Upper
        content_upper = process_lib_upper(content)
        out_fname_upper = fname.replace('.lib', '.upper.lib')
        with open(os.path.join(upper_dir, out_fname_upper), 'w') as f:
            f.write(content_upper)

def main():
    os.makedirs(ASAP7_DIR, exist_ok=True)
    
    # 1. Download LEF files
    for remote, local in LEF_FILES.items():
        url = f"{BASE_URL}/{remote}"
        dest = os.path.join(ASAP7_DIR, local)
        if not os.path.exists(dest):
            download_file(url, dest)
        else:
            print(f"Skipping download of {local} (already exists).")
            
    # 2. Download and extract Liberty files
    for lib in LIB_FILES:
        dest_lib = os.path.join(ASAP7_DIR, lib)
        if os.path.exists(dest_lib):
            print(f"Skipping download of {lib} (already exists).")
            continue
            
        archive = f"{lib}.7z"
        url = f"{BASE_URL}/LIB/NLDM/{archive}"
        dest_archive = os.path.join(ASAP7_DIR, archive)
        
        # Download archive
        download_file(url, dest_archive)
        
        # Extract archive
        try:
            extract_7z(dest_archive, ASAP7_DIR)
        finally:
            # Clean up the .7z archive
            if os.path.exists(dest_archive):
                os.remove(dest_archive)
                
    # 3. Generate 3D Platform collateral
    generate_3d_tech()
    generate_3d_cells()
    generate_3d_libs()
    
    print("\nASAP7 2D & 3D PDK setup successfully completed!")

if __name__ == '__main__':
    main()
