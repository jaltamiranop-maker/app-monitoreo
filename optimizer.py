PANEL_SIZES = [12000, 9000, 6000, 3000]

def optimize_cutting(cortes_input):
    # 1. Expandir y ordenar cortes de mayor a menor (Estrategia Decreasing)
    # Los cortes grandes son más difíciles de ubicar, por eso van primero.
    cuts = []
    for item in cortes_input:
        cuts += [item.longitud] * item.cantidad
    cuts.sort(reverse=True)

    used_panels = []

    for cut in cuts:
        best_panel_index = -1
        min_waste_after_cut = float('inf')
        
        # 2. Buscar en los paneles que ya estamos usando si cabe el corte
        for i, panel in enumerate(used_panels):
            remaining_space = panel["remaining"]
            if remaining_space >= cut:
                waste_after = remaining_space - cut
                # "Best-fit": Elegimos el panel donde quede MENOS espacio libre
                if waste_after < min_waste_after_cut:
                    min_waste_after_cut = waste_after
                    best_panel_index = i

        # 3. Si cabe en un panel existente, lo metemos ahí
        if best_panel_index != -1:
            used_panels[best_panel_index]["cuts"].append(cut)
            used_panels[best_panel_index]["remaining"] -= cut
        
        # 4. Si NO cabe en ninguno, abrimos un panel nuevo del tamaño óptimo
        else:
            # Elegimos el panel más pequeño posible de la lista de Kingspan donde quepa el corte
            possible_sizes = [s for s in PANEL_SIZES if s >= cut]
            if not possible_sizes:
                continue # El corte es más grande que cualquier panel disponible
            
            chosen_size = min(possible_sizes)
            used_panels.append({
                "panel_size": chosen_size,
                "cuts": [cut],
                "remaining": chosen_size - cut
            })

    # Re-ajustar el tamaño del panel: 
    # Si un panel de 12000 solo usó 2500, el algoritmo lo "encoge" al tamaño estándar más pequeño (3000)
    for panel in used_panels:
        actual_usage = panel["panel_size"] - panel["remaining"]
        new_best_size = min([s for s in PANEL_SIZES if s >= actual_usage])
        panel["panel_size"] = new_best_size
        panel["waste"] = new_best_size - actual_usage

    return used_panels

def format_output(panels):
    result = []
    for i, p in enumerate(panels, 1):
        # Dinámicamente creamos las columnas de cortes para no limitarnos a 3
        row = {
            "Panel": i,
            "Tamaño": p["panel_size"],
            "Cortes": ", ".join(map(str, p["cuts"])),
            "Desperdicio": p["waste"]
        }
        result.append(row)
    return result