from openai import OpenAI

class LocalKnowledgeBase:
    """
    Smarter Offline Knowledge Base.
    Merges Smart Context Checks with Fix/Solve logic.
    """
    def __init__(self):
        self.definitions = {
            "leakage": "Data Leakage happens when information from outside the training dataset is used to create the model. A common example is fitting a StandardScaler on the entire dataset before splitting.",
            "overfitting": "Overfitting occurs when a model learns the training data too well, including noise. It performs well on training data but poorly on new data. Try Cross-Validation or Regularization.",
            "accuracy": "Accuracy is often misleading for imbalanced datasets. If your data is 90% class A, a model guessing 'A' every time is 90% accurate but useless. Use F1-Score or AUC instead.",
            "reproducibility": "Reproducibility ensures others can recreate your results. Always set a `random_state` (seed) for your splits and models.",
            "imbalanced": "For imbalanced data, accuracy is misleading. Use F1-score, Precision, Recall, or AUC-ROC.",
            "split": "Random splitting on time-series data causes leakage. Use Time-Based splitting instead.",
            "validation": "A validation set is used to tune hyperparameters. You should have Train, Validation, and Test sets to avoid overfitting."
        }

    def get_response(self, query, audit_results=None, has_code=False):
        query = query.lower()
        
        # --- 1. CHECK FOR FIX/SOLVE REQUESTS ---
        if "fix" in query or "solve" in query or "correct" in query or "rewrite" in query:
            if audit_results and audit_results.get('issues'):
                issues = audit_results['issues']
                response = "🛠️ **Offline Fix Instructions:**\n\nI found issues in your code. Here is how to fix them manually:\n\n"
                
                found_issues = False
                for i in issues:
                    issue_type = i.get('type')
                    line = i.get('line')
                    found_issues = True
                    
                    if issue_type == "Data Leakage":
                        response += f"1. **Data Leakage (Line {line})**: Move the `fit` or `fit_transform` call to happen **after** `train_test_split`. You must only fit on `X_train`.\n"
                    elif issue_type == "Reproducibility":
                        response += f"2. **Reproducibility (Line {line})**: Add `random_state=42` to the parameters of the function.\n"
                    elif issue_type == "Metric Misuse":
                        response += f"3. **Metric Misuse (Line {line})**: Replace `accuracy_score` with `f1_score` or `classification_report`.\n"
                    else:
                        response += f"- Issue on line {line}: {i.get('message')}\n"
                
                if not found_issues:
                    response += "No critical issues found that require fixing."
                
                response += "\n\n*Tip: Add an OpenAI API Key in the sidebar to let AI rewrite the code for you automatically.*"
                return response
            else:
                return "⚠️ I didn't find any issues to fix. Either your code is clean, or you haven't run the **Audit** yet."

        # --- 2. CHECK FOR SUMMARY REQUESTS ---
        # Comprehensive list of triggers
        summary_triggers = ["summary", "result", "issues", "found", "error", "problem", "report", "bugs", "list", "audit"]
        
        if any(word in query for word in summary_triggers):
            if audit_results:
                issues_list = audit_results.get('issues', [])
                if not issues_list:
                    return "✅ **Audit Complete**: I scanned your code and found no critical issues."
                else:
                    summary = []
                    for i in issues_list:
                        issue_type = i.get('type', 'Unknown')
                        line = i.get('line', 'N/A')
                        msg = i.get('message', 'No details')
                        summary.append(f"- **{issue_type}** (Line {line}): {msg}")
                    return f"📊 **Audit Summary**: I found {len(issues_list)} issue(s):\n" + "\n".join(summary)
            else:
                return "⚠️ **No Audit Data**: Please go to the **Auditor Tool** and click **Run Audit**."

        # --- 3. CONTEXT CHECK (Is there leakage in my code?) ---
        # Smart Detection: If user asks about a topic, check if WE FOUND IT in their code first.
        if audit_results and audit_results.get('issues'):
            issues = audit_results['issues']
            
            # Map keywords to Issue Types
            # Example: If user says "leakage", look for "Data Leakage" issues.
            issue_checks = {
                "leakage": "Data Leakage",
                "metric": "Metric Misuse",
                "accuracy": "Metric Misuse",
                "reproducibility": "Reproducibility",
                "seed": "Reproducibility"
            }

            for key, issue_type in issue_checks.items():
                if key in query:
                    # Filter issues that match this type
                    found_issues = [i for i in issues if i.get('type') == issue_type]
                    
                    if found_issues:
                        response = f"🔍 **Good news!** I actually found **{len(found_issues)} {issue_type}** issue(s) in your uploaded code:\n\n"
                        for i in found_issues:
                            response += f"- Line {i.get('line', 'N/A')}: {i.get('message', '')}\n"
                        response += f"\n**Definition:** {self.definitions.get(key, '')}"
                        return response
                    else:
                        # If keyword matches but no bug found, clarify that.
                        return f"I scanned your code and did **not** find any **{issue_type}** issues.\n\n**Definition:** {self.definitions.get(key, '')}"

        # --- 4. GENERAL KNOWLEDGE BASE ---
        # If no context found, just return the definition
        for key, definition in self.definitions.items():
            if key in query:
                return definition

        # --- 5. FALLBACK ---
        if audit_results:
            return "🤖 I didn't quite understand. You can ask for a **summary**, ask how to **fix**, or ask about concepts like **leakage** or **overfitting**."
        
        return "🤖 I am in Offline Mode. I can answer questions about **Leakage**, **Metrics**, **Reproducibility**, or **Fixes**."

def chat_with_assistant(query, code_context, api_key, audit_results=None):
    """
    Routes the chat query.
    """
    
    # CASE 1: No API Key -> Use Local Knowledge Base
    if not api_key:
        local_brain = LocalKnowledgeBase()
        return local_brain.get_response(query, audit_results, has_code=bool(code_context))

    # CASE 2: API Key Provided -> Use OpenAI
    try:
        client = OpenAI(api_key=api_key)
        
        system_prompt = f"""
        You are an expert ML Code Fixer. The user has uploaded a code file.
        Here is the content:
        --------------------
        {code_context}
        --------------------
        If the user asks to 'fix' or 'solve', rewrite the code with the corrections applied.
        Provide the code in a markdown block.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg:
            return "⚠️ **API Quota Exceeded**: Remove the API Key to use **Offline Mode** (which gives text instructions)."
        else:
            return f"AI Error: {error_msg}"
        