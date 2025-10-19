#ifndef LOST_IN_SPACE_PLAYER
#define LOST_IN_SPACE_PLAYER

#include "splashkit.h"
#include <vector>

using namespace std;

#define PLAYER_SPEED 1.5
#define PLAYER_ROTATE_SPEED 3
#define SCREEN_BORDER 100
#define STARTING_TIME 50

/**
 * Different ship options that determine the ship's appearance.
 */
enum ship_kind
{
    AQUARII,
    GLIESE,
    PEGASI
};

/**
 * The player data structure stores information related to the player.
 *
 * @field player_sprite: The player's sprite, used for position and movement tracking.
 * @field score: The current player level.
 * @field kind: The current player ship kind.
 * @field fuel_pct: Fuel percentage of the ship.
 * @field level: Current player path.
 */
struct player_data
{
    sprite player_sprite;
    int level;
    ship_kind kind;
    double fuel_pct;
    int path;
};

/**
 * Creates a new player in the center of the screen with the default ship.
 *
 * @returns The new player data.
 */
player_data new_player();

/**
 * Draws the player on the screen.
 *
 * @param player_to_draw: The player to draw on the screen.
 */
void draw_player(const player_data &player_to_draw);

/**
 * Updates the player's position and performs camera adjustments.
 *
 * @param player_to_update: The player being updated.
 */
void update_player(player_data &player_to_update);

/**
 * Reads user input and updates the player based on interactions.
 *
 * @param player: The player to update.
 */
void handle_input(player_data &player);

#endif