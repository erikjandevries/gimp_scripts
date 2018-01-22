# This file contains a function for cutting a subject out of an image.

import gimpfu
import os


# if debug==True, we place on a green background
def convert(filename, new_name, x, y, feather_radius, debug=False):
    if x == '':
        x = 0
    if y == '':
        y = 0

    if feather_radius == '':
        feather_radius = 5

    img = pdb.gimp_file_load(filename, filename)
    layer = pdb.gimp_image_merge_visible_layers(img, 1)

    pdb.gimp_context_set_antialias(True)
    pdb.gimp_context_set_feather(True)
    pdb.gimp_context_set_feather_radius(feather_radius, feather_radius)
    # pdb.gimp_context_set_sample_criterion
    # pdb.gimp_context_set_sample_threshold
    # pdb.gimp_context_set_sample_transparent

    # 0 == CHANNEL_OP_ADD
    pdb.gimp_image_select_contiguous_color(img, 0, layer, y, x)

    if not pdb.gimp_edit_cut(layer):
        print "Couldn't cut...?"

    if debug:
        # 1 == RGBA_IMAGE
        # 0 == NORMAL_MODE
        layer_bg = pdb.gimp_layer_new(img, pdb.gimp_image_width(img), pdb.gimp_image_height(img), 1, "bg", 100, 0)

        pdb.gimp_image_insert_layer(img, layer_bg, None, 1)  # insert to bottom

        # BRIGHT GREEN
        pdb.gimp_context_set_foreground((0, 255, 0))

        pdb.gimp_drawable_fill(layer_bg, 0)  # 0 == FOREGROUND_FILL

        pdb.gimp_layer_add_alpha(layer)

        layer = pdb.gimp_image_merge_visible_layers(img, 1)

    pdb.gimp_file_save(img, layer, new_name, new_name)
    pdb.gimp_image_delete(img)


try:
    convert(os.environ["PY_CUT_INPUT"], os.environ["PY_CUT_OUTPUT"], os.environ["PY_CUT_X"], os.environ["PY_CUT_Y"], os.environ["PY_CUT_FEATHER_RADIUS"], os.environ.has_key("PY_CUT_DEBUG"))
finally:
    pdb.gimp_quit(1)
