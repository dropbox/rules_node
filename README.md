# Node Rules for Bazel

Rules | Description
--- | ---
[node_binary] | Creates a node binary.
[node_library] | Groups node.js sources and deps together.
[npm_library] | Defines an external npm module.
[node_internal_module] | Create an internal node module that can be required as `require('module_name')`.
[node_build] | Build JS/CSS/etc with a node binary.
[webpack_binary] | Build JS/CSS/etc with webpack.
[node_test] | Defines a basic node test.
[mocha_test] | Defines a node test that uses mocha.
[node_repositories] | External dependencies

## Setup

First you must [install][bazel-install] Bazel.

### Linux

For Linux, you must add the following to your `WORKSPACE` file:

```bzl
git_repository(
    name = "org_dropbox_rules_node",
    remote = "https://github.com/dropbox/rules_node.git",
    commit = "{HEAD}",
)

load("@org_dropbox_rules_node//node:defs.bzl", "node_repositories")

node_repositories()
```

This will pull in node v6.11.1 built for linux-x64. If you want to use
another version of node, you should pass `omit_nodejs=True` and define
another version of `nodejs` in your `WORKSPACE` file.

### macOS

NOTE: These rules have only been tested on Linux.

For macOS, you must add the following to your `WORKSPACE` file:

```bzl
git_repository(
    name = "org_dropbox_rules_node",
    remote = "https://github.com/dropbox/rules_node.git",
    commit = "{HEAD}",
)

load("@org_dropbox_rules_node//node:defs.bzl", "node_repositories", "NODEJS_BUILD_FILE_CONTENT")

node_repositories(omit_nodejs=True)

new_http_archive(
    name = "nodejs",
    url = "https://nodejs.org/dist/v6.11.1/node-v6.11.1-darwin-x64.tar.gz",
    strip_prefix = "node-v6.11.1-darwin-x64",
    sha256 = "a2b839259089ef26f20c17864ff5ce9cd1a67e841be3d129b38d288b45fe375b",
    build_file_content = NODEJS_BUILD_FILE_CONTENT,
)
```

This will pull in node v6.11.1 built for macOS.

# Rules

## `node_binary`

```bzl
load("@org_dropbox_rules_node//node:defs.bzl", "node_library")
node_binary(name, main, srcs, deps, data, extra_args, node, max_old_memory, expose_gc)
```

Creates a node binary, which is an executable Node program consisting
of a collection of `.js` source files.

Node binaries are created using `--preserve-symlinks`.

One quirk of this rule is that if your script uses the pattern:

```javascript
  if (require.main === module) {
```

to only execute something if the node script is the "main" script,
you'll need to modify it to check `BAZEL_NODE_MAIN_ID` against the
module id instead, like this:

```javascript
  if (process.env['BAZEL_NODE_MAIN_ID'] === module.id || require.main === module) {
```

All node modules that this rule depends on, direct and transitive, end
up flattened in `{package-directory}/node_modules`, where
`package-directory` is the directory that the node_binary target
is it. This means that, across all of your transitive dependencies
tracked by Bazel, you can't depend on different versions of the same
node module. (This does not apply to transitive dependencies of
npm_library rules, which are not tracked by Bazel.)

The environmental variable `NODE_PATH` is set to
`{package-directory}/node_modules` so that all the files that end up
running can find all the included node modules.

One side-effect of that is that node libraries have access to all the
transitive dependencies for the node binary that depends on them.

Examples:

```bzl
node_binary(
    name = 'mybin',
    srcs = [
        'mybin.js',
    ],
    main = 'mybin.js',
    deps = [
        '//npm/loose-envify',
        '//npm/minimist',
        '//npm/mkdirp',
    ],
)
```

```bzl
node_library(
    name = 'lib',
    srcs = ['lib.js'],
    deps = [
        '//npm/mkdirp',
    ],
)

node_binary(
    name = 'bin',
    srcs = ['bin.js'],
    deps = [
        ':lib',
    ],
)
```

### Arguments

 - **name:** ([Name]; required) A unique name for this rule.

 - **main:** ([Label]; required) The name of the source file that is the main entry point of the
    application.

 - **srcs:** (List of [labels]; optional) The list of source files that are processed to create the target.

 - **deps:** (List of [labels]; optional) The list of other libraries included in the binary target.

 - **data:** (List of [labels]; optional) The list of files needed by this binary at runtime.

 - **extra_args:** (List of strings; optional) Command line arguments that bazel will pass to the target when it
    is executed either by the `run` command or as a test. These arguments
    are passed before the ones that are specified on the `bazel run` or
    `bazel test` command line.

 - **node:** ([Label]; defaults to `@nodejs//:node`) The node binary used to run the binary. Must be greater than 6.2.0.

 - **max_old_memory:** (Integer; optional) Node, by default, doesn't run its garbage collector on old space
    until a maximum old space size limit is reached. This overrides the default (of around 1.4gb)
    with the provided value in MB.

 - **expose_gc:** (Boolean; optional) Expose `global.gc()` in the node process to allow manual requests for
    garbage collection.

## `node_library`

Groups node.js sources and deps together. Similar to [py_library] and [java_library] rules.

**NOTE:** This does not create an internal module that you can then `require`. For that, you need to use [node_internal_module].

### Arguments

 - **srcs:** (List of [labels]; optional) The list of source files that are processed to create the target.

 - **deps:** (List of [labels]; optional) The list of other libraries or node modules needed to be linked into
    the target library.

 - **data:** (List of [labels]; optional) The list of files needed by this library at runtime.



[Name]: http://bazel.io/docs/build-ref.html#name
[labels]: http://bazel.io/docs/build-ref.html#labels
[Label]: http://bazel.io/docs/build-ref.html#labels
[bazel-install]: https://docs.bazel.build/versions/master/install.html
[node_binary]: #node_binary
[node_library]: #node_library
[npm_library]: #npm_library
[node_internal_module]: #node_internal_module
[node_build]: #node_build
[webpack_binary]: #webpack_binary
[node_test]: #node_test
[mocha_test]: #mocha_test
[node_repositories]: #node_repositories
