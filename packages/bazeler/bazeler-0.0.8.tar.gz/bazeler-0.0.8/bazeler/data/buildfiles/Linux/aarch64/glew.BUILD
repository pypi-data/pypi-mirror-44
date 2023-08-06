cc_library(
    name = "glew",
    srcs = glob([
      "lib/libGL.so.1",
      "lib/aarch6464-linux-gnu/libGLEW*.so",
      "lib/aarch6464-linux-gnu/libGLU*.so",
      "lib/aarch6464-linux-gnu/libGL*.so",
      "lib/aarch6464-linux-gnu/libglut*.so",
    ]),
    hdrs = glob([
      "include/GL/*"
    ]),
    includes = ["include"],
    visibility = ["//visibility:public"],
)
