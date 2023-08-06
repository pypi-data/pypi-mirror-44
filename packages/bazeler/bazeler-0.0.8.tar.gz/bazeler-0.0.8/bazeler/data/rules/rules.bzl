COMMON_OPTS = ["-std=c++14", "-DEIGEN_INITIALIZE_MATRICES_BY_NAN"]
COMPILE_OPTS = COMMON_OPTS + ["-Wall", "-pedantic", "-Wextra", "-Wno-gnu"]
# Ideally:
#  STRICT_OPTS = COMPILE_OPTS + ["-Werror"]
# But this has to be configured on a per-codebase level
STRICT_OPTS = COMPILE_OPTS 
