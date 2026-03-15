import sys
from ml_auditor.engine import AuditorEngine

def main():
    # This script expects a file path as an argument
    if len(sys.argv) < 2:
        print("Usage: python pre_commit_hook.py <notebook_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    print(f"Running ML Audit on {file_path}...")
    
    engine = AuditorEngine(file_path)
    results = engine.run_audit() # No LLM for speed in CI/CD
    
    issues = results['issues']
    
    if not issues:
        print("✅ Audit Passed. No critical bugs found.")
        sys.exit(0) # Success exit code
    else:
        print(f"❌ Audit Failed. Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"- [{issue['severity']}] Line {issue['line']}: {issue['message']}")
        sys.exit(1) # Failure exit code (blocks the commit if configured)

if __name__ == "__main__":
    main()
    