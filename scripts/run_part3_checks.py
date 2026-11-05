"""Run Part 3 checks and regenerate reports without starting a server or pushing."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ['coverage','run','-m','pytest','-q','--junitxml=docs/reports/evidence/junit.xml'],
    ['coverage','json','-o','docs/reports/evidence/coverage-data.json'],
    ['coverage','xml','-o','docs/reports/evidence/cobertura.xml'],
    ['coverage','html'],
]

if __name__ == '__main__':
    for command in COMMANDS:
        subprocess.run([sys.executable,'-m',*command],cwd=ROOT,check=True)
    # Coverage normally ignores its HTML assets; coursework evidence must be shareable.
    (ROOT/'docs/reports/evidence/coverage-html/.gitignore').write_text(
        '# Include generated coverage evidence in the course submission.\n!*\n', encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_test_reports.py')],cwd=ROOT,check=True)
    print('Reports regenerated in docs/reports; manual acceptance remains a separate team task.')
