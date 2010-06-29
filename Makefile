CPP = g++
LIBS = lib/hold.hpp

simulate : simulate.cpp $(LIBS)
	$(CPP) -o $@ $<

clean:
	rm simulate
