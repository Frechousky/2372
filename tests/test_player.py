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
    "x,y,vx,vy,fps,expected_x,expected_y",
    [
        (
            50,
            50,
            0,
            0,
            60.0,
            50,
            50,
        ),
        (
            50,
            50,
            -180,
            0,
            60.0,
            47,
            50,
        ),
        (
            50,
            50,
            222,
            0,
            60.0,
            53,
            50,
        ),
        (
            50,
            50,
            0,
            -666,
            60.0,
            50,
            38,
        ),
        (
            50,
            50,
            0,
            333,
            60.0,
            50,
            55,
        ),
        (
            50,
            50,
            -777,
            963,
            60.0,
            37,
            66,
        ),
        (
            50,
            50,
            -120,
            0,
            0.0,
            -70,
            50,
        ),
    ],
    ids=[
        "when no vx and no xy, does not update position",
        "when only negative vx, only updates x position",
        "when only positive vx, only updates x position",
        "when only negative vy, only updates y position",
        "when only positive vy, only updates y position",
        "when vx and vy, updates x and y position",
        "when 0 fps, does not raise ZeroDivisionError",
    ],
)
def test_update_position(
    x: int, y: int, vx: int, vy: int, fps: float, expected_x: int, expected_y: int
):
    tested = PlayerSprite(vx=vx, vy=vy)
    tested.rect.topleft = (x, y)

    tested.update_position(fps)

    assert tested.rect.topleft == (
        expected_x,
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
