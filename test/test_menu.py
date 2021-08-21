from source.ui.menu.menu_item import MenuItem

def test_can_instantiate_menu_item():
    assert MenuItem
    testitem = MenuItem('test')
    assert type(testitem) is MenuItem

def test_menu_item_string():
    assert str(MenuItem('test')) == 'test'