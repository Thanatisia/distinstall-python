## Makefile containing targets/rules/functions for documentation generating using asciinema and asciinema-agg

## Ingredients/Variables

### Documentation Settings
#### System Command
command ?= 
#### Demo Recording
demo_recording_output_filename ?= output.cast
#### Demo GIF
demo_gif_input_filename ?= output.cast
demo_gif_output_filename ?= output
demo_gif_output_format ?= gif
demo_gif_background_theme ?= monokai
demo_gif_foreground_font ?=
demo_gif_canvas_size ?= 
demo_gif_font_size ?= --font-size 16
demo_gif_process_options ?= --speed 2
#### Asciinema/agg options
asciinema_options ?= --overwrite
asciinema_agg_options ?= $(demo_gif_canvas_size) $(demo_gif_font_size) $(demo_gif_foreground_font) $(demo_gif_process_options)

### System
SHELL := bash
.PHONY := help record
.DEFAULT_RULES := help

## Targets/Rules
help:
	## Display help message
	@echo -e "help : Display this help message"
	@echo -e "record : Record the demo using asciinema-util (asciinema options)"
	@echo -e "convert : Convert the recorded demo .cast file using asciinema-util (asciinema-agg options)"

record:
	## Record the demo using asciinema-util (asciinema options)
	@asciinema-util record \
		--output-terminal-rec-filename ${demo_recording_output_filename} \
		--asciinema-opts "${asciinema_options}" \
		-c "${command}"

convert:
	## Convert the recorded demo .cast file using asciinema-util (asciinema-agg options)
	@asciinema-util convert \
		--theme ${demo_gif_background_theme} \
		--input-terminal-rec-filename ${demo_gif_input_filename} \
		--output-animation-filename ${demo_gif_output_filename}.${demo_gif_output_format} \
		--asciinema-agg-opts "${asciinema_agg_options}"

