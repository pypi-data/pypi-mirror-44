cc_library(
  name = "jpeg",
  hdrs = [
      "include/jpegint.h",
      "include/aarch64-linux-gnu/jconfig.h",
      "include/turbojpeg.h",
      "include/jerror.h",
      "include/jmorecfg.h",
      "include/jpeglib.h",
  ],
  srcs = [
      "lib/aarch64-linux-gnu/libjpeg.so",
      "lib/aarch64-linux-gnu/libjpeg.a",
      "lib/aarch64-linux-gnu/libturbojpeg.a",
  ],
  visibility = ["//visibility:public"],
)
