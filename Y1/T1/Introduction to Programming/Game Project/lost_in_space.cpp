#include "lost_in_space.h"
#include "splashkit.h"

#define MIN_POWER_UP_RANGE -1500
#define MAX_POWER_UP_RANGE 1500
#define MAX_GAME_RANGE 3000

game_data new_game()
{
    game_data game;
    game.player = new_player();
    return game;
}

void apply_power_up(game_data &game, int index)
{
    if (game.power_ups[index].kind == FUEL)
    {
        if (game.player.fuel_pct <= 1)
        {
            game.player.fuel_pct += 0.25;
        }
        play_sound_effect("rocket_sound");
    }
    else
    {
        play_sound_effect("default_sound");
    }
}

void remove_power_up(game_data &game, int index)
{
    int last_idx = game.power_ups.size() - 1;
    game.power_ups[index] = game.power_ups[last_idx];
    game.power_ups.pop_back();
}

void check_collisions(game_data &game)
{
    for (int i = game.power_ups.size() - 1; i >= 0; i--)
    {
        if (sprite_collision(game.player.player_sprite, game.power_ups[i].power_up_sprite))
        {
            game.player.level++;
            apply_power_up(game, i);
            remove_power_up(game, i);
        }
    }
}

void add_power_up(game_data &game)
{
    int value = rnd(MIN_POWER_UP_RANGE, MAX_POWER_UP_RANGE);
    game.power_ups.push_back(new_power_up(value, value));
}

void check_power_up_position(game_data &game)
{
    for (int i = 0; i < game.power_ups.size(); i++)
    {
        double power_up_x = sprite_x(game.power_ups[i].power_up_sprite);
        double power_up_y = sprite_y(game.power_ups[i].power_up_sprite);

        if (power_up_x > MAX_POWER_UP_RANGE || power_up_y > MAX_POWER_UP_RANGE ||
            power_up_x < MIN_POWER_UP_RANGE || power_up_y < MIN_POWER_UP_RANGE)
        {
            remove_power_up(game, i);
        }
    }
}

void update_game(game_data &game)
{
    if (rnd() < 0.02)
    {
        add_power_up(game);
    }

    check_collisions(game);
    update_player(game.player);

    for (int i = 0; i < game.power_ups.size(); i++)
    {
        check_power_up_position(game);
        update_power_up(game.power_ups[i]);
    }
}

drawing_options option_part(double x, double y, double width, double height)
{
    drawing_options options;
    options = option_part_bmp(x, y, width, height, option_to_screen());
    return options;
}

void draw_hud(const game_data &game)
{
    clear_screen(COLOR_GRAY);
    draw_rectangle(COLOR_BLUE, 10, 10, 350, 150, option_part(0, 0, 340, 220));

    draw_text("LEVEL: " + to_string(game.player.level), COLOR_BLACK, 30, 40, option_to_screen());
    draw_text("LOCATION: " + point_to_string(center_point(game.player.player_sprite)), COLOR_BLACK, 15, 25, option_to_screen());

    draw_text("FUEL: ", COLOR_BLACK, 15, 65, option_to_screen());
    draw_bitmap("empty", 50, 50, option_part(0, 0, bitmap_width("empty"), bitmap_height("empty")));
    draw_bitmap("full", 50, 50, option_part(0, 0, game.player.fuel_pct * bitmap_width("full"), bitmap_height("full")));
}

void draw_game(const game_data &game)
{
    draw_hud(game);

    draw_player(game.player);

    for (int i = 0; i < game.power_ups.size(); i++)
    {
        draw_power_up(game.power_ups[i]);
    }

    refresh_screen(60);
}


