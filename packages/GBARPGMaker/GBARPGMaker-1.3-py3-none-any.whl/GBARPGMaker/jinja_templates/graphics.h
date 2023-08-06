#ifndef GRAPHICS_H
#define GRAPHICS_H

void moveScreen(int screenx, int screeny);

void forceMoveScreen(int screenx, int screeny);

{% for map_name in maps.keys() %}
void loadMap{{ map_name }}(void (*heroSpecialActions_[])(int x, int y), int heroSpecialActionCount_);
{% endfor -%}

u16 spriteAttrs[128][3];
int spriteRealSizes[128][2];

{%- for sprite_graphic_name in sprite_graphics.keys() %}
void loadSpriteGraphic{{ sprite_graphic_name }}();

void unloadSpriteGraphic{{ sprite_graphic_name }}();
{% endfor %}

void clearSpriteGraphics();

void updateSpriteAttr0(int spriteIndex);
void updateSpriteAttr1(int spriteIndex);
void updateSpriteAttr2(int spriteIndex);

void setSpriteX(int spriteIndex, int x);

void setSpriteY(int spriteIndex, int y);

int getSpriteX(int spriteIndex);

int getSpriteY(int spriteIndex);

void setSpriteDisable(int spriteIndex);

void setSpriteEnable(int spriteIndex);

void setSpritePriority(int spriteIndex, int p);

void showSpriteOnMap(int spriteIndex);

void hideSpriteOnMap(int spriteIndex);

void placeSpriteOnMap(int spriteIndex, int x, int y);

{% for sprite_graphic_name in sprite_graphics.keys() %}
void setSpriteGraphicsFrame{{ sprite_graphic_name }}(int spriteIndex, int frameIndex);
void setSpriteGraphics{{ sprite_graphic_name }}(int spriteIndex);
{% endfor %}

typedef struct {
    int code;
    int position[2];
} special;

typedef struct {
    int count;
    special specials[64];
} specialList;

specialList spriteCheckForSpecials(int spriteIndex, int spritex, int spritey);

bool spriteCheckForAnySpecial(int spriteIndex, int spritex, int spritey);

bool spriteCheckForWalls(int spriteIndex, int spritex, int spritey);

bool checkSpriteCollision(int spriteIndex1, int sprite1x, int sprite1y, int spriteIndex2, int sprite2x, int sprite2y);

bool checkSpriteCollisionOnMap(int spriteIndex1, int spriteIndex2);

void setSpecialActions(void (*special_Actions_[])(int x, int y), int specialActionCount_);

void updateMap();

void initHero(int* hero_x_pointer_, int* hero_y_pointer_, int hero_sprite_index_);

void showText();

void hideText();

void printText(char* text);

void initText(char font[][8]);

void initMap();

#endif
