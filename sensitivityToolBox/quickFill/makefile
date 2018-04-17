CC=g++
TARGET=fillHistograms
OBJECTS=TreeClass.o fillHistograms.o
INCFLAGS=-m64 -O2 -Wall -I./ -I$(shell root-config --incdir) -std=gnu++11
LIBS=-m64 $(shell root-config --libs) -lTreePlayer -lHistPainter

$(TARGET): $(OBJECTS)
	@echo -e "\nlinking executable..."
	$(CC) $(OBJECTS) $(LIBS) -o $(TARGET)

clean:
	@rm -f *.o *~

veryclean: clean
	@rm -f $(TARGET)

%.o: %.cxx
	@echo -e "\ncompiling C++ source..." 
	$(CC) -c $(INCFLAGS) $<
