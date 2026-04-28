PANEL_SIZES = [12000, 9000, 6000, 3000]


# -------------------------
# Expandir cortes
# -------------------------
def expand_cuts(cortes):
    expanded = []
    for item in cortes:
        expanded += [item.longitud] * item.cantidad
    return expanded


# -------------------------
# FASE 1: agrupar iguales
# -------------------------
def group_equal_cuts(cuts):
    result = []


    from collections import Counter
    count = Counter(cuts)


    for length, qty in count.items():


        while qty > 0:
            best_option = None


            # probar todas las combinaciones posibles (1 a 4 piezas)
            for pieces in range(1, min(qty, 4) + 1):
                total = length * pieces


                for panel in PANEL_SIZES:
                    if panel >= total:
                        waste = panel - total


                        if best_option is None or waste < best_option["waste"]:
                            best_option = {
                                "panel_size": panel,
                                "cuts": [length] * pieces,
                                "waste": waste,
                                "pieces": pieces
                            }


            result.append({
                "panel_size": best_option["panel_size"],
                "cuts": best_option["cuts"],
                "waste": best_option["waste"]
            })


            qty -= best_option["pieces"]


    return result       


# -------------------------
# FASE 2: combinaciones perfectas
# -------------------------
def combine_pairs(cuts):
    result = []
    cuts = cuts.copy()


    i = 0
    while i < len(cuts):
        found = False


        for j in range(i+1, len(cuts)):
            total = cuts[i] + cuts[j]


            # 🔥 elegir panel estándar
            possible_panels = [p for p in PANEL_SIZES if p >= total]


            if possible_panels:
                panel_size = min(possible_panels)


                result.append({
                    "panel_size": panel_size,
                    "cuts": [cuts[i], cuts[j]],
                    "waste": panel_size - total
                })


                cuts.pop(j)
                cuts.pop(i)
                found = True
                break


        if not found:
            i += 1


    return result, cuts
    return result, cuts


# -------------------------
# FASE 3: greedy final
# -------------------------
def greedy_cut(cuts):
    panels = []


    while cuts:
        best = None


        for size in PANEL_SIZES:
            temp = []
            total = 0


            for c in cuts:
                if total + c <= size:
                    temp.append(c)
                    total += c


            waste = size - total
            usage = total / size  # 🔥 porcentaje de uso


            if best is None:
                best = {
                    "panel_size": size,
                    "cuts": temp,
                    "waste": waste,
                    "usage": usage
                }
            else:
                # 🔥 criterio doble
                if (
                    waste < best["waste"] or
                    (waste == best["waste"] and usage > best["usage"])
                ):
                    best = {
                        "panel_size": size,
                        "cuts": temp,
                        "waste": waste,
                        "usage": usage
                    }


        for c in best["cuts"]:
            cuts.remove(c)


        panels.append({
            "panel_size": best["panel_size"],
            "cuts": best["cuts"],
            "waste": best["waste"]
        })


    return panels


# -------------------------
# MOTOR PRINCIPAL
# -------------------------
def optimize_cutting(cortes_input):
    cuts = expand_cuts(cortes_input)
    cuts.sort(reverse=True)


    panels = []


    while cuts:
        best = None


        for size in PANEL_SIZES:
            best_combo = []
            best_total = 0


            # probar combinaciones
            def backtrack(start, current, total):
                nonlocal best_combo, best_total


                if total > size:
                    return


                if total > best_total:
                    best_total = total
                    best_combo = current.copy()


                for i in range(start, len(cuts)):
                    backtrack(i + 1, current + [cuts[i]], total + cuts[i])


            backtrack(0, [], 0)


            waste = size - best_total
            usage = best_total / size if size > 0 else 0


            if best is None:
                best = {
                    "panel_size": size,
                    "cuts": best_combo,
                    "waste": waste,
                    "usage": usage
                }
            else:
                if (
                    waste < best["waste"] or
                    (waste == best["waste"] and usage > best["usage"])
                ):
                    best = {
                        "panel_size": size,
                        "cuts": best_combo,
                        "waste": waste,
                        "usage": usage
                    }


        # eliminar cortes usados
        for c in best["cuts"]:
            cuts.remove(c)


        panels.append({
            "panel_size": best["panel_size"],
            "cuts": best["cuts"],
            "waste": best["waste"]
        })


    return panels


# -------------------------
# FORMATO FINAL
# -------------------------
def format_output(panels):
    result = []


    for i, p in enumerate(panels, 1):
        row = {
            "Panel": i,
            "Tamaño": p["panel_size"],
            "Corte 1": p["cuts"][0] if len(p["cuts"]) > 0 else "",
            "Corte 2": p["cuts"][1] if len(p["cuts"]) > 1 else "",
            "Corte 3": p["cuts"][2] if len(p["cuts"]) > 2 else "",
            "Desperdicio": p["waste"]
        }
        result.append(row)


    return result   