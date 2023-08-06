#include <gba.h>
#include <stdio.h>
#include <stdlib.h>

#include "imageData.h"
#include "graphics.h"

int hero_x = 10;
int hero_y = 10;

int main() {
    // init stuff and load sprites
    initMap();
    initText(NULL);

    loadSpriteGraphic{{ first_sprite_graphics_name }}();

    // setup hero
    initHero(&hero_x, &hero_y, 0);

    setSpriteGraphics{{ first_sprite_graphics_name }}(0);
    setSpriteEnable(0);

    // load first map
    loadMap{{ first_map_name }}(NULL, 0);
    updateMap();

    while (true) {
        scanKeys();
        if (keysHeld() & KEY_RIGHT) {
            hero_x += 1;
        } else if (keysHeld() & KEY_LEFT) {
            hero_x -= 1;
        } else if (keysHeld() & KEY_DOWN) {
            hero_y += 1;
        } else if (keysHeld() & KEY_UP) {
            hero_y -= 1;
        }

        // wait for the next VBlank before updating graphics
        VBlankIntrWait();
        updateMap();
    }
}
