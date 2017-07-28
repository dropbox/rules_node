package(default_visibility = ['//visibility:public'])

load('@org_dropbox_rules_node//node:def.bzl', 'node_binary', 'node_library')

node_binary(
    name = 'binary',
    srcs = ['main.js'],
    main = 'main.js',
    deps = [
        ':lib',
        '//examples/internal_module',
    ],
)

node_library(
    name = 'lib',
    srcs = ['lib.js'],
)
