
# We are using the 'format_map' function with those strings, so we use
# double brackets here to escape normal brackets

# inputs: project_name
cmake_base = ('cmake_minimum_required( VERSION 3.8.0 )\n'
'project( {project_name} )\n\n'
'set(CMAKE_CXX_STANDARD 17)\n'
'add_compile_options( -Wall -Wextra -pedantic )\n\n'
'include_directories( ${{CMAKE_CURRENT_SOURCE_DIR}} )\n')

# inputs: project_name
header_base = ('#ifndef {project_name}_HPP\n'
'#define {project_name}_HPP\n\n\n'
'#endif')

main_tests = ('#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN\n'
'#include "extern/doctest.h"\n\n')

main_sample = ('#include <iostream>\n'
'int main() {{\n'
'\tputs("Hello world!");\n'
'\treturn 0;\n'
'}}')

