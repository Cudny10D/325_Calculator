cmake_minimum_required(VERSION 3.16)
project(Calculator325 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# 中文/emoji 编码
if (MSVC)
    add_compile_options(/utf-8)
elseif (MINGW)
    add_compile_options(-finput-charset=UTF-8 -fexec-charset=UTF-8)
endif()

# 兼容 Qt6 / Qt5
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

add_executable(Calculator325 WIN32 main.cpp)
target_link_libraries(Calculator325 PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

set_target_properties(Calculator325 PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")