package(default_visibility = ['//visibility:public'])

load('@org_dropbox_rules_node//node:defs.bzl', 'webpack_binary')

webpack_binary(
    name = 'webpack_build',
    srcs = glob([
        'src/*.ts',
        'tsconfig.json',
    ]),
    outs = ['bundle.js'],
    config = 'webpack.config.js',
    deps = [
        '@org_dropbox_rules_node//node/dbxBazelUtils',
        '//examples/npm/ts-loader',
        '//examples/npm/typescript',
    ],
)
