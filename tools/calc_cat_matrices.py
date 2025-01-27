"""Calculate CATs."""
import numpy as np

np.set_printoptions(precision=None, sign='-', floatmode='unique')


def xy_to_xyz(x, y):
    """Convert `xyY` to `xyz`."""

    return [x / y, 1, (1 - x - y) / y]


white_d65 = np.asfarray(xy_to_xyz(0.31270, 0.32900))
white_d50 = np.asfarray(xy_to_xyz(0.34570, 0.35850))


bradford_m = np.asfarray(
    [
        [0.8951000, 0.2664000, -0.1614000],
        [-0.7502000, 1.7135000, 0.0367000],
        [0.0389000, -0.0685000, 1.0296000]
    ]
)

von_kries_m = np.asfarray(
    [
        [0.4002400, 0.7076000, -0.0808100],
        [-0.2263000, 1.1653200, 0.0457000],
        [0.0000000, 0.0000000, 0.9182200]
    ]
)

xyz_scale_m = np.asfarray(
    [
        [1.0000000, 0.0000000, 0.0000000],
        [0.0000000, 1.0000000, 0.0000000],
        [0.0000000, 0.0000000, 1.0000000]
    ]
)

cat02_m = np.asfarray(
    [
        [0.7328000, 0.4296000, -0.1624000],
        [-0.7036000, 1.6975000, 0.0061000],
        [0.0030000, 0.0136000, 0.9834000]
    ]
)

cmccat97_m = np.asfarray(
    [
        [0.8951000, -0.7502000, 0.0389000],
        [0.2664000, 1.7135000, 0.0685000],
        [-0.1614000, 0.0367000, 1.0296000]
    ]
)

sharp_m = np.asfarray(
    [
        [1.2694000, -0.0988000, -0.1706000],
        [-0.8364000, 1.8006000, 0.0357000],
        [0.0297000, -0.0315000, 1.0018000]
    ]
)

cmccat2000_m = np.asfarray(
    [
        [0.7982000, 0.3389000, -0.1371000],
        [-0.5918000, 1.5512000, 0.0406000],
        [0.0008000, 0.0239000, 0.9753000]
    ]
)


def pre_calculate_cat(src_white, dest_white, m):
    """Calculate CAT."""

    mi = np.linalg.inv(m)
    src = np.dot(m, np.array(src_white))
    dest = np.dot(m, np.array(dest_white))
    m2 = np.diag(np.divide(dest, src))
    to_d50 = np.dot(mi, np.dot(m2, m))
    to_d65 = np.linalg.inv(to_d50)
    return to_d65, to_d50


if __name__ == '__main__':
    # Since we now calculate transform matrices on the fly and then cache them,
    # it isn't strictly necessary for us to pre-calculate D50 and D65 transform
    # matrices anymore. While we take a performance hit on the first calculation,
    # afterwards, we just retrieve the previously calculated matrices from the cache.
    # This allows us to check what the actual values we are using.

    to_d65, to_d50 = pre_calculate_cat(white_d65, white_d50, bradford_m)
    print('===== Bradford To D65 =====')
    print(to_d65)
    print('===== Bradford To D50 =====')
    print(to_d50)
