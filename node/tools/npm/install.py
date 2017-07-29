# Install a set of npm modules.
#
# This file installs the npm modules directly from the public npm
# registry. Ideally, you should be using your own installer that pulls
# from an internal mirror of npm.

import argparse
import os
import shutil
from tempfile import mkdtemp

from node.tools.npm.utils import (
    run_npm,
    SHRINKWRAP,
)

def npm_install(shrinkwrap_path, output):
    shutil.copyfile(shrinkwrap_path, os.path.join(output, SHRINKWRAP))

    tmpdir = mkdtemp(suffix='npm_install')
    env = {
        # Change the npm cache to a tmp directory so that this can run
        # sandboxed.
        'NPM_CONFIG_CACHE': os.path.join(tmpdir, '.npm'),
    }

    run_npm(['install'], env=env, cwd=output)

    shutil.rmtree(tmpdir)


def main():
    parser = argparse.ArgumentParser(
        description="Install npm modules",
    )
    parser.add_argument("shrinkwrap",
                        help="Path to npm-shrinkwrap.json",
                        type=str)
    parser.add_argument("output",
                        help="Directory that you want to install into.",
                        type=str)

    args = parser.parse_args()

    npm_install(args.shrinkwrap, args.output)


if __name__ == '__main__':
    main()
