PANEL_SIZES = [12000, 9000, 6000, 3000]

def optimize_cutting(cortes_input):
    # 1. Expandir y ordenar cortes de mayor a menor
    # El orden descendente es clave para que los cortes grandes ocupen su lugar
    # y los pequeños rellenen los huecos sobrantes en el mismo panel.
    cuts = []
    for item in cortes_input:
        cuts += [item.longitud] * item.cantidad
    cuts.sort(reverse=True)

    used_panels = []

    for cut in cuts:
        best_panel_index = -1
        
        # 2. INTENTO DE ACUMULACIÓN: Buscar en paneles ya abiertos
        # Priorizamos el primer panel de la lista (First-Fit).
        # Como el primer panel que abrimos es de 12000mm, intentará llenarlo al 100%.
        for i, panel in enumerate(used_panels):
            if panel["remaining"] >= cut:
                best_panel_index = i
                break 

        if best_panel_index != -1:
            used_panels[best_panel_index]["cuts"].append(cut)
            used_panels[best_panel_index]["remaining"] -= cut
        
        # 3. APERTURA DE NUEVO PANEL: Prioridad Máxima al de 12000mm[cite: 5]
        else:
            # Filtramos tamaños donde quepa el corte
            possible_sizes = [s for s in PANEL_SIZES if s >= cut]
            
            if not possible_sizes:
                continue 
            
            # --- CAMBIO CRÍTICO PARA TU REQUERIMIENTO ---
            # Forzamos que, si el corte cabe en el panel más grande de Kingspan (12000), 
            # se use ese, incluso si el corte es muy pequeño (ej. 120mm).
            # Esto "acumula" espacio para los siguientes 99 cortes en el mismo panel.
            if 12000 >= cut:
                chosen_size = 12000
            else:
                chosen_size = max(possible_sizes) 
            
            used_panels.append({
                "panel_size": chosen_size,
                "cuts": [cut],
                "remaining": chosen_size - cut
            })

    # 4. RE-AJUSTE DE EFICIENCIA (Opcional)[cite: 5]
    # Solo al final, si un panel quedó casi vacío y NO es de 12000,
    # verificamos si podemos usar un tamaño estándar menor para no desperdiciar material.
    for panel in used_panels:
        actual_usage = panel["panel_size"] - panel["remaining"]
        # Buscamos el tamaño estándar más pequeño que cubra lo que realmente se cortó
        efficient_size = min([s for s in PANEL_SIZES if s >= actual_usage])
        panel["panel_size"] = efficient_size
        panel["waste"] = efficient_size - actual_usage

    return used_panels

def format_output(panels):
    # Mantenemos tu estructura de salida para la tabla de Streamlit[cite: 5]
    result = []
    for i, p in enumerate(panels, 1):
        row = {
            "Panel": i,
            "Tamaño": p["panel_size"],
            "Cortes": ", ".join(map(str, p["cuts"])),
            "Desperdicio": p["waste"]
        }
        result.append(row)
    return result
