package(default_visibility = ['//visibility:public'])

load('@org_dropbox_rules_node//node:defs.bzl', 'webpack_build')
load('@org_dropbox_rules_node//node:defs.bzl', 'mocha_test')

webpack_build(
    name = 'webpack_build',
    srcs = glob([
        'src/*.ts',
        'tsconfig.json',
    ]),
    outs = ['bundle.js'],
    config = 'webpack.config.js',
    deps = [
        '@org_dropbox_rules_node//node/dbx-bazel-utils',
        '//examples/npm/ts-loader',
        '//examples/npm/typescript',
        '//examples/npm/react',
        '//examples/internal_module',
    ],
)

mocha_test(
    name = 'mocha_test',
    srcs = glob([
        'test/*.spec.js'
    ]),
    deps = [
        '@org_dropbox_rules_node//node/dbx-bazel-utils',
        '//examples/webpack_build'
    ],
)
