# MassaFF Lab

Aplicativo Android experimental para investigar o visual gráfico em blocos ("massinha") no Free Fire, usando Shizuku e opções de renderização ANGLE, sem root.

**Dispositivo de referência:** Samsung Galaxy A06 SM-A065M · Android 16  
**Pacote do aplicativo:** `io.github.astromg01.massaff`  
**Versão inicial:** 0.1.0

## Estado do projeto

Este é um MVP de laboratório. A configuração de ANGLE pode ser solicitada pelo app, mas isso não confirma que o Free Fire oficial carregará ANGLE nem que o backend Vulkan aceitará os filtros experimentais. A compatibilidade precisa ser verificada no dispositivo real e nos logs do sistema.

O projeto não modifica o APK nem os arquivos privados do Free Fire, não injeta bibliotecas, não altera memória ou eventos de toque e não tenta contornar o anti-cheat. Não há promessa de ganho de FPS ou garantia de compatibilidade com as regras do jogo.

## Estrutura da branch

O código-fonte Android está compactado em cinco partes Base64 em `source/`. O workflow remonta o arquivo `MassaFF-Lab-source.tar.xz`, extrai o projeto na raiz do runner, executa os testes unitários e compila o APK de depuração.

A separação em partes é apenas uma forma de transportar o arquivo binário pelo conector GitHub; o workflow reconstrói o arquivo original antes do build. O overlay `source/fixes/ITextureService.aidl` corrige a numeração de transações AIDL da interface Shizuku antes da compilação.

## Gerar APK

1. Abra **Actions → Build MassaFF Lab APK**.
2. Aguarde as etapas de testes e `:app:assembleDebug`.
3. Baixe o artefato **MassaFF-Lab-debug-apk**.
4. Extraia o ZIP e instale `app-debug.apk` para testar.

O artefato é de depuração e não é uma versão de distribuição assinada.

## Teste no Galaxy A06

1. Inicie o Shizuku e conceda a permissão solicitada pelo MassaFF Lab.
2. Verifique se o app reconhece o Free Fire e a identidade ADB do serviço.
3. Feche o Free Fire completamente antes de aplicar ou restaurar configurações do ANGLE.
4. Aplique o perfil experimental e abra o jogo novamente.
5. Leia os logs para confirmar separadamente se ANGLE, Vulkan e as opções de filtragem aparecem.
6. Caso o jogo não carregue corretamente, use **Restaurar** no app e reinicie o jogo.

## Segurança e compatibilidade

As opções avançadas de ANGLE podem ter escopo do sistema e atingir outros aplicativos que usem ANGLE. O app salva as configurações anteriores para permitir restauração, mas o comportamento depende das permissões disponíveis no firmware Samsung e do serviço Shizuku. Não aplique o perfil sem entender que a compatibilidade ainda é experimental.

Consulte `AGENTS.md` e `docs/SESSION_CHECKPOINT.md` no arquivo-fonte para o estado técnico detalhado.
