#!/usr/bin/env python3
"""MassaFF Lab 0.2.1: exact restore UX and temporary compatibility hold."""
from pathlib import Path

ROOT = Path('.')

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: esperado exatamente 1 trecho, encontrado {count}')
    return text.replace(old, new, 1)

activity_path = ROOT / 'app/src/main/java/io/github/astromg01/massaff/MainActivity.kt'
activity = activity_path.read_text(encoding='utf-8')
activity = replace_once(activity,
    '                        Text("Restaurar configurações anteriores")',
    '                        Text("URGENTE: RESTAURAR ORIGINAL / DESATIVAR MASSINHA")',
    'rótulo de restauração')
activity = replace_once(activity,
    '                    Text("O filtro forceNearestFiltering e o nível LOD são recursos do ANGLE/Vulkan. Se o aparelho não usar esse backend no jogo, o visual não muda.", color = Color(0xFF9EAAA2), style = MaterialTheme.typography.bodySmall)',
    '                    Text("RECUPERAÇÃO: este botão restaura exatamente o backup anterior à massinha, incluindo seleção ANGLE e filtros globais. Até a compatibilidade ser confirmada, mantenha o perfil desativado e não o use em partidas competitivas.", color = Color(0xFFFFC36B), style = MaterialTheme.typography.bodySmall)\n                    Text("O efeito depende de ANGLE/Vulkan e pode causar incompatibilidade ou stutter. Nenhum bypass de matchmaking faz parte do app.", color = Color(0xFF9EAAA2), style = MaterialTheme.typography.bodySmall)',
    'aviso de recuperação')
activity = replace_once(activity,
    'Feche completamente o Free Fire antes de aplicar. Os filtros ANGLE são propriedades globais e podem afetar outros apps que usem ANGLE. O app salva um backup para restauração. Depois, reabra o jogo e confira os logs. Se houver stutter ou falha gráfica, volte para Equilibrado ou restaure.',
    'Feche completamente o Free Fire antes de aplicar. Os filtros ANGLE são propriedades globais e podem afetar outros apps. A compatibilidade com o matchmaking do Free Fire ainda não foi confirmada: não use em partidas competitivas. O app salva um backup para restauração. Reaplique somente em teste controlado.',
    'aviso antes de aplicar')
activity = replace_once(activity,
    'Configurações originais restauradas e verificadas. Reabra o jogo para confirmar o visual normal.',
    'Configurações originais restauradas e verificadas. A massinha foi desativada; feche completamente o Free Fire antes de testar novamente.',
    'mensagem pós-restauração')
activity = activity.replace('Text("0.2.0", color = Color(0xFF92A196)', 'Text("0.2.1", color = Color(0xFF92A196)', 1)
activity = replace_once(activity,
    '    val scroll = rememberScrollState()\n    Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFF090C0B)) {',
    '    val compatibilityHold = true // Keep ANGLE profile application paused until matchmaking compatibility is verified.\n    val scroll = rememberScrollState()\n    Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFF090C0B)) {',
    'bloqueio temporário de aplicação')
activity = replace_once(activity,
    'enabled = serviceReady && selectedGamePackage != null && !isWorking, modifier = Modifier.fillMaxWidth()) {\n                        Text("Aplicar gráfico de massinha")',
    'enabled = serviceReady && selectedGamePackage != null && !isWorking && !compatibilityHold, modifier = Modifier.fillMaxWidth()) {\n                        Text(if (compatibilityHold) "PERFIL PAUSADO • compatibilidade em revisão" else "Aplicar gráfico de massinha")',
    'botão de aplicação pausado')
activity_path.write_text(activity, encoding='utf-8')

gradle_path = ROOT / 'app/build.gradle.kts'
gradle = gradle_path.read_text(encoding='utf-8')
gradle = replace_once(gradle, 'versionCode = 2', 'versionCode = 3', 'versionCode')
gradle = replace_once(gradle, 'versionName = "0.2.0"', 'versionName = "0.2.1"', 'versionName')
gradle_path.write_text(gradle, encoding='utf-8')

readme_path = ROOT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
readme = replace_once(readme, '## Versão 0.2.0 — foco em fluidez e estabilidade', '## Versão 0.2.1 — restauração e compatibilidade', 'título README')
readme = replace_once(readme,
    '7. Se houver falha gráfica, stutter forte ou instabilidade, volte ao Equilibrado ou use **Restaurar configurações anteriores**.',
    '7. A aplicação da massinha fica temporariamente pausada até a compatibilidade com matchmaking ser validada. Se houver qualquer incompatibilidade, use **URGENTE: RESTAURAR ORIGINAL / DESATIVAR MASSINHA**. A ação restaura exatamente o snapshot prévio. Não reaplique em partidas competitivas.',
    'passo recuperação README')
readme_path.write_text(readme, encoding='utf-8')

checkpoint_path = ROOT / 'docs/SESSION_CHECKPOINT.md'
checkpoint = checkpoint_path.read_text(encoding='utf-8')
checkpoint = replace_once(checkpoint, '# Session checkpoint — MassaFF Lab 0.2.0', '# Session checkpoint — MassaFF Lab 0.2.1', 'título checkpoint')
checkpoint += '\n\n## 0.2.1 compatibility response\n- The user reported solo matchmaking that appeared to contain emulator players/cheaters after enabling the ANGLE profile. Treat this as a serious compatibility regression, without inferring player skill or claiming the exact server-side cause.\n- The app highlights the exact-snapshot restore action and temporarily blocks new profile application until compatibility is verified.\n- Restore uses the pre-profile snapshot for both ANGLE package selection and global feature properties, then verifies the restored values.\n- Do not implement emulator identity spoofing or anti-cheat/matchmaking bypass.\n- Reproduce only in controlled tests; separately isolate per-package ANGLE selection from global feature overrides before re-enabling the clay profile.\n'
checkpoint_path.write_text(checkpoint, encoding='utf-8')

print('Patch 0.2.1 aplicado: restauração exata destacada e aplicação ANGLE temporariamente pausada.')
