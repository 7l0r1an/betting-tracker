# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['business', 'business.type_analyzer', 'business.weekly_summary', 'business.tracker', 'business.accumulator_tracker', 'business.bank_manager', 'business.stats_analyzer', 'business.predictor', 'business.chart', 'business.calculator', 'repository', 'repository.file_repo', 'repository.accumulator_repo', 'repository.bank_repo', 'repository.api_repo', 'domain', 'domain.bet', 'domain.accumulator'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BettingTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
