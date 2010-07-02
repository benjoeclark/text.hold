CPP = g++
LIBS = hold.o game.o shop.o

.cpp.o :
	$(CPP) -c $<

all : play buy

play : play.cpp $(LIBS)
	$(CPP) -o $@ $< $(LIBS)

buy : buy.cpp $(LIBS)
	$(CPP) -o $@ $< $(LIBS)

clean:
	rm -rf play buy $(LIBS)
