cc_library(
    name = "spinnaker",
    hdrs = glob(["*.h", "SpinGenApi/*.h", "Interface/*.h"]),
    linkopts = ["-lSpinnaker"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "spinnaker_config",
    data = glob(["SFNC*", "Input.xml"]),
)
