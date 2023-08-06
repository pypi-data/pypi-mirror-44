cc_library(
    name = "glew",
    srcs = glob([
      "lib/libGL.so.1",
      "lib/x86_64-linux-gnu/libGLEW*.so",
      "lib/x86_64-linux-gnu/libGLU*.so",
      "lib/x86_64-linux-gnu/libGL*.so",
      "lib/x86_64-linux-gnu/libglut*.so",
    ]),
    hdrs = glob([
      "include/GL/*"
    ]),
    includes = ["include"],
    visibility = ["//visibility:public"],
)
