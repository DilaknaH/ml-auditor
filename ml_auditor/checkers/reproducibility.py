import astroid

def check_reproducibility(code_content):
    """
    Improved Reproducibility Checker.
    Deep scans for missing random_state.
    """
    issues = []
    try:
        tree = astroid.parse(code_content)
        
        for node in tree.body:
            for call in node.nodes_of_class(astroid.nodes.Call):
                
                # 1. Check train_test_split
                if isinstance(call.func, astroid.nodes.Name) and call.func.name == 'train_test_split':
                    has_rs = any(kw.arg == 'random_state' for kw in call.keywords)
                    if not has_rs:
                        issues.append({
                            "type": "Reproducibility",
                            "severity": "Medium",
                            "line": call.lineno,
                            "message": "Non-reproducible split: 'train_test_split' used without 'random_state'."
                        })

                # 2. Check Model Initialization
                if isinstance(call.func, astroid.nodes.Attribute) or isinstance(call.func, astroid.nodes.Name):
                     class_name = ""
                     if isinstance(call.func, astroid.nodes.Attribute):
                         class_name = call.func.attrname
                     elif isinstance(call.func, astroid.nodes.Name):
                         class_name = call.func.name
                     
                     # List of common models that need random_state
                     targets = ["Classifier", "Regressor", "Forest", "Boost", "XGB", "LGBM", "SVM", "KMeans"]
                     if any(t in class_name for t in targets):
                         has_rs = any(kw.arg == 'random_state' for kw in call.keywords)
                         if not has_rs:
                             issues.append({
                                "type": "Reproducibility",
                                "severity": "Low",
                                "line": call.lineno,
                                "message": f"Model '{class_name}' initialized without 'random_state'."
                            })

    except Exception as e:
        issues.append({
            "type": "Checker Error",
            "severity": "High",
            "line": 0,
            "message": f"Reproducibility checker failed: {str(e)}"
        })
        
    return issues
