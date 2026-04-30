import os
import subprocess
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ==============================
# CONFIG
# ==============================

MODEL = "gpt-5.3"
OUTPUT_DIR = "generated_output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "generated_backend.md")

SPEC_PRODUCT = "specs/product.spec.md"
SPEC_REQUIREMENTS = "specs/requirements.spec.json"
PROMPT_FILE = "prompts/prompt_initial.md"

# ==============================
# UTILIDADES
# ==============================

def read_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def has_git_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    return bool(result.stdout.strip())

def git_commit(message):
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)

# ==============================
# GENERACIÓN
# ==============================

def generate_code():
    print("🔹 Reading specification files...")

    product_spec = read_file(SPEC_PRODUCT)
    requirements_spec = read_file(SPEC_REQUIREMENTS)
    prompt = read_file(PROMPT_FILE)

    full_prompt = f"""
{prompt}

--- PRODUCT SPEC ---
{product_spec}

--- REQUIREMENTS SPEC ---
{requirements_spec}
"""

    print("🔹 Connecting to OpenAI...")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a senior backend engineer following strict SDD."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    ensure_output_dir()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Code generated at {OUTPUT_FILE}")

# ==============================
# VALIDACIÓN BÁSICA
# ==============================

def validate_output():
    print("🔹 Validating output...")

    if not os.path.exists(OUTPUT_FILE):
        raise Exception("Output file was not generated")

    size = os.path.getsize(OUTPUT_FILE)

    if size < 500:
        raise Exception("Generated output seems too small (possible failure)")

    print("✅ Basic validation passed")

# ==============================
# MAIN
# ==============================

def main():
    try:
        generate_code()
        validate_output()

        if has_git_changes():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"feat(sdd): auto-generated backend from spec [{timestamp}]"
            git_commit(commit_message)
            print("✅ Changes committed to git")
        else:
            print("ℹ️ No changes detected, skipping commit")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()