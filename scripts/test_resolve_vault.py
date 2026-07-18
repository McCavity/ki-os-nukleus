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
            "zweitvault": {"path": "${VAULT_ZWEIT}"},
            "demo": {"path": "${VAULT_DEMO}"},
        },
        "routing": {"start": "privat", "zweit": "zweitvault"},
    }))
    privat = tmp_path / "privat"; privat.mkdir()
    zweit = tmp_path / "zweit"; zweit.mkdir()
    (tmp_path / ".env").write_text(
        f"VAULT_PRIVAT={privat}\n"
        f"VAULT_ZWEIT={zweit}\n"
        f"VAULT_DEMO={tmp_path / 'demo'}\n"  # demo-Ordner existiert bewusst NICHT
    )
    scripts = tmp_path / "scripts"; scripts.mkdir()
    script_copy = scripts / "resolve_vault.py"
    script_copy.write_text(SCRIPT.read_text())
    return script_copy, privat, zweit


def _run(script, *args):
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True)


def test_start_routes_to_privat(tmp_path):
    script, privat, _ = _write_registry(tmp_path)
    r = _run(script, "start")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(privat)


def test_zweit_routes_to_zweitvault(tmp_path):
    script, _, zweit = _write_registry(tmp_path)
    r = _run(script, "zweit")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(zweit)


def test_vault_override_wins(tmp_path):
    script, _, zweit = _write_registry(tmp_path)
    r = _run(script, "start", "--vault", "zweitvault")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(zweit)


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


def test_env_value_double_quoted(tmp_path):
    """VAULT_PRIVAT="/pfad" muss trotz Anführungszeichen aufgelöst werden."""
    script, privat, zweit = _write_registry(tmp_path)
    (tmp_path / ".env").write_text(
        f'VAULT_PRIVAT="{privat}"\n'
        f"VAULT_ZWEIT={zweit}\n"
        f"VAULT_DEMO={tmp_path / 'demo'}\n"
    )
    r = _run(script, "start")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(privat)


def test_env_value_single_quoted(tmp_path):
    """VAULT_PRIVAT='/pfad' muss trotz Anführungszeichen aufgelöst werden."""
    script, privat, zweit = _write_registry(tmp_path)
    (tmp_path / ".env").write_text(
        f"VAULT_PRIVAT='{privat}'\n"
        f"VAULT_ZWEIT={zweit}\n"
        f"VAULT_DEMO={tmp_path / 'demo'}\n"
    )
    r = _run(script, "start")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(privat)


def test_env_value_trailing_comment_stripped(tmp_path):
    """VAULT_PRIVAT=/pfad  # Kommentar darf den Pfad nicht verlängern."""
    script, privat, zweit = _write_registry(tmp_path)
    (tmp_path / ".env").write_text(
        f"VAULT_PRIVAT={privat}  # mein Vault\n"
        f"VAULT_ZWEIT={zweit}\n"
        f"VAULT_DEMO={tmp_path / 'demo'}\n"
    )
    r = _run(script, "start")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(privat)


def test_env_value_hash_in_quoted_path_not_truncated(tmp_path):
    """Gegenprobe: ein '#' INNERHALB des Pfads (gequotet) ist Teil des Werts, kein Kommentar."""
    script, _, zweit = _write_registry(tmp_path)
    hashed = tmp_path / "vault#privat"
    hashed.mkdir()
    (tmp_path / ".env").write_text(
        f'VAULT_PRIVAT="{hashed}"\n'
        f"VAULT_ZWEIT={zweit}\n"
        f"VAULT_DEMO={tmp_path / 'demo'}\n"
    )
    r = _run(script, "start")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(hashed)
