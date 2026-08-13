#!/usr/bin/env python3
"""Search necessary rooted-component profiles for a cutting-center path.

Deleting the center-path edges partitions the tree into rooted components of
sizes b_i.  If the off-path branches at root i have sizes forming a partition
of b_i-1, let q_i be the sum of their squared sizes.  Equal cutting numbers are
equivalent to

    prefix_i^2 + suffix_i^2 + q_i = K

for a common K.  This program searches these exact arithmetic conditions plus
the Harary--Ostrand inequalities 2*b_i <= prefix_i,suffix_i for internal roots.
They are necessary; a returned profile still needs an explicit tree and a
global cutting-number verification.
"""

import argparse


def square_partition_bits(limit):
    """bits[s] has bit q iff s has a partition with sum of squares q."""
    bits = [0] * (limit + 1)
    bits[0] = 1
    for part in range(1, limit + 1):
        shift = part * part
        for total in range(part, limit + 1):
            bits[total] |= bits[total - part] << shift
    return bits


def first_set_bit(x):
    return (x & -x).bit_length() - 1


def one_partition(total, square_sum, largest=None):
    """Return one nonincreasing partition with prescribed sum and square sum."""
    if total == 0:
        return () if square_sum == 0 else None
    if square_sum < total or square_sum > total * total:
        return None
    if largest is None or largest > total:
        largest = total
    for part in range(largest, 0, -1):
        got = one_partition(total - part, square_sum - part * part, part)
        if got is not None:
            return (part,) + got
    return None


def safe_partition_spectra(order, maximum_cut):
    """Spectra using rooted subtrees strictly below the center's maximum.

    A rooted subtree of size s is attached to an outside component of size
    order-s.  If its child subtree sizes partition s-1 and have square sum q,
    its root cutting number is

      (order-s)(s-1) + ((s-1)^2-q)/2.

    Child safety depends only on their sizes, so sizes can be admitted in
    increasing order in an unbounded partition DP.
    """
    spectra = [0] * (order + 1)
    spectra[0] = 1
    safe = [False] * (order + 1)
    witness = [None] * (order + 1)
    safe[1] = True
    witness[1] = ()
    # Add size 1 as an allowed child part.
    for total in range(1, order + 1):
        spectra[total] |= spectra[total - 1] << 1
    for size in range(2, order + 1):
        possibilities = spectra[size - 1]
        ok = False
        while possibilities:
            bit = possibilities & -possibilities
            q = bit.bit_length() - 1
            cut = (order - size) * (size - 1) + ((size - 1) ** 2 - q) // 2
            # Equality would put this off-path root in the cutting center and
            # therefore enlarge (or disconnect) the prescribed center path.
            if cut < maximum_cut:
                ok = True
                witness[size] = one_partition_allowed(size - 1, q, safe)
                break
            possibilities ^= bit
        if ok:
            safe[size] = True
            shift = size * size
            for total in range(size, order + 1):
                spectra[total] |= spectra[total - size] << shift
    return safe, spectra, witness


def globally_safe(profile, common_k, order):
    numerator = (order - 1) ** 2 - common_k
    if numerator < 0 or numerator % 2:
        return None
    maximum_cut = numerator // 2
    safe, spectra, witness = safe_partition_spectra(order, maximum_cut)
    branches = []
    left = 0
    for b in profile:
        right = order - left - b
        q = common_k - left * left - right * right
        if q < 0 or not ((spectra[b - 1] >> q) & 1):
            return None
        branches.append(one_partition_allowed(b - 1, q, safe))
        left += b
    return maximum_cut, tuple(branches), tuple(witness)


def one_partition_allowed(total, square_sum, allowed, largest=None):
    if total == 0:
        return () if square_sum == 0 else None
    if square_sum < total or square_sum > total * total:
        return None
    if largest is None or largest > total:
        largest = total
    for part in range(largest, 0, -1):
        if not allowed[part]:
            continue
        got = one_partition_allowed(total - part, square_sum - part * part,
                                    allowed, part)
        if got is not None:
            return (part,) + got
    return None


def profiles(center_size, order, spectra, stop_after=1):
    found = []

    def visit(prefix, common):
        used = sum(prefix)
        slots = center_size - len(prefix)
        if slots == 0:
            if used != order or prefix > prefix[::-1]:
                return
            while common:
                bit = common & -common
                common_k = bit.bit_length() - 1
                realization = globally_safe(prefix, common_k, order)
                if realization is not None:
                    maximum_cut, branches, witness = realization
                    found.append((tuple(prefix), common_k, maximum_cut, branches,
                                  witness))
                    break
                common ^= bit
            return
        # Positive component sizes and enough room for all remaining slots.
        maximum = order - used - (slots - 1)
        for b in range(1, maximum + 1):
            # Left half of the Harary--Ostrand lemma can be checked now for
            # every internal center vertex.
            index = len(prefix)
            if 0 < index < center_size - 1 and 2 * b > used:
                continue
            candidate = prefix + [b]
            # Once total order is fixed, the right half is also known.
            if 0 < index < center_size - 1:
                right = order - used - b
                if 2 * b > right:
                    continue
            right = order - used - b
            possible = spectra[b - 1] << (used * used + right * right)
            next_common = possible if common is None else common & possible
            if not next_common:
                continue
            visit(candidate, next_common)
            if len(found) >= stop_after:
                return

    visit([], None)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("center_size", type=int)
    parser.add_argument("--max-order", type=int, required=True)
    parser.add_argument("--min-order", type=int)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    lower = args.min_order or args.center_size
    spectra = square_partition_bits(args.max_order)
    for order in range(lower, args.max_order + 1):
        got = profiles(args.center_size, order, spectra, 10**9 if args.all else 1)
        if got:
            print("order", order, "profiles", len(got))
            for profile, common_k, maximum_cut, branches, witness in got[:20]:
                print("profile", profile, "K", common_k, "cut", maximum_cut,
                      "branches", branches)
            return
    print("no arithmetic profile through", args.max_order)


if __name__ == "__main__":
    main()
