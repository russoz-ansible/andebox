#
# (C) 2025 Alexei Znamensky
# Licensed under the MIT License. See LICENSES/MIT.txt for details.
# SPDX-FileCopyrightText: 2025 Alexei Znamensky
# SPDX-License-Identifier: MIT
#

PEXPS = integration.pexp units.pexp sanity.pexp
CASTS = $(PEXPS:.pexp=.cast)
GIFS = $(CASTS:.cast=.gif)


PLAY_SPEED = 3.5


all: $(GIFS)


clean:
	rm -f *.cast *.gif

%.cast: %.pexp pexp make-cast
	@echo "=== Making cast file"
	./make-cast $< $@
	@echo "=== Cast file generated: $@\n\n"

%.gif: %.cast Makefile
	@echo "=== Making gif file"
	docker run --rm \
		-v $(shell pwd):/data \
		--user $(shell id -u):$(shell id -g) \
		ghcr.io/asciinema/agg:latest -v \
		--speed $(PLAY_SPEED) \
		--theme dracula \
		--font-size 12 \
		$< $@
	ls -lh $@
	gifsicle --lossy=80 -k 128 -O2 -Okeep-empty $@ -o small-$@ && mv small-$@ $@
	ls -lh $@
	@echo "=== GIF file generated: $@\n\n"
