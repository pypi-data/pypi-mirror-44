#include <gba.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "imageData.h"
#include "graphics.h"

static bool forceMapCopy;

static const int* currentMapSize;
static const int* currentSpecials;
static const unsigned short* currentBottomMap;
static const int* currentBottomMapSize;
static const unsigned short* currentMiddleMap;
static const int* currentMiddleMapSize;
static const unsigned short* currentTopMap;
static const int* currentTopMapSize;

void moveScreen(int screenx, int screeny) {
    static int lastscreentx;
    static int lastscreenty;
    int screentx = (screenx) / 8;
    int screenty = (screeny) / 8;

    if (screentx != lastscreentx || screenty != lastscreenty || forceMapCopy) {
        for (int i = 0; i < 22; ++i) {
            dmaCopy(currentBottomMap + (i + screenty - 1) * currentBottomMapSize[0] + screentx - 1, MAP_BASE_ADR(28) + 32 * 2 * i, 32 * 2);
        }
        for (int i = 0; i < 22; ++i) {
            dmaCopy(currentMiddleMap + (i + screenty - 1) * currentTopMapSize[0] + screentx - 1, MAP_BASE_ADR(29) + 32 * 2 * i, 32 * 2);
        }
        for (int i = 0; i < 22; ++i) {
            dmaCopy(currentTopMap + (i + screenty - 1) * currentTopMapSize[0] + screentx - 1, MAP_BASE_ADR(30) + 32 * 2 * i, 32 * 2);
        }
    }

    REG_BG1HOFS = screenx % 8 + 8;
    REG_BG1VOFS = screeny % 8 + 8;
    REG_BG2HOFS = screenx % 8 + 8;
    REG_BG2VOFS = screeny % 8 + 8;
    REG_BG3HOFS = screenx % 8 + 8;
    REG_BG3VOFS = screeny % 8 + 8;

    lastscreentx = screentx;
    lastscreenty = screenty;
}

void forceMoveScreen(int screenx, int screeny) {
    forceMapCopy = true;
    moveScreen(screenx, screeny);
}

void setSpecialActions(void (*heroSpecialActions_[])(int x, int y), int heroSpecialActionCount_);
{% for map_name, map in maps.items() %}
void loadMap{{ map_name }}(void (*heroSpecialActions_[])(int x, int y), int heroSpecialActionCount_) {
    currentMapSize = {{ map_name }}Size;
    currentSpecials = {{ map_name }}Specials;
    dmaCopy({{ map_name }}Palette, BG_PALETTE, {{ map_name }}PaletteLen);
    dmaCopy({{ map_name }}Tileset, TILE_BASE_ADR(0), {{ map_name }}TilesetLen);
    currentBottomMap = {{ map.bottom_layer_name }};
    currentBottomMapSize = {{ map.bottom_layer_name }}Size;
    currentMiddleMap = {{ map.middle_layer_name }};
    currentMiddleMapSize = {{ map.middle_layer_name }}Size;
    currentTopMap = {{ map.top_layer_name }};
    currentTopMapSize = {{ map.top_layer_name }}Size;

    forceMoveScreen(0, 0);
    
    if (heroSpecialActionCount_ > 0) {
        setSpecialActions(heroSpecialActions_, heroSpecialActionCount_);
    }
}
{%- endfor %}

// each sprite has its 3 attrs, a size and a position
u16 spriteAttrs[128][3];
int spriteRealSizes[128][2];
static int spritePositions[128][2];
static int spriteMapPositions[128][2];
static bool spriteShowOnMap[128];

static u16* spritePaletteIndex = (u16*)SPRITE_PALETTE + 1;
static u32* spriteTilesetIndex = (u32*)OBJ_BASE_ADR;

static int lastSpriteGraphicIndex;
{% for sprite_graphic_name in sprite_graphics.keys() %}
static bool {{ sprite_graphic_name }}loaded = false;
static int {{ sprite_graphic_name }}Location;

void loadSpriteGraphic{{ sprite_graphic_name }}() {
    if ({{ sprite_graphic_name }}loaded == true) {
        return;
    }
    {{ sprite_graphic_name }}Location = (spriteTilesetIndex - (u32*)OBJ_BASE_ADR) / 8;

    dmaCopy({{ sprite_graphic_name }}Palette, spritePaletteIndex, {{ sprite_graphic_name }}PaletteLen * 2);
    char colorOffset = spritePaletteIndex - (u16*)SPRITE_PALETTE;
    for (int i = 0; i < {{ sprite_graphic_name }}TilesetLen; i += 4) {
        u32 val = 0;
        for (int o = 0; o < 4; ++o) {
            if ({{ sprite_graphic_name }}Tileset[i + o] != 255) {
                val += (({{ sprite_graphic_name }}Tileset[i + o] + colorOffset) & 255) << (8 * o);
            }
        }
        *spriteTilesetIndex = val;
        spriteTilesetIndex += 1;
    }

    spritePaletteIndex += {{ sprite_graphic_name }}PaletteLen;
    {{ sprite_graphic_name }}loaded = true;
    lastSpriteGraphicIndex = {{ loop.index }};
}

void unloadSpriteGraphic{{ sprite_graphic_name }}() {
    if (({{ sprite_graphic_name }}loaded == false) || (lastSpriteGraphicIndex != {{ loop.index }})) {
        return;
    }
    spritePaletteIndex -= {{ sprite_graphic_name }}PaletteLen;
    spriteTilesetIndex -= {{ sprite_graphic_name }}TilesetLen;
    {{ sprite_graphic_name }}loaded = false;
}
{%- endfor %}

void clearSpriteGraphics() {
    spritePaletteIndex = (u16*)SPRITE_PALETTE + 1;
    spriteTilesetIndex = (u32*)OBJ_BASE_ADR;
    memset((void*)SPRITE_PALETTE, 0, 512);
    // TODO: zjistit jestli odpovida cislo 512 - jestli ne tak to budou hoooodne random bugy :D
    memset((void*)OBJ_BASE_ADR, 0, 512);
    {% for sprite_graphic_name in sprite_graphics.keys() %}
    {{ sprite_graphic_name }}loaded = false;
    {% endfor %}
}

void updateSpriteAttr0(int spriteIndex) {
    OAM[spriteIndex].attr0 = spriteAttrs[spriteIndex][0] + spritePositions[spriteIndex][1];
}

void updateSpriteAttr1(int spriteIndex) {
    OAM[spriteIndex].attr1 = spriteAttrs[spriteIndex][1] + spritePositions[spriteIndex][0];
}

void updateSpriteAttr2(int spriteIndex) {
    OAM[spriteIndex].attr2 = spriteAttrs[spriteIndex][2];
}

void setSpriteX(int spriteIndex, int x) {
    x = x & 511;
    spritePositions[spriteIndex][0] = x;
    updateSpriteAttr1(spriteIndex);
}

void setSpriteY(int spriteIndex, int y) {
    y = y & 255;
    spritePositions[spriteIndex][1] = y;
    updateSpriteAttr0(spriteIndex);
}

int getSpriteX(int spriteIndex) {
    return spritePositions[spriteIndex][0];
}

int getSpriteY(int spriteIndex) {
    return spritePositions[spriteIndex][1];
}

void setSpriteDisable(int spriteIndex) {
    spriteAttrs[spriteIndex][0] = OBJ_DISABLE | spriteAttrs[spriteIndex][0];
    updateSpriteAttr0(spriteIndex);
}

void setSpriteEnable(int spriteIndex) {
    spriteAttrs[spriteIndex][0] = ~OBJ_DISABLE & spriteAttrs[spriteIndex][0];
    updateSpriteAttr0(spriteIndex);
}

void setSpritePriority(int spriteIndex, int p) {
    spriteAttrs[spriteIndex][2] = (spriteAttrs[spriteIndex][2] & ~OBJ_PRIORITY(3)) | OBJ_PRIORITY(p);
    updateSpriteAttr2(spriteIndex);
}

void showSpriteOnMap(int spriteIndex) {
    spriteShowOnMap[spriteIndex] = true;
}

void hideSpriteOnMap(int spriteIndex) {
    spriteShowOnMap[spriteIndex] = false;
    setSpriteDisable(spriteIndex);
}

void placeSpriteOnMap(int spriteIndex, int x, int y) {
    spriteMapPositions[spriteIndex][0] = x;
    spriteMapPositions[spriteIndex][1] = y;
    showSpriteOnMap(spriteIndex);
}

{% for sprite_graphic_name in sprite_graphics.keys() %}
void setSpriteGraphicsFrame{{ sprite_graphic_name }}(int spriteIndex, int frameIndex) {
    if ({{ sprite_graphic_name }}loaded == false) {
        return;
    }
    spriteAttrs[spriteIndex][0] = (spriteAttrs[spriteIndex][0] & ~OBJ_SHAPE(3)) | ({{ sprite_graphic_name }}Shape << 14);
    spriteAttrs[spriteIndex][1] = (spriteAttrs[spriteIndex][1] & ~ATTR1_SIZE_64) | ({{ sprite_graphic_name }}Size << 14);
    spriteAttrs[spriteIndex][2] = (spriteAttrs[spriteIndex][2] & ~OBJ_CHAR(1023)) | OBJ_CHAR({{ sprite_graphic_name }}Location + frameIndex * {{ sprite_graphic_name }}FrameLen);
    updateSpriteAttr0(spriteIndex);
    updateSpriteAttr1(spriteIndex);
    updateSpriteAttr2(spriteIndex);
    spriteRealSizes[spriteIndex][0] = {{ sprite_graphic_name }}RealSize[0];
    spriteRealSizes[spriteIndex][1] = {{ sprite_graphic_name }}RealSize[1];
}

void setSpriteGraphics{{ sprite_graphic_name }}(int spriteIndex) {
    setSpriteGraphicsFrame{{ sprite_graphic_name }}(spriteIndex, 0);
}
{% endfor %}

specialList spriteCheckForSpecials(int spriteIndex, int spritex, int spritey) {
    int spritetx = (spritex) / 8;
    int spritety = (spritey) / 8;
    int spritetex = (spritex - 1) / 8;
    int spritetey = (spritey - 1) / 8;

    specialList sl;
    sl.count = 0;
    for (int i = 0; i < 64; ++i) {
        sl.specials[i].code = 0;
        sl.specials[i].position[0] = 0;
        sl.specials[i].position[1] = 0;
    }

    for (int i = spritetx; i <= spritetex + spriteRealSizes[spriteIndex][0]; ++i) {
        for (int o = spritety; o <= spritetey + spriteRealSizes[spriteIndex][1]; ++o) {
            if (currentSpecials[i + o * currentMapSize[0]] != 0) {
                sl.specials[sl.count].code = currentSpecials[i + o * currentMapSize[0]];
                sl.specials[sl.count].position[0] = i;
                sl.specials[sl.count].position[1] = o;
                sl.count += 1;
            }
        }
    }

    return sl;
}

bool spriteCheckForAnySpecial(int spriteIndex, int spritex, int spritey) {
    int spritetx = (spritex) / 8;
    int spritety = (spritey) / 8;
    int spritetex = (spritex - 1) / 8;
    int spritetey = (spritey - 1) / 8;

    for (int i = spritetx; i <= spritetex + spriteRealSizes[spriteIndex][0]; ++i) {
        for (int o = spritety; o <= spritetey + spriteRealSizes[spriteIndex][1]; ++o) {
            if (currentSpecials[i + o * currentMapSize[0]] != 0) {
                return true;
            }
        }
    }

    return false;
}

bool spriteCheckForWalls(int spriteIndex, int spritex, int spritey) {
    int spritetx = (spritex) / 8;
    int spritety = (spritey) / 8;
    int spritetex = (spritex - 1) / 8;
    int spritetey = (spritey - 1) / 8;

    for (int i = spritetx; i <= spritetex + spriteRealSizes[spriteIndex][0]; ++i) {
        for (int o = spritety; o <= spritetey + spriteRealSizes[spriteIndex][1]; ++o) {
            if (currentSpecials[i + o * currentMapSize[0]] & 1) {
                return true;
            }
        }
    }

    return false;
}

bool checkSpriteCollision(int spriteIndex1, int sprite1x, int sprite1y, int spriteIndex2, int sprite2x, int sprite2y) {
    return (sprite1x <= sprite2x + spriteRealSizes[spriteIndex2][0] * 8) &&
           (sprite2x <= sprite1x + spriteRealSizes[spriteIndex1][0] * 8) &&
           (sprite1y <= sprite2y + spriteRealSizes[spriteIndex2][1] * 8) &&
           (sprite2y <= sprite1y + spriteRealSizes[spriteIndex1][1] * 8);
}

bool checkSpriteCollisionOnMap(int spriteIndex1, int spriteIndex2) {
    if ((spriteShowOnMap[spriteIndex1] == false) || (spriteShowOnMap[spriteIndex2] == false)) {
        return false;
    }
    return (spriteMapPositions[spriteIndex1][0] <= spriteMapPositions[spriteIndex2][0] + spriteRealSizes[spriteIndex2][0] * 8) &&
           (spriteMapPositions[spriteIndex2][0] <= spriteMapPositions[spriteIndex1][0] + spriteRealSizes[spriteIndex1][0] * 8) &&
           (spriteMapPositions[spriteIndex1][1] <= spriteMapPositions[spriteIndex2][1] + spriteRealSizes[spriteIndex2][1] * 8) &&
           (spriteMapPositions[spriteIndex2][1] <= spriteMapPositions[spriteIndex1][1] + spriteRealSizes[spriteIndex1][1] * 8);
}

static void (*heroSpecialActions[128])(int x, int y) = {0};
static int heroSpecialActionCount = 0;

void setSpecialActions(void (*heroSpecialActions_[])(int x, int y), int heroSpecialActionCount_) {
    for (int i = 0; i < heroSpecialActionCount_; ++i) {
        heroSpecialActions[i] = heroSpecialActions_[i];
    }
    heroSpecialActionCount = heroSpecialActionCount_;
}

int hero_sprite_index;
static int* hero_x_pointer;
static int* hero_y_pointer;

void updateMap() {
    int screenx = 0;
    int screeny = 0;
    static int last_hero_x;
    static int last_hero_y;

    // mapm boundry check
    if (*hero_x_pointer < 0) {
        *hero_x_pointer = 0;
    } else if (*hero_x_pointer > currentMapSize[0] * 8 - spriteRealSizes[hero_sprite_index][0] * 8) {
        *hero_x_pointer = currentMapSize[0] * 8 - spriteRealSizes[hero_sprite_index][0] * 8;
    }
    if (*hero_y_pointer < 0) {
        *hero_y_pointer = 0;
    } else if (*hero_y_pointer > currentMapSize[1] * 8 - spriteRealSizes[hero_sprite_index][1] * 8) {
        *hero_y_pointer = currentMapSize[1] * 8 - spriteRealSizes[hero_sprite_index][1] * 8;
    }

    // collision check
    specialList sl = spriteCheckForSpecials(hero_sprite_index, *hero_x_pointer, *hero_y_pointer);
    for (int i = 0; i < sl.count; ++i) {
        int code = sl.specials[i].code;
        if (code & 1) {
            *hero_x_pointer = last_hero_x;
            *hero_y_pointer = last_hero_y;
        }
        if ((code >> 1 != 0) && ((code >> 1) - 1 < heroSpecialActionCount)) {
            heroSpecialActions[(code >> 1) - 1](sl.specials[i].position[0], sl.specials[i].position[1]);
        }
    }

    // move the sreen and the sprite
    if (*hero_x_pointer <= 120 - spriteRealSizes[hero_sprite_index][0] * 4) {
        setSpriteX(hero_sprite_index, *hero_x_pointer);
    } else if (*hero_x_pointer >= currentMapSize[0] * 8 - 120 - spriteRealSizes[hero_sprite_index][0] * 4) {
        screenx = currentMapSize[0] * 8 - 240;
        setSpriteX(hero_sprite_index, OBJ_X(*hero_x_pointer - (currentMapSize[0] * 8 - 120 - spriteRealSizes[hero_sprite_index][0] * 4) + 120 - spriteRealSizes[hero_sprite_index][0] * 4));
    } else {
        screenx = *hero_x_pointer - (120 - spriteRealSizes[hero_sprite_index][0] * 4);
        setSpriteX(0, 120 - spriteRealSizes[hero_sprite_index][0] * 4);
    }
    if (*hero_y_pointer <= 80 - spriteRealSizes[hero_sprite_index][1] * 4) {
        setSpriteY(hero_sprite_index, *hero_y_pointer);
    } else if (*hero_y_pointer >= currentMapSize[1] * 8 - 80 - spriteRealSizes[hero_sprite_index][1] * 4) {
        screeny = currentMapSize[1] * 8 - 160;
        setSpriteY(hero_sprite_index, *hero_y_pointer - (currentMapSize[1] * 8 - 80 - spriteRealSizes[hero_sprite_index][1] * 4) + 80 - spriteRealSizes[hero_sprite_index][1] * 4);
    } else {
        screeny = *hero_y_pointer - (80 - spriteRealSizes[hero_sprite_index][1] * 4);
        setSpriteY(hero_sprite_index, 80 - spriteRealSizes[hero_sprite_index][1] * 4);
    }
    moveScreen(screenx, screeny);
    last_hero_x = *hero_x_pointer;
    last_hero_y = *hero_y_pointer;

    for (int spriteIndex = 0; spriteIndex < 128; ++spriteIndex) {
        if (spriteShowOnMap[spriteIndex]) {
            int sprite_x = spriteMapPositions[spriteIndex][0] - screenx;
            int sprite_y = spriteMapPositions[spriteIndex][1] - screeny;
            if (sprite_x > -8 && sprite_x < 240 && sprite_y > -8 && sprite_y < 160){
                setSpriteX(spriteIndex, spriteMapPositions[spriteIndex][0] - screenx);
                setSpriteY(spriteIndex, spriteMapPositions[spriteIndex][1] - screeny);
                setSpriteEnable(spriteIndex);
            } else {
                setSpriteDisable(spriteIndex);
            }
        }
    }
}

void initHero(int* hero_x_pointer_, int* hero_y_pointer_, int hero_sprite_index_) {
    hero_x_pointer = hero_x_pointer_;
    hero_y_pointer = hero_y_pointer_;
    hero_sprite_index = hero_sprite_index_;
}

void showText() {
    REG_DISPCNT = REG_DISPCNT | BG0_ON;
}

void hideText() {
    REG_DISPCNT = REG_DISPCNT & ~BG0_ON;
}

static void setText(char* text) {
    u16 *text_out = (u16*)MAP_BASE_ADR(31);
    text_out += 380;
    for (int i = 0; i < 156; ++i) {
        if (i % 26 == 0) {
            text_out += 6;
        }
        if ((text[i] > 31) & (text[i] < 127)) {
            *text_out = (15 << 12) + text[i] - 31;
        } else {
            *text_out = (15 << 12) + 32 - 31;
        }
        text_out++;
    }
}

static void printPart(char* text) {
    setText(text);

    while (true) {
        VBlankIntrWait();
        scanKeys();
        if (keysDown() & KEY_A) {
            break;
        }
    }
}

void printText(char* text) {
    REG_DISPCNT = REG_DISPCNT | BG0_ON;

    int index = 0;
    int partLen = 0;
    char part[156] = {0};
    int wordLen = 0;
    char word[156] = {0};

    while (text[index] != 0) {
        if (partLen == 156) {
            printPart(part);
            for (int i = 0; i < 156; ++i) {
                part[i] = 0;
            }
            partLen = 0;
        }
        if (text[index] == ' ') {
            if (((partLen) % 26) + wordLen > 26) {
                for (int i = ((partLen) % 26); i < 26; ++i) {
                    part[partLen] = ' ';
                    partLen++;
                }
            }
            if (partLen + wordLen >= 156) {
                printPart(part);
                for (int i = 0; i < 156; ++i) {
                    part[i] = 0;
                }
                partLen = 0;
            }
            for (int i = 0; i < wordLen; ++i) {
                part[partLen] = word[i];
                partLen++;
            }
            part[partLen] = ' ';
            partLen++;
            for (int i = 0; i < 156; ++i) {
                word[i] = 0;
            }
            wordLen = 0;
        } else {
            word[wordLen] = text[index];
            wordLen++;
        }
        index++;
    }
    if (((partLen) % 26) + wordLen > 26) {
        for (int i = ((partLen) % 26); i < 26; ++i) {
            part[partLen] = '!';
            partLen++;
        }
    }
    if (partLen + wordLen >= 156) {
        printPart(part);
        for (int i = 0; i < 156; ++i) {
            part[i] = 0;
        }
        partLen = 0;
    }
    for (int i = 0; i < wordLen; ++i) {
        part[partLen] = word[i];
        partLen++;
    }
    part[partLen] = ' ';
    partLen++;
    for (int i = 0; i < 156; ++i) {
        word[i] = 0;
    }
    wordLen = 0;
    printPart(part);

    REG_DISPCNT = REG_DISPCNT & ~BG0_ON;
}

void initText(char font[][8]) {
    REG_BG0CNT = TILE_BASE(3) | MAP_BASE(31) | BG_PRIORITY(0);

    if (font == NULL) {
        font = default_font;
    }

    u32 *font_out = (u32*)TILE_BASE_ADR(3);

    font_out += 8;

    for (int symbol_index = 32; symbol_index < 128; ++symbol_index) {
        for (int part_index = 0; part_index < 8; ++part_index) {
            u32 val = 0;
            char part = font[symbol_index][part_index];
            for (int bit_index = 0; bit_index < 8; ++bit_index) {
                if ((part >> bit_index) & 1) {
                    val += 15 << (4 * bit_index);
                } else {
                    val += 13 << (4 * bit_index);
                }
            }
            *font_out = val;
            font_out++;
        }
    }

    dmaCopy(BorderTextPal, BG_PALETTE + 252, 8);
    dmaCopy(BorderTextTileset, font_out, 24 * 4);

    *(((u16*)MAP_BASE_ADR(31)) + 353) = (15 << 12) + 97;
    *(((u16*)MAP_BASE_ADR(31)) + 380) = (61 << 10) + 97;
    *(((u16*)MAP_BASE_ADR(31)) + 577) = (31 << 11) + 97;
    *(((u16*)MAP_BASE_ADR(31)) + 604) = (63 << 10) + 97;
    for (int i = 354; i < 380; ++i) {
        *(((u16*)MAP_BASE_ADR(31)) + i) = (15 << 12) + 98;
    }
    for (int i = 412; i < 604; i += 32) {
        *(((u16*)MAP_BASE_ADR(31)) + i) = (61 << 10) + 99;
    }
    for (int i = 578; i < 604; ++i) {
        *(((u16*)MAP_BASE_ADR(31)) + i) = (31 << 11) + 98;
    }
    for (int i = 385; i < 576; i += 32) {
        *(((u16*)MAP_BASE_ADR(31)) + i) = (15 << 12) + 99;
    }
}

void initMap() {
    irqInit();
    irqEnable(IRQ_VBLANK);
    SetMode(BG3_ON | BG2_ON | BG1_ON | OBJ_ENABLE | OBJ_1D_MAP);

    REG_BG3CNT = TILE_BASE(0) | MAP_BASE(28) | BG_256_COLOR | BG_PRIORITY(3);
    REG_BG2CNT = TILE_BASE(0) | MAP_BASE(29) | BG_256_COLOR | BG_PRIORITY(3);
    REG_BG1CNT = TILE_BASE(0) | MAP_BASE(30) | BG_256_COLOR | BG_PRIORITY(0);

    REG_BG1HOFS = 0;
    REG_BG1VOFS = 0;
    REG_BG2HOFS = 0;
    REG_BG2VOFS = 0;
    REG_BG3HOFS = 0;
    REG_BG3VOFS = 0;

    for (int i = 0; i < 128; ++i) {
        spriteAttrs[i][0] = OBJ_DISABLE | OBJ_256_COLOR;
        setSpritePriority(i, 1);
        updateSpriteAttr0(i);
    }
}

