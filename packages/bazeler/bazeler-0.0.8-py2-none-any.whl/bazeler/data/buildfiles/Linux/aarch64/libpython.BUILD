cc_library(
    name = "libpython",
    srcs = [
        "lib/aarch64-linux-gnu/libpython2.7.so",
        "lib/aarch64-linux-gnu/libpython3.5m.so.1",
    ],
    hdrs = glob([
        "include/python2.7/*.h",
    ]) + glob([
        "local/lib/python2.7/dist-packages/numpy/core/include/numpy/*.h",
    ]),
    includes = [
        "include/python2.7",
        "local/lib/python2.7/dist-packages/numpy/core/include",
    ],
    visibility = ["//visibility:public"],
)
