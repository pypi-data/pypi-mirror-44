#ifndef IMAGE_DATA_H
#define IMAGE_DATA_H

// Background stuff

{% for map_name, map in maps.items() %}
#define {{ map_name }}PaletteLen {{ 2 * map.palette|length }}
extern const unsigned short {{ map_name }}Palette[{{ map.palette|length }}];

#define {{ map_name }}TilesetLen {{ 4 * map.tileset|length }}
extern const unsigned int {{ map_name }}Tileset[{{ map.tileset|length }}];

extern const int {{ map_name }}Size[2];

extern const int {{ map_name }}Specials[{{ map.specials|length }}];

{%- for i in range(map.layer_tile_maps|length) %}

#define {{ map.layer_names[i] }}Len {{ 2 * map.layer_tile_maps[i]|length }}
extern const int {{ map.layer_names[i] }}Size[2];
extern const unsigned short {{ map.layer_names[i] }}[{{ map.layer_tile_maps[i]|length }}];
{%- endfor %}
{% endfor %}

// Sprite stuff

{%- for sprite_graphic_name, sprite_graphic in sprite_graphics.items() %}

#define {{ sprite_graphic_name }}Shape {{ sprite_graphic.shape_size[0] }}
#define {{ sprite_graphic_name }}Size {{ sprite_graphic.shape_size[1] }}
extern const unsigned short {{ sprite_graphic_name }}RealSize[2];

#define {{ sprite_graphic_name }}PaletteLen {{ sprite_graphic.palette|length }}
extern const unsigned short {{ sprite_graphic_name }}Palette[{{ sprite_graphic.palette|length }}];

#define {{ sprite_graphic_name }}TilesetLen {{ sprite_graphic.tileset|length }}
#define {{ sprite_graphic_name }}FrameLen {{ 2 * (sprite_graphic.gba_size[0] * sprite_graphic.gba_size[1])|int }}
extern const int {{ sprite_graphic_name }}Tileset[{{ sprite_graphic.tileset|length }}];
{% endfor %}

const unsigned int BorderTextTileset[24];
const unsigned short BorderTextPal[4];
char default_font[128][8];
#endif
