import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "resolve_vault.py"


def _write_registry(tmp_path):
    """Baut ein Workspace-Layout mit vaults.json + .env + einer Kopie des Skripts."""
    (tmp_path / "vaults.json").write_text(json.dumps({
        "vaults": {
            "privat": {"path": "${VAULT_PRIVAT}", "default": True},
            "weiterbildung": {"path": "${VAULT_WEITERBILDUNG}"},
            "demo": {"path": "${VAULT_DEMO}"},
        },
        "routing": {"start": "privat", "lernen": "weiterbildung"},
    }))
    privat = tmp_path / "privat"; privat.mkdir()
    weiter = tmp_path / "weiter"; weiter.mkdir()
    (tmp_path / ".env").write_text(
        f"VAULT_PRIVAT={privat}\n"
        f"VAULT_WEITERBILDUNG={weiter}\n"
        f"VAULT_DEMO={tmp_path / 'demo'}\n"  # demo-Ordner existiert bewusst NICHT
    )
    scripts = tmp_path / "scripts"; scripts.mkdir()
    script_copy = scripts / "resolve_vault.py"
    script_copy.write_text(SCRIPT.read_text())
    return script_copy, privat, weiter


def _run(script, *args):
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True)


def test_start_routes_to_privat(tmp_path):
    script, privat, _ = _write_registry(tmp_path)
    r = _run(script, "start")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(privat)


def test_lernen_routes_to_weiterbildung(tmp_path):
    script, _, weiter = _write_registry(tmp_path)
    r = _run(script, "lernen")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(weiter)


def test_vault_override_wins(tmp_path):
    script, _, weiter = _write_registry(tmp_path)
    r = _run(script, "start", "--vault", "weiterbildung")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(weiter)


def test_unknown_route_errors(tmp_path):
    script, *_ = _write_registry(tmp_path)
    r = _run(script, "nichtgeroutet")
    assert r.returncode == 1
    assert "nichtgeroutet" in (r.stderr + r.stdout).lower()


def test_missing_path_errors(tmp_path):
    script, *_ = _write_registry(tmp_path)
    # demo-Slot zeigt auf einen nicht existierenden Ordner -> Fehler
    r = _run(script, "start", "--vault", "demo")
    assert r.returncode == 1
