import astroid

def check_leakage(code_content):
    """
    Improved Leakage Checker.
    - Scans inside functions.
    - Reports parsing errors instead of failing silently.
    """
    issues = []
    try:
        tree = astroid.parse(code_content)
        
        split_lines = []
        fit_lines = []

        # Traverse all nodes in the tree recursively
        for node in tree.body:
            # nodes_of_class finds nodes anywhere inside this node (deep scan)
            for call in node.nodes_of_class(astroid.nodes.Call):
                
                # 1. Identify train_test_split
                func_name = ""
                if isinstance(call.func, astroid.nodes.Name):
                    func_name = call.func.name
                elif isinstance(call.func, astroid.nodes.Attribute):
                    func_name = call.func.attrname
                
                if func_name == "train_test_split":
                    split_lines.append(call.lineno)

                # 2. Identify fit or fit_transform
                if func_name in ["fit", "fit_transform"]:
                    fit_lines.append(call.lineno)

        # 3. Compare: Leakage happens if fit happens BEFORE split
        if split_lines: # Only check if a split exists
            min_split_line = min(split_lines)
            for fit_line in fit_lines:
                if fit_line < min_split_line:
                    issues.append({
                        "type": "Data Leakage",
                        "severity": "Critical",
                        "line": fit_line,
                        "message": f"Data Leakage Risk: Scaler/Model fitted on line {fit_line} BEFORE train_test_split on line {min_split_line}."
                    })

    except Exception as e:
        # If we fail to parse, report it so user knows score is not 100%
        issues.append({
            "type": "Checker Error",
            "severity": "High",
            "line": 0,
            "message": f"Leakage checker failed: {str(e)}"
        })
        
    return issues
