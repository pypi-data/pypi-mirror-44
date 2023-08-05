#! /usr/bin/env python

import numpy as np
import time


flopsPerInteraction = 30
SOFTENING_SQUARED = 0.01


def normalize (vector):
    dist = np.sqrt((vector * vector).sum())
    if dist > 1e-6:
        vector /= dist
    return dist


def randomize_bodies(pos, vel, cluster_scale, velocity_scale, n):
    np.random.seed(42)
    scale = cluster_scale
    vscale = scale * velocity_scale
    inner = 2.5 * scale
    outer = 4.0 * scale

    i = 0
    while i < n:
        point = np.random.random(3) / 2.
        length = normalize(point)
        if length > 1.:
            continue
        pos[i,:3] = point * ((inner + (outer - inner)) * np.random.random(3))
        pos[i,3] = 1.0
        axis = np.array((0., 0., 1.))
        normalize(axis)
        if (1 - ((point * axis).sum())) < 1e-6:
            axis[0] = point[1]
            axis[1] = point[0]
            normalize(axis)
        vv = np.cross(pos[i,:3], axis)
        vel[i] = vscale * vv
        print("%d: %s, %s" % (i, pos[i], vel[i]))
        i += 1


def check_correctness(pin, pout, v, f, dt, n, integrate_0, integrate_1):
    pin_ref = np.zeros_like(pin)
    pout_ref = np.zeros_like(pout)
    v_ref = np.zeros_like(v)
    f_ref = np.zeros_like(f)
    randomize_bodies(pin_ref, v_ref, 1.54, 8.0, n)
    integrate_0(pout_ref, pin_ref, v_ref, f_ref, dt, n)
    integrate_1(pout, pin, v, f, dt, n)

    errt = 0
    errmax = 0

    errs = np.fabs(pout_ref - pout).reshape(4 * n)
    errt = errs.sum()
    errmax = errs.max()

    print("Maximum error: %0.4f -- Total error: %0.4f" % (errmax, errt))


def body_body_interaction(force, pos_mass0, pos_mass1):
    r = pos_mass1[:3] - pos_mass0
    dist_sqr = (r * r).sum()
    dist_sqr += SOFTENING_SQUARED
    inv_dist = np.sqrt(dist_sqr)
    inv_dist_cube = inv_dist * inv_dist * inv_dist
    s = pos_mass1[3] * inv_dist_cube
    force += r * s


def integrate(position_out, position_in, velocity, force, delta_time, n):
    for i in range(n):
        p = position_in[i][:3]
        f = np.zeros(3)
        for j in range(i):
            body_body_interaction(f, p, position_in[j])
        inv_mass = position_in[i,3]
        v = velocity[i]
        v += f * inv_mass * delta_time
        p += v * delta_time
        position_out[i,:3] = p
        position_out[i,3] = inv_mass
        velocity[i] = v


def compute_perf_stats(milliseconds, iterations, n):
    interactionsPerSecond = float(n * n)
    interactionsPerSecond *= 1e-9 * iterations * 1000 / milliseconds
    return interactionsPerSecond * flopsPerInteraction;


def main(*args):
    n = 128
    iterations = 10
    dt = 0.01667

    if len(args) > 0:
        n = int(args[0])
        if len(args) > 1:
            iterations = int(args[1])

    pin = np.zeros((n, 4))
    pout = np.zeros((n, 4))
    v = np.zeros((n, 3))
    f = np.zeros((n, 3))

    randomize_bodies(pin, v, 1.54, 8.0, n)

    check_correctness(pin, pout, v, f, dt, n, integrate, integrate)

    time0 = time.time()
    for i in range(iterations):
        integrate(pout, pin, v, f, dt, n)
        t = pout
        pout = pin
        pin = t
    time1 = time.time()
    ms = (time1 - time0)*1000
    gf = compute_perf_stats(ms, iterations, n)

    print("%d n-body iterations" % iterations)
    print("%f ms: %f GFLOP/s" % (ms, gf))


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
