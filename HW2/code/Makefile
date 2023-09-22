CXX = g++
CXXFLAGS = -std=c++11
OPENCV_LIBS = `pkg-config --cflags --libs opencv4`

.PHONY: all clean graph

all: $(patsubst %.cpp,%,$(wildcard *.cpp)) graph

%: %.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(OPENCV_LIBS)
	./$@

graph: 
	python3 graph.py

clean:
	rm -f $(patsubst %.cpp,%,$(wildcard *.cpp)) histogram.csv

