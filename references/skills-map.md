# Карта скиллов

Все ставятся скриптом установки. Вручную: `npx skills add <репозиторий> -g -a '*' -y` (`-a '*'` — для всех агентов: Claude Code, Codex и др.).

## Ядро (ставится всегда)

| Репозиторий | Скиллы | Когда брать |
|---|---|---|
| `heygen-com/hyperframes` | hyperframes, hyperframes-cli, hyperframes-registry, media-use | HTML → видео; ~450 готовых блоков: переходы, титры, кинетический текст, субтитры, графики, 3D, движения камеры. media-use: музыка, звуки, голос, картинки, цвет |
| `remotion-dev/skills` | remotion-best-practices, remotion-create, remotion-render, remotion-captions, remotion-multimedia, remotion-studio и др. | Видео на React, серии по шаблону и данным, субтитры |
| `AbubakrChan/product-launch-motion` | product-launch-motion | Режиссура launch-роликов: один объект, пружины, курсор, удары под музыку |
| `greensock/gsap-skills` | gsap-core, gsap-timeline, gsap-plugins, gsap-utils и др. | Сложные таймлайны и последовательности |
| `emilkowalski/skills` | animate, animation-vocabulary, emil-design-eng, review-animations, improve-animations, apple-design и др. | Качество движения; словарь названий эффектов для промптов |
| `browser-use/video-use` | video-use | Монтаж съёмки разговором: расшифровка, нарезка, субтитры, цвет, оверлеи |

## Дополнительно (флаг `-Extra` / `--extra`)

| Репозиторий | Скиллы | Когда брать |
|---|---|---|
| `pbakaus/impeccable` | impeccable | Полировка вёрстки кадров, иерархия, типографика |
| `nextlevelbuilder/ui-ux-pro-max-skill` | ui-ux-pro-max, design, banner-design, brand, design-system, slides | Палитры, пары шрифтов, баннеры и обложки к роликам |

## Решающее правило

1. Есть готовый блок под нужный эффект в `hyperframes-registry` → бери блок, не пиши с нуля.
2. Ролик-история с одним героем и интерфейсом → `product-launch-motion` или наш шаблон.
3. Нужно 10+ роликов по одному шаблону с разными данными → Remotion.
4. Есть живая съёмка → video-use, а моушн-вставки рендерить отдельно и вклеивать.
5. Не можешь назвать эффект из референса → `animation-vocabulary`.
