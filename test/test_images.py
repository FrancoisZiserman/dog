from images import Images


def test_images_load():
    images = Images("FiveImages", 200)
    assert images.black is not None
    assert len(images.image_keys) == 5
    assert len(images.images) == 5


def test_images_get_selection():
    images = Images("FiveImages", 200)
    assert images.get_selection("apple").image.name == "apple.png"


def test_images_criteria_apple():
    images = Images("FiveImages", 200, "apple")
    assert images.get_selection("apple").image.name == "apple.png"
    assert len(images.images) == 1


def test_images_criteria_o():
    images = Images("FiveImages", 200, "o")
    assert len(images.images) == 2


def test_images_criteria_on_all_picts():
    images = Images("all_picts", 200, "de|co")
    assert len(images.images) == 16
