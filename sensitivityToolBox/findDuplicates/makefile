CC=g++
TARGET=doEventsList
OBJECTS=doEventsList.o
INCFLAGS=-m64 -O2 -Wall -I./ -I$(shell root-config --incdir) -std=c++11
LIBS=-m64 $(shell root-config --libs) -lTreePlayer -lHistPainter

$(TARGET).exe: $(OBJECTS)
	@echo "linking executable..."
	$(CC) $(OBJECTS) $(LIBS) -o $(TARGET)

clean:
	@rm -f *.o *~

veryclean: clean
	@rm -f $(TARGET)

%.o: %.cxx
	@echo "compiling C++ source..." 
	$(CC) -c $(INCFLAGS) $<
