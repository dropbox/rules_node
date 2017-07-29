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

```python
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

```python
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
