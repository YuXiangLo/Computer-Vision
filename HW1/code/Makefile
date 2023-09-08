CXX = g++
CXXFLAGS = -std=c++11
OPENCV_LIBS = `pkg-config --cflags --libs opencv4`

.PHONY: all clean

all: $(patsubst %.cpp,%,$(wildcard *.cpp))

%: %.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(OPENCV_LIBS)
	./$@

clean:
	rm -f $(patsubst %.cpp,%,$(wildcard *.cpp))

