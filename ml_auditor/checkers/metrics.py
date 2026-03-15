import astroid

def check_metrics(code_content):
    """
    Checks for use of accuracy_score.
    """
    issues = []
    try:
        tree = astroid.parse(code_content)
        
        for node in tree.body:
            for call in node.nodes_of_class(astroid.nodes.Call):
                if isinstance(call.func, astroid.nodes.Name) and call.func.name == 'accuracy_score':
                    issues.append({
                        "type": "Metric Misuse",
                        "severity": "High",
                        "line": call.lineno,
                        "message": "Metric Warning: 'accuracy_score' used. Ensure dataset is balanced. If imbalanced, use F1-score."
                    })
                    
    except Exception as e:
         issues.append({
            "type": "Checker Error",
            "severity": "High",
            "line": 0,
            "message": f"Metrics checker failed: {str(e)}"
        })
    return issues
