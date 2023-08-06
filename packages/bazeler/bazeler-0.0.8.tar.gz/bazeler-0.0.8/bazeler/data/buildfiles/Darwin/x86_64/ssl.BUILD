cc_library(
  name = "ssl",
  srcs = glob([
    "opt/openssl/lib/*.dylib",
  ]),
  hdrs = glob([
    "opt/openssl/include/openssl/**/*.h",
  ]),
  includes = [
    "opt/openssl/include"
  ],
  visibility = ["//visibility:public"],
)
