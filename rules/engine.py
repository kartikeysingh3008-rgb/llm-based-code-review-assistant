def generate_suggestions(analysis):
    suggestions = []

    loops = analysis.get("loops", 0)
    depth = analysis.get("max_nesting_depth", 0)
    functions = analysis.get("functions", [])

    # Loop-based rules
    if loops >= 2:
        suggestions.append("Multiple loops detected. Consider optimizing using better data structures like sets or dictionaries.")

    # Nesting rules
    if depth >= 3:
        suggestions.append("Deep nesting detected. Try reducing nested structures for better readability.")

    # Function length rules
    for func in functions:
        if func["length"] > 30:
            suggestions.append(f"Function '{func['name']}' is too long. Consider breaking it into smaller functions.")

    # Default fallback
    if not suggestions:
        suggestions.append("Code looks clean. No major issues detected.")

    return suggestions