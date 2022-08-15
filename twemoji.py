#!/usr/bin/env python3

from pathlib import Path
from argparse import ArgumentParser
from json import dump
from os import chdir, system
import sys
import shutil


def error(msg: str):
    print(f'[38;2;255;85;85m{msg}[0m')
    sys.exit(1)


def main():
    parser = ArgumentParser('twemoji-gen')

    parser.add_argument('directory')
    parser.add_argument('--silent', action='store_true', default=False)

    args = parser.parse_args()

    def log(*ag, **kwd):
        if not args.silent:
            print(*ag, **kwd)

    print(args)

    base_dir = Path(args.directory).resolve()
    log(f'Checking if folder "{base_dir}" exists.')
    if not base_dir.exists():
        error(f'error: Path {args.directory} does not exist')

    source_dir = (base_dir / 'emojis').absolute()
    log(f'Checking for folder "{source_dir}"')
    if source_dir.exists():
        error(f'error: Folder named "emoji" exists in "{base_dir.absolute()}"')
    source_dir.mkdir(exist_ok=True)

    log("Creating pack.mcmeta")
    with (source_dir / 'pack.mcmeta').open('w') as f:
        f.write(
            '{"pack":{"pack_format": 9,"description":"Twetmoji in Minecraft"}}'
        )

    log('Creating folder structure')

    assets_dir = (source_dir / 'assets').absolute()
    assets_dir.mkdir()

    mc_dir = (assets_dir / "minecraft").absolute()
    mc_dir.mkdir()

    font_dir = (mc_dir / 'font').absolute()
    font_dir.mkdir()

    textures_dir = (mc_dir / 'textures').absolute()
    textures_dir.mkdir()

    log('Downloading emojis')
    chdir(str(source_dir.absolute()))
    system('git init')
    system('git remote add twemoji https://github.com/twitter/twemoji.git')
    system('git fetch twemoji')
    system('git checkout twemoji/master -- assets/72x72')
    
    font_textures_dir = (textures_dir / 'font').absolute()
    shutil.move(str(assets_dir / "72x72"), str(font_textures_dir))

    log('Creating config file')

    providers = [
        {
            'type': 'bitmap', 'file': f'minecraft:font/{d.name}', 'height': 8, 'ascent': 8, 'chars': [chr(int(d.stem, base=16))]
        } for d in font_textures_dir.iterdir() if d.is_file() and '-' not in str(d.name)
    ]

    config = {'providers': providers}

    with (font_dir / 'default.json').open('w') as f:
        dump(config, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
