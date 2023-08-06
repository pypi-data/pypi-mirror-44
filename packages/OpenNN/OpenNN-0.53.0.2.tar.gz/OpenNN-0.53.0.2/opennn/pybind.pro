###################################################################################################
#                                                                                                 #
#   OpenNN: Open Neural Networks Library                                                          #
#   www.artelnics.com/opennn                                                                      #
#                                                                                                 #
#   P Y B I N D 1 1   P R O J E C T                                                               #
#                                                                                                 #
#   Artificial Intelligence Techniques SL                                                         #
#   artelnics@artelnics.com                                                                       #
#                                                                                                 #
###################################################################################################

QT = core# Do not use qt

TEMPLATE = app
CONFIG += console
CONFIG += c++11

mac{
    CONFIG-=app_bundle
}

TARGET = opennnp


SOURCES += pybind.cpp

win32-g++{
QMAKE_LFLAGS += -static-libgcc
QMAKE_LFLAGS += -static-libstdc++
QMAKE_LFLAGS += -static
}

# OpenNN library


# OpenMP library

win32:!win32-g++{
QMAKE_CXXFLAGS += -openmp
QMAKE_LFLAGS   += -openmp
}

!win32{
QMAKE_CXXFLAGS+= -fopenmp
QMAKE_LFLAGS +=  -fopenmp
}

mac{
INCLUDEPATH += /usr/local/Cellar/libiomp/20150701/include/libiomp
LIBS += -L/usr/local/Cellar/libiomp/20150701/lib -liomp5
}



