#!/usr/bin/env python3
"""Convert MassaFF Lab's forced-native action into an exact pre-profile restore."""
from pathlib import Path

ROOT = Path('.')

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: esperado exatamente 1 trecho, encontrado {count}')
    return text.replace(old, new, 1)

service_path = ROOT / 'app/src/main/java/io/github/astromg01/massaff/service/TextureUserService.java'
service = service_path.read_text(encoding='utf-8')
start_marker = '    /**\n     * Disable the experimental clay profile'
end_marker = '    @Override\n    public String restoreState(String snapshotJson) {'
start = service.find(start_marker)
end = service.find(end_marker, start + len(start_marker))
if start < 0 or end < 0:
    raise SystemExit('Não foi possível localizar o método de compatibilidade para remover.')
service = service[:start] + service[end:]
service_path.write_text(service, encoding='utf-8')

aidl_path = ROOT / 'app/src/main/aidl/io/github/astromg01/massaff/service/ITextureService.aidl'
aidl = aidl_path.read_text(encoding='utf-8')
aidl = aidl.replace('    String setNativeCompatibilityMode(String gamePackage, String snapshotJson) = 8;\n', '')
aidl_path.write_text(aidl, encoding='utf-8')

activity_path = ROOT / 'app/src/main/java/io/github/astromg01/massaff/MainActivity.kt'
activity = activity_path.read_text(encoding='utf-8')
activity = replace_once(activity, '                    onNativeCompatibility = ::useNativeCompatibilityMode,\n', '', 'callback nativo')
activity = replace_once(activity, '    onNativeCompatibility: () -> Unit,\n', '', 'parâmetro UI nativo')
start_marker = '    private fun useNativeCompatibilityMode() {'
end_marker = '    private fun readAngleLogs() {'
start = activity.find(start_marker)
end = activity.find(end_marker, start + len(start_marker))
if start < 0 or end < 0:
    raise SystemExit('Não foi possível localizar a função de modo nativo para remover.')
activity = activity[:start] + activity[end:]

native_button = '''                    OutlinedButton(onClick = onNativeCompatibility, enabled = serviceReady && hasBackup && !isWorking, modifier = Modifier.fillMaxWidth()) {
                        Text("Desativar massinha • usar driver nativo")
                    }
'''
activity = replace_once(activity, native_button, '', 'botão que forçava driver nativo')
activity = replace_once(activity,
    '                        Text("Restaurar estado original completo")',
    '                        Text("RESTAURAR: desativar perfil e voltar ao original")',
    'rótulo de restauração')
old_warning = '                    Text("Compatibilidade nativa desliga o efeito de massinha, restaura as propriedades globais ANGLE anteriores e seleciona o driver GLES nativo apenas para o Free Fire. Não é bypass de emulador nem garantia sobre filas de matchmaking.", color = Color(0xFFFFC36B), style = MaterialTheme.typography.bodySmall)'
new_warning = '                    Text("RECUPERAÇÃO: restaura exatamente o backup salvo antes do perfil, remove as alterações experimentais e não força outro driver. Mantenha o perfil desativado enquanto testa a compatibilidade do jogo.", color = Color(0xFFFFC36B), style = MaterialTheme.typography.bodySmall)'
activity = replace_once(activity, old_warning, new_warning, 'aviso de compatibilidade')
activity = activity.replace('Text("0.2.1", color = Color(0xFF92A196)', 'Text("0.2.2", color = Color(0xFF92A196)', 1)
activity_path.write_text(activity, encoding='utf-8')

gradle_path = ROOT / 'app/build.gradle.kts'
gradle = gradle_path.read_text(encoding='utf-8')
gradle = replace_once(gradle, 'versionName = "0.2.1"', 'versionName = "0.2.2"', 'versionName')
gradle_path.write_text(gradle, encoding='utf-8')

print('Patch 0.2.2 aplicado: restaura o snapshot exato e remove a seleção forçada de driver.')
