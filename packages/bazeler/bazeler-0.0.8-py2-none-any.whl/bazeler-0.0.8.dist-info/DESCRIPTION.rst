# Bazel helper

Repositories are defined by the `required.json` and `provides.json` sentinel
files in each repository. For example, in `common/Sophus`:

```
{
  "dependencies": [
    "eigen"
  ]
}
```

This requires the `eigen` dependency, which means either: 

* A repository exists in the parent directory that contains a `provides.json`
  file, or:
* A buildfile exists for the given architecture (for natively installed
  libraries)

This is designed to be used in conjunction with Google's git-repo:
[git-repo](https://code.google.com/archive/p/git-repo/)


