#!/usr/bin/env python3

import sys

def classify_histidine(histidine_atoms):
    """Clasifica el tipo de histidina según los protones presentes."""
    has_hd1 = any("HD1" in atom for atom in histidine_atoms)
    has_he2 = any("HE2" in atom for atom in histidine_atoms)
    has_heme = any("HEME" in atom for atom in histidine_atoms)  # Verificación de acoplamiento con heme
    
    if has_heme:
        return "HIS1"  # Histidina acoplada a Heme
    elif has_hd1 and has_he2:
        return "HISH"  # Histidina diprotonada
    elif has_hd1:
        return "HISD"  # Histidina protonada en ND1
    elif has_he2:
        return "HISE"  # Histidina protonada en NE2
    else:
        return "HISD"  # Por defecto, asignar HISD si no se encuentra otra opción

def process_pdb(input_pdb, output_pdb):
    """Procesa un archivo PDB y corrige la nomenclatura de las histidinas."""
    with open(input_pdb, "r") as f:
        lines = f.readlines()
    
    histidine_groups = {}
    corrected_lines = []
    changes = {}
    
    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            res_name = line[17:20].strip()
            res_id = line[22:26].strip()
            
            if res_name == "HIS":
                if res_id not in histidine_groups:
                    histidine_groups[res_id] = []
                histidine_groups[res_id].append(line)
    
    # Identificar el tipo de cada histidina
    histidine_types = {res_id: classify_histidine(atoms) for res_id, atoms in histidine_groups.items()}
    
    # Reescribir el archivo con las histidinas corregidas
    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            res_name = line[17:20].strip()
            res_id = line[22:26].strip()
            
            if res_name == "HIS" and res_id in histidine_types:
                new_res_name = histidine_types[res_id]
                if new_res_name != "HIS" and res_id not in changes:
                    changes[res_id] = f"Residuo {res_id}: HIS -> {new_res_name}"
                line = line[:17] + new_res_name.ljust(4) + line[21:]  # Ajustar formato eliminando un espacio
        corrected_lines.append(line)
    
    # Guardar el archivo corregido
    with open(output_pdb, "w") as f:
        f.writelines(corrected_lines)
    
    # Mostrar cambios realizados
    print("Histidinas corregidas:")
    for change in changes.values():
        print(change)
    print(f"Histidinas corregidas y guardadas en {output_pdb}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py archivo_entrada.pdb archivo_salida.pdb")
        sys.exit(1)
    
    input_pdb = sys.argv[1]
    output_pdb = sys.argv[2]
    process_pdb(input_pdb, output_pdb)

