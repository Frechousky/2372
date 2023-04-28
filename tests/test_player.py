import pytest

from graphics import PlayerSprite


@pytest.mark.parametrize("vy", [0, -10, 20])
def test_jump__if_available_jump__updates_player_vy(vy: int):
    tested = PlayerSprite(vy=vy, available_jumps=1)

    assert tested._available_jumps > 0

    before_aj = tested._available_jumps

    tested.jump()

    assert tested._available_jumps == before_aj - 1
    assert tested._vy < 0, "vy is negative so the player is moving up"


@pytest.mark.parametrize("vy", [0, -10, 20])
def test_jump__if_no_available_jump__does_nothing(vy: int):
    tested = PlayerSprite(vy=vy, available_jumps=0)

    assert tested._available_jumps == 0

    tested.jump()

    assert tested._vy == vy
    assert tested._available_jumps == 0


@pytest.mark.parametrize("vx", [0, -10, 20])
def test_move_right__updates_player_vx(vx):
    tested = PlayerSprite(vx=vx)

    assert tested._vx == vx

    tested.move_right()

    assert tested._vx > 0, "vx is positive so the player is moving right"


@pytest.mark.parametrize("vx", [0, -10, 20])
def test_move_left__updates_player_vx(vx):
    tested = PlayerSprite(vx=vx)

    assert tested._vx == vx

    tested.move_left()

    assert tested._vx < 0, "vx is negative so the player is moving left"


@pytest.mark.parametrize("vx", [0, -10, 20])
def test_stop_horizontal_movement__resets_vx(vx):
    tested = PlayerSprite(vx=vx)

    assert tested._vx == vx

    tested.stop_horizontal_movement()

    assert tested._vx == 0


@pytest.mark.parametrize(
    "x,y,vx,fps,expected_x",
    [
        (
            50,
            50,
            0,
            60.0,
            50,
        ),
        (
            50,
            50,
            -180,
            60.0,
            47,
        ),
        (
            50,
            50,
            222,
            60.0,
            53,
        ),
        (
            50,
            50,
            -120,
            0.0,
            -70,
        ),
    ],
    ids=[
        "when no vx, does not update position",
        "when negative vx, updates x position",
        "when positive vx, updates x position",
        "when 0 fps, does not raise ZeroDivisionError",
    ],
)
def update_vertical_pos(x: int, y: int, vx: int, fps: float, expected_x: int):
    tested = PlayerSprite(vx=vx)
    tested.rect.topleft = (x, y)

    tested.update_horizontal_pos(fps)

    assert tested.rect.topleft == (
        expected_x,
        y,
    )


@pytest.mark.parametrize(
    "x,y,vy,fps,expected_y",
    [
        (
            50,
            50,
            0,
            60.0,
            50,
        ),
        (
            50,
            50,
            -180,
            60.0,
            47,
        ),
        (
            50,
            50,
            222,
            60.0,
            53,
        ),
        (
            50,
            50,
            -120,
            0.0,
            -70,
        ),
    ],
    ids=[
        "when no vy does not update position",
        "when negative vy, updates y position",
        "when positive vy, updates y position",
        "when 0 fps, does not raise ZeroDivisionError",
    ],
)
def update_vertical_pos(x: int, y: int, vy: int, fps: float, expected_y: int):
    tested = PlayerSprite(vy=vy)
    tested.rect.topleft = (x, y)

    tested.update_vertical_pos(fps)

    assert tested.rect.topleft == (
        x,
        expected_y,
    )


@pytest.mark.parametrize("vy,fps", [(-50, 60.0), (72, 60.0), (0, 60.0), (-50, 0.0)])
def test_apply_gravity__increases_vy(vy: int, fps: float):
    tested = PlayerSprite(vy=vy)

    tested.apply_gravity(fps)

    assert tested._vy > vy


@pytest.mark.parametrize("available_jumps", [-1, 0, 5])
def test_hit_ground__resets_available_jumps(available_jumps: int):
    tested = PlayerSprite(available_jumps=available_jumps)

    tested.hit_ground()

    assert tested._available_jumps > 0


@pytest.mark.parametrize("vy", [0, -10, 20])
def test_hit_ground__resets_vy(vy: int):
    tested = PlayerSprite(vy=vy)

    tested.hit_ground()

    assert tested._vy == 0


@pytest.mark.parametrize("vy", [0, -10, 20])
def test_hit_roof__resets_vy(vy: int):
    tested = PlayerSprite(vy=vy)

    tested.hit_roof()

    assert tested._vy == 0
