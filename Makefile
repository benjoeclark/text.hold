CPP = g++
LIBS = hold.o game.o

.cpp.o :
	$(CPP) -c $<

play : play.cpp $(LIBS)
	$(CPP) -o $@ play.cpp $(LIBS)

clean:
	rm -rf play $(LIBS)
