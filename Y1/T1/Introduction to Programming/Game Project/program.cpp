#include "splashkit.h"
#include "player.h"
#include "power_up.h"
#include "lost_in_space.h"

/**
 * Load the game images, sounds, etc.
 */
void load_resources()
{
    // Load the resource bundle "game_bundle" from "lost_in_space.txt" (if you haven't done so already)
    load_resource_bundle("game_bundle", "lost_in_space.txt");

    // Load player ship bitmaps
    load_bitmap("aquarii", "path_to_aquarii_ship.png");  // Replace with your image path
    load_bitmap("gliese", "path_to_gliese_ship.png");    // Replace with your image path
    load_bitmap("pegasi", "path_to_pegasi_ship.png");    // Replace with your image path

    // Load power-up bitmaps
    load_bitmap("life", "path_to_blue_bar_bubbles_up.png");        // Replace with your image path
    load_bitmap("fuel", "path_to_fuel_up.png");          // Replace with your image path
    load_bitmap("star", "path_to_star_up.png");        // Replace with your image path
    load_bitmap("heart", "path_to_saturn_up.png");      // Replace with your image path

    // Load sound effects
    load_sound_effect("rocket_sound", "rocket.wav");        // Replace with your sound effect file path
    load_sound_effect("default_sound", "default.wav");          // Replace with your sound effect file path
}
/**
 * Entry point.
 *
 * Manages the initialization of data, the event loop, and quitting.
 */
int main()
{
    open_window("Lost In Space", 800, 800);
    load_resources();

    // Initialize the new game with a new player
    game_data my_game;
    my_game = new_game();

    while (!quit_requested())
    {
        process_events();

        // Handle input to adjust player movement
        handle_input(my_game.player);

        // Update the game with player and power-ups
        update_game(my_game);

        // Draw the game
        draw_game(my_game);
    }

    return 0;
}