from datagen_base import *


def make_basic_block(name, default_loot_table=True):
    variables = {'block': name}
    copy_blockstate('simple_blockstate', name, variables)
    copy_block_model('cube', name, variables)
    copy_item_model('block', name, variables)
    if default_loot_table:
        drop_itself(name, variables)


def make_pottable_plant(name):
    variables = {'block': name}
    copy_blockstate('simple_blockstate', name, variables)
    copy_block_model('bush', name, variables)
    copy_item_model('flat_block', name, variables)
    drop_itself(name, variables)

    potted_name = variables['block'] = 'potted_' + name
    copy_blockstate('simple_blockstate', potted_name, variables)
    copy_block_model('potted_bush', potted_name, variables)
    copy_loot_table('potted_bush', potted_name, variables)
    add_to_block_tag('flower_pots', '%s:%s' % (MODID, potted_name))


def make_flower(name, dye_color, condition):
    make_pottable_plant(name)
    copy_crafting_recipe('shapeless_one_ingredient', 'dyes/dye_from_' + name, {
        'ingredient': name,
        'output': 'minecraft:%s_dye' % dye_color,
        'count': '1',
        'condition': condition
    })

    add_to_item_and_block_tags('small_flowers', '%s:%s' % (MODID, name))


def make_tall_flower(name, dye_color, condition):
    copy_blockstate('tall_flower', name, {'block': name})
    copy_block_model('bush', name + '_top', {'block': name + '_top'})
    copy_block_model('bush', name + '_bottom', {'block': name + '_bottom'})
    copy_item_model('flat_block', name, {'block': name + '_top'})
    copy_loot_table('double_block', name, {'block': name})
    copy_crafting_recipe('shapeless_one_ingredient', 'dyes/dye_from_' + name, {
        'ingredient': name,
        'output': 'minecraft:%s_dye' % dye_color,
        'count': '2',
        'condition': condition
    })

    add_to_item_and_block_tags('tall_flowers', '%s:%s' % (MODID, name))


def make_stairs_and_slabs(type, base_block, condition):
    block = type + '_stairs'
    variables = {'type': type, 'block': block, 'base_block': base_block, 'condition': condition}
    copy_blockstate_and_models('stairs', block, variables, block_model_suffixes=['', '_inner', '_outer'])
    drop_itself(block, variables)
    copy_crafting_recipe('stairs', type + '/stairs', variables)

    block = type + '_slab'
    variables['block'] = block
    copy_blockstate_and_models('slab', block, variables, block_model_suffixes=['', '_top'])
    drop_itself(block, variables)
    copy_crafting_recipe('slabs', type + '/slab', variables)

    block = type + '_vertical_slab'
    variables['block'] = block
    copy_blockstate_and_models('vertical_slab', block, variables)
    drop_itself(block, variables)
    copy_crafting_recipe('vertical_slabs', 'compat/quark/%s/vertical_slabs' % type, variables)
    add_to_item_and_block_tags('vertical_slab', '%s:%s' % (MODID, block), namespace='quark')


def make_button(type, base_block, condition):
    block = type + '_button'
    variables = {'type': type, 'block': block, 'base_block': base_block, 'ingredient': base_block, 'output': '%s:%s' % (MODID, block),
            'count': '1', 'condition': condition}
    copy_blockstate_and_models('button', block, variables, block_model_suffixes=['', '_inventory', '_pressed'])
    drop_itself(block, variables)
    copy_crafting_recipe('shapeless_one_ingredient', type + '/button', variables)


def make_pressure_plate(type, base_block, condition):
    block = type + '_pressure_plate'
    variables = {'type': type, 'block': block, 'base_block': base_block, 'condition': condition}
    copy_blockstate_and_models('pressure_plate', block, variables, block_model_suffixes=['', '_down'])
    drop_itself(block, variables)
    copy_crafting_recipe('pressure_plate', type + '/pressure_plate', variables)


def make_wood_type(type):
    # Sapling and leaves
    sapling = type + '_sapling'
    make_pottable_plant(sapling)
    add_to_item_and_block_tags('saplings', '%s:%s' % (MODID, sapling))

    leaves = type + '_leaves'
    make_basic_block(leaves, default_loot_table=False)
    copy_loot_table('leaves', leaves, {'block': leaves, 'sapling': sapling})
    add_to_item_and_block_tags('leaves', '%s:%s' % (MODID, leaves))

    leaf_carpet = type + '_leaf_carpet'
    variables = {'type': type, 'block': leaf_carpet, 'condition': type}
    copy_blockstate('simple_blockstate', leaf_carpet, variables)
    copy_block_model('leaf_carpet', leaf_carpet, variables)
    copy_item_model('block', leaf_carpet, variables)
    drop_itself(leaf_carpet, variables)
    copy_crafting_recipe('leaf_carpet', 'compat/quark/%s/leaf_carpet' % type, variables)

    # Logs and wood
    for prefix in ['', 'stripped_']:
        log = prefix + type + '_log'
        variables = {'type': prefix + type, 'block': log}
        copy_blockstate_and_models('log', log, variables, block_model_suffixes=['', '_horizontal'])
        drop_itself(log, variables)

        wood = variables['block'] = prefix + type + '_wood'
        copy_blockstate_and_models('wood', wood, variables)
        drop_itself(wood, variables)
        copy_crafting_recipe('wood', '%s/%swood' % (type, prefix), {'type': type, 'log': log, 'wood': wood})

        post = prefix + type + '_post'
        variables = {'type': type, 'block': post, 'ingredient': wood}
        copy_blockstate_and_models('post', post, variables)
        drop_itself(post, variables)
        copy_crafting_recipe('post', 'compat/quark/%s/%spost' % (type, prefix), variables)

    copy_block_tag('wood', type + '_logs', variables)
    copy_item_tag('wood', type + '_logs', variables)
    add_to_item_and_block_tags('logs_that_burn', '#%s:%s_logs' % (MODID, type))

    # Planks, vertical planks, stairs and slabs
    planks = type + '_planks'
    make_basic_block(planks)
    copy_crafting_recipe('planks', type + '/planks', {'type': type})
    make_basic_block('vertical_' + planks)
    copy_crafting_recipe('vertical_planks', 'compat/quark/%s/vertical_planks' % type, {'type': type})
    make_stairs_and_slabs(type, planks, type)
    add_to_item_and_block_tags('planks', '%s:%s' % (MODID, planks), '%s:vertical_%s' % (MODID, planks))
    add_to_item_and_block_tags('wooden_stairs', '%s:%s_stairs' % (MODID, type))
    add_to_item_and_block_tags('wooden_slabs', '%s:%s_slab' % (MODID, type))

    # Buttons and pressure plates
    make_button(type, planks, type)
    make_pressure_plate(type, type + '_planks', type)
    add_to_item_and_block_tags('wooden_buttons', '%s:%s_button' % (MODID, type))
    add_to_item_and_block_tags('wooden_pressure_plates', '%s:%s_pressure_plate' % (MODID, type))

    # Fences and hedges
    fence = type + '_fence'
    variables = {'type': type, 'block': fence, 'base_block': planks}
    copy_blockstate_and_models('fence', fence, variables, block_model_suffixes=['_inventory', '_post', '_side'])
    drop_itself(fence, variables)
    copy_crafting_recipe('fence', type + '/fence', variables)
    add_to_item_and_block_tags('wooden_fences', '%s:%s' % (MODID, fence))
    add_to_item_and_block_tags('fences/wooden', '%s:%s' % (MODID, fence), namespace='forge')

    fence_gate = variables['block'] = fence + '_gate'
    copy_blockstate_and_models('fence_gate', fence_gate, variables,
                               block_model_suffixes=['', '_open', '_wall', '_wall_open'])
    drop_itself(fence_gate, variables)
    copy_crafting_recipe('fence_gate', type + '/fence_gate', variables)
    add_to_item_and_block_tags('fence_gates', '%s:%s' % (MODID, fence_gate))
    add_to_item_and_block_tags('fence_gates/wooden', '%s:%s' % (MODID, fence_gate), namespace='forge')

    hedge = variables['block'] = type + '_hedge'
    copy_blockstate_and_models('hedge', hedge, variables, block_model_suffixes=['_extend', '_post', '_side'],
                               item_model_suffix='_post')
    drop_itself(hedge, variables)
    copy_crafting_recipe('hedge', 'compat/quark/%s/hedge' % type, variables)
    add_to_item_and_block_tags('hedges', '%s:%s' % (MODID, hedge), namespace='quark')

    # Doors and trapdoors
    door = variables['block'] = type + '_door'
    copy_blockstate('door', door, variables)
    copy_block_model('door', door, variables, block_model_suffixes=['_bottom', '_bottom_hinge', '_top', '_top_hinge'])
    copy_item_model('item', door, {'item': door})
    copy_loot_table('double_block', door, variables)
    copy_crafting_recipe('door', type + '/door', variables)
    add_to_item_and_block_tags('wooden_doors', '%s:%s' % (MODID, door))

    trapdoor = variables['block'] = type + '_trapdoor'
    copy_blockstate_and_models('trapdoor', trapdoor, variables, block_model_suffixes=['_bottom', '_open', '_top'],
                               item_model_suffix='_bottom')
    drop_itself(trapdoor, variables)
    copy_crafting_recipe('trapdoor', type + '/trapdoor', variables)
    add_to_item_and_block_tags('wooden_trapdoors', '%s:%s' % (MODID, trapdoor))

    # Chests and signs
    chest = variables['block'] = type + '_chest'
    copy_blockstate('simple_blockstate', chest, variables)
    copy_block_model('plank_particles', chest, {'type': type})
    copy_item_model('chest', chest, variables)
    copy_loot_table('named_tile_entity', chest, variables)
    copy_crafting_recipe('chest', type + '/chest', variables)
    copy_crafting_recipe('chest_from_logs', type + '/chest_from_logs', variables)
    add_to_block_tag('chests/wooden', '%s:%s' % (MODID, chest), namespace='forge')

    trapped_chest = type + '_trapped_chest'
    copy_blockstate('simple_blockstate', trapped_chest, variables)
    copy_block_model('plank_particles', trapped_chest, variables)
    copy_item_model('trapped_chest', trapped_chest, variables)
    copy_loot_table('named_tile_entity', trapped_chest, {'block': trapped_chest, 'condition': type})
    copy_crafting_recipe('trapped_chest', type + '/trapped_chest', variables)
    add_to_block_tag('chests/trapped', '%s:%s' % (MODID, trapped_chest), namespace='forge')

    sign = variables['block'] = type + '_sign'
    wall_sign = type + '_wall_sign'
    copy_blockstate('simple_blockstate', sign, variables)
    copy_blockstate('simple_blockstate', wall_sign, variables)
    copy_block_model('plank_particles', sign, variables)
    copy_item_model('item', sign, {'item': sign})
    copy_crafting_recipe('sign', '%s/sign' % type, variables)
    drop_itself(sign, variables)
    add_to_block_tag('standing_signs', '%s:%s' % (MODID, sign))
    add_to_block_tag('wall_signs', '%s:%s' % (MODID, wall_sign))

    # Other stuff
    bookshelf = variables['block'] = type + '_bookshelf'
    copy_blockstate('simple_blockstate', bookshelf, variables)
    copy_block_model('bookshelf', bookshelf, variables)
    copy_item_model('block', bookshelf, variables)
    copy_loot_table('bookshelf', bookshelf, variables)
    copy_crafting_recipe('bookshelf', 'compat/quark/%s/bookshelf' % type, variables)
    add_to_block_tag('bookshelves', '%s:%s' % (MODID, bookshelf), namespace='forge')

    ladder = variables['block'] = type + '_ladder'
    copy_blockstate('rotatable', ladder, variables)
    copy_block_model('ladder', ladder, variables)
    copy_item_model('flat_block', ladder, variables)
    drop_itself(ladder, variables)
    copy_crafting_recipe('ladder', 'compat/quark/%s/ladder' % type, variables)
    add_to_item_and_block_tags('ladders', '%s:%s' % (MODID, ladder), namespace='quark')
    add_to_block_tag('climbable', '%s:%s' % (MODID, ladder))

    boat = type + '_boat'
    copy_item_model('item', boat, {'item': boat})
    add_to_item_tag('boats', '%s:%s' % (MODID, boat))
    copy_crafting_recipe('boat', '%s/boat' % type, variables)
