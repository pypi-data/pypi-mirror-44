cc_library(
    name = "Sophus",
    hdrs = glob([
        "**/*.hpp",
    ]),
    includes = ["Sophus"],
    visibility = ["//visibility:public"],
    deps = [
        "@eigen",
    ],
)

cc_library(
    name = "tests",
    hdrs = [
        "Sophus/test/core/tests.hpp",
    ],
    deps = [
        ":Sophus",
    ],
)

cc_binary(
    name = "test_se3",
    srcs = ["Sophus/test/core/test_se3.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_se2",
    srcs = ["Sophus/test/core/test_se2.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_common",
    srcs = ["Sophus/test/core/test_common.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_geometry",
    srcs = ["Sophus/test/core/test_geometry.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_rxso2",
    srcs = ["Sophus/test/core/test_rxso2.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_rxso3",
    srcs = ["Sophus/test/core/test_rxso3.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_sim2",
    srcs = ["Sophus/test/core/test_sim2.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_sim3",
    srcs = ["Sophus/test/core/test_sim3.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_so2",
    srcs = ["Sophus/test/core/test_so2.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_so3",
    srcs = ["Sophus/test/core/test_so3.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

cc_binary(
    name = "test_velocities",
    srcs = ["Sophus/test/core/test_velocities.cpp"],
    deps = [
        ":Sophus",
        ":tests",
    ],
)

#./test/ceres/test_ceres_se3.cpp
