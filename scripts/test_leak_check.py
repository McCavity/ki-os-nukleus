"""Tests für leak_check.py — pytest, wie test_resolve_vault.py.

Die inhaltliche Kalibrierung (welche Muster müssen anschlagen, welche
schweigen) lebt bewußt IM Skript unter `--selftest`: sie soll mitreisen,
wenn jemand die Datei in ein anderes Repo kopiert. Hier stehen die Fälle,
die der Selbsttest nicht erreicht — das VERHALTEN an der Kommandozeile,
und dabei vor allem die Fehlbedienung.
"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent / "leak_check.py"


def _run(*args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, cwd=cwd)


def test_selftest_ist_gruen():
    """Die eingebaute Kalibrierung muß in beiden Richtungen halten."""
    r = _run("--selftest")
    assert r.returncode == 0, r.stdout
    assert "KALIBRIERT" in r.stdout


def test_fund_wird_maskiert_und_nicht_gedruckt(tmp_path):
    """Der Kern des Werkzeugs: es darf den Fund NICHT ins Protokoll holen."""
    geheim = "ghp_ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"  # leakcheck: allow
    f = tmp_path / "x.txt"
    f.write_text(f'token = "{geheim}"\n')
    r = _run(str(f))
    assert r.returncode == 1
    assert geheim not in r.stdout          # <- die eigentliche Zusicherung
    assert "github_token" in r.stdout
    assert "•" in r.stdout


def test_show_gibt_den_wert_frei(tmp_path):
    """--show ist die bewußte Gegenrichtung und muß wirken."""
    geheim = "ghp_ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"  # leakcheck: allow
    f = tmp_path / "x.txt"
    f.write_text(f'token = "{geheim}"\n')
    r = _run(str(f), "--show")
    assert geheim in r.stdout


def test_sauberer_lauf_ist_exit_null(tmp_path):
    f = tmp_path / "ok.md"
    f.write_text("Ein harmloser Satz ohne alles.\n")
    r = _run(str(f))
    assert r.returncode == 0
    assert "nichts gefunden" in r.stdout


# --- Fehlbedienung: hier sitzen die Fehler, die der Selbsttest nicht sieht ---

def test_pfad_mit_tippfehler_bricht_ab(tmp_path):
    """"Nicht gefunden" darf nie "nicht gesucht" bedeuten."""
    r = _run(str(tmp_path / "gibtesnicht.md"))
    assert r.returncode == 2
    assert "existiert nicht" in r.stderr


def test_ohne_argument_kein_freibrief():
    r = _run()
    assert r.returncode == 2


def test_nur_binaerdateien_ist_kein_nullbefund(tmp_path):
    (tmp_path / "bild.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00binary")
    r = _run(str(tmp_path))
    assert r.returncode == 2
    assert "0 Dateien gelesen" in r.stderr


def test_leerer_diff_ist_kein_nullbefund(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    r = _run("--staged", cwd=tmp_path)
    assert r.returncode == 2
    assert "leer" in r.stderr


def test_alarm_entwarnt_wieder(tmp_path):
    """Der Rückweg gehört zur Prüfung: die Regel muß auch schweigen."""
    f = tmp_path / "x.txt"
    f.write_text('token = "ghp_ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"\n')  # leakcheck: allow
    assert _run(str(f)).returncode == 1
    f.write_text("harmlos\n")
    assert _run(str(f)).returncode == 0


def test_allowlist_filtert_wert_nicht_datei(tmp_path):
    """Eine Freistellung darf die Datei nicht als Wachposten verlieren."""
    (tmp_path / ".leakcheckignore").write_text("secret_assignment ^testwert123$\n")  # leakcheck: allow
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    f = tmp_path / "x.txt"
    f.write_text('a_token = "testwert123"\nb_token = "echtgeheim456"\n')  # leakcheck: allow
    r = _run(str(f), cwd=tmp_path)
    assert r.returncode == 1
    assert "1 Fund" in r.stdout          # nur der zweite


def test_inline_marker_schaltet_zeile_stumm(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text('token = "ghp_ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"'  # leakcheck: allow
                 '  # leakcheck: allow github_token\n')
    r = _run(str(f))
    assert "github_token" not in r.stdout


def _run_stdin(text, *args):
    return subprocess.run([sys.executable, str(SCRIPT), "-", *args],
                          input=text, capture_output=True, text=True)


def test_stdin_findet_und_maskiert():
    """Für `gh api ... | base64 -d | leak_check.py -`: das veröffentlichte
    Artefakt prüfen, nicht die lokale Kopie."""
    geheim = "ghp_QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"  # leakcheck: allow
    r = _run_stdin(f'token = "{geheim}"\n')
    assert r.returncode == 1
    assert geheim not in r.stdout
    assert "github_token" in r.stdout


def test_stdin_sauber_ist_exit_null():
    r = _run_stdin("harmlose Zeile\n")
    assert r.returncode == 0


def test_leerer_stdin_ist_kein_nullbefund():
    """Eine leere Pipe darf nie wie ein sauberer Lauf aussehen."""
    r = _run_stdin("")
    assert r.returncode == 2
    assert "leer" in r.stderr
