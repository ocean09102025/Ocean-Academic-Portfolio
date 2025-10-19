#include "player.h"
#include "splashkit.h"
#include "power_up.h"

/**
 * The power_up_bitmap function converts a power-up kind into a bitmap that can be used.
 *
 * This function is not exposed by the header.
 *
 * @param kind The kind of power-up you want the bitmap of
 * @return The bitmap matching this power-up kind
 */
bitmap power_up_bitmap(power_up_kind kind)
{
    switch (kind)
    {
        case LIFE:
            return bitmap_named("life");

        case FUEL:
            return bitmap_named("fuel");

        case STAR:
            return bitmap_named("star");

        case HEART:
            return bitmap_named("heart");
        default:
            return bitmap_named("fuel");
    }
}

power_up_data new_power_up(double x, double y)
{
    power_up_kind kind;
    power_up_data result;

    // Assigning a random power-up kind to the power_up_kind
    kind = static_cast<power_up_kind>(rnd(6));

    // Creating the power-up sprite with a random kind
    result.power_up_sprite = create_sprite(power_up_bitmap(kind));

    // Remembering the power-up kind
    result.kind = kind;

    // Setting the position for the power-up sprite
    sprite_set_x(result.power_up_sprite, x);
    sprite_set_y(result.power_up_sprite, y);

    // Giving some velocity to the power-up sprite so that it can move around
    sprite_set_dx(result.power_up_sprite, rnd() * 4 - 2);
    sprite_set_dy(result.power_up_sprite, rnd() * 4 - 2);

    return result;
}

void draw_power_up(const power_up_data &power_to_draw)
{
    // Drawing the power-up sprite to the screen
    draw_sprite(power_to_draw.power_up_sprite);
}

void update_power_up(power_up_data &power_to_update)
{
    // Updating the power-up sprite
    update_sprite(power_to_update.power_up_sprite);
}


