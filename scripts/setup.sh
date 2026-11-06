#!/usr/bin/env bash
# GemHub Motion Studio — установка для macOS и Linux
# bash scripts/setup.sh [--check] [--extra]
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
has(){ command -v "$1" >/dev/null 2>&1; }
step(){ printf '\n== %s\n' "$1"; }
CORE="heygen-com/hyperframes remotion-dev/skills AbubakrChan/product-launch-motion greensock/gsap-skills emilkowalski/skills"
MORE="pbakaus/impeccable nextlevelbuilder/ui-ux-pro-max-skill"
CHECK=0; EXTRA=0; for a in "$@"; do [ "$a" = --check ] && CHECK=1; [ "$a" = --extra ] && EXTRA=1; done

step 'Проверка'
for c in python3 node npx git ffmpeg; do has $c && echo "  есть: $c" || echo "  нет:  $c"; done
python3 -c "import playwright, faster_whisper, numpy, scipy, PIL; print('  Python-пакеты: есть')" 2>/dev/null || echo '  Python-пакеты: не все'
[ -d "$HOME/Developer/video-use" ] && echo '  video-use: есть' || echo '  video-use: нет'
[ $CHECK = 1 ] && exit 0

step 'Программы'
if has brew; then for p in python node git ffmpeg; do brew list $p >/dev/null 2>&1 || brew install $p; done
elif has apt-get; then sudo apt-get update && sudo apt-get install -y python3 python3-pip nodejs npm git ffmpeg
else echo '  Поставьте python3, node, git, ffmpeg вручную'; fi

step 'Python-пакеты и браузер'
python3 -m pip install --upgrade pip
python3 -m pip install playwright faster-whisper numpy scipy pillow
python3 -m playwright install chromium

step 'video-use'
VU="$HOME/Developer/video-use"
[ -d "$VU" ] || { mkdir -p "$HOME/Developer"; git clone https://github.com/browser-use/video-use "$VU"; }
(cd "$VU" && python3 -m pip install -e .)
[ -f "$VU/.env" ] || echo 'ELEVENLABS_API_KEY=' > "$VU/.env"

step 'Скиллы'
LIST="$CORE"; [ $EXTRA = 1 ] && LIST="$LIST $MORE"
for r in $LIST "$VU"; do npx --yes skills add "$r" -g -a '*' --skill '*' -y; done

date > "$ROOT/.installed"
echo "Готово. Ключ ElevenLabs впишите в $VU/.env и в .env проекта. В чат ключи не отправляйте."
