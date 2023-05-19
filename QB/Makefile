# Makefile for Java program

# Compiler and flags
JAVAC = javac
JAVA_FLAGS = -g -cp $(SOURCE_DIR)
JAVA = java

# Source and output directories
SOURCE_DIR = src
OUTPUT_DIR = bin

# Find all Java source files recursively
SOURCES := $(shell find $(SOURCE_DIR) -name '*.java')

# Generate class file paths based on source file paths
CLASSES := $(patsubst $(SOURCE_DIR)/%.java,$(OUTPUT_DIR)/%.class,$(SOURCES))

# Default target
all: $(CLASSES)

# Compile Java source files
$(OUTPUT_DIR)/%.class: $(SOURCE_DIR)/%.java
	@mkdir -p $(OUTPUT_DIR)/$(dir $<)
	$(JAVAC) $(JAVA_FLAGS) -d $(OUTPUT_DIR)/$(dir $<) $<

# Run the Java program
run: $(CLASSES)
	$(JAVA) -cp $(OUTPUT_DIR)/$(SOURCE_DIR) QBServer $(ARGS)

# Clean build artifacts
clean:
	rm -rf $(OUTPUT_DIR)

.PHONY: all run clean