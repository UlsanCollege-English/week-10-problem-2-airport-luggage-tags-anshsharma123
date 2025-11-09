"""
HW02 — Airport Luggage Tags (Open Addressing with Delete)
Implement linear probing with EMPTY and DELETED markers.
"""

# Step 1: Create unique marker objects
EMPTY = object()
DELETED = object()


def _hash_basic(key):
    """Simple deterministic hash (sum of ordinals)."""
    return sum(ord(ch) for ch in key)


def make_table_open(m):
    """Return a table of length m filled with EMPTY markers."""
    return [EMPTY for _ in range(m)]


def _find_slot_for_insert(t, key):
    """
    Return index to insert/overwrite (may return DELETED slot).
    Return None if table full.
    """
    m = len(t)
    start = _hash_basic(key) % m
    first_deleted = None

    for step in range(m):
        i = (start + step) % m
        slot = t[i]

        if slot is EMPTY:
            # If we saw a deleted earlier, reuse it
            return first_deleted if first_deleted is not None else i
        elif slot is DELETED:
            # Remember first DELETED spot
            if first_deleted is None:
                first_deleted = i
        else:
            k, v = slot
            if k == key:
                return i  # Overwrite existing
    return None  # Table full


def _find_slot_for_search(t, key):
    """Return index where key is found; else None. DELETED does not stop search."""
    m = len(t)
    start = _hash_basic(key) % m

    for step in range(m):
        i = (start + step) % m
        slot = t[i]

        if slot is EMPTY:
            # Empty slot means key was never inserted
            return None
        elif slot is DELETED:
            continue  # Skip deleted, keep probing
        else:
            k, v = slot
            if k == key:
                return i
    return None


def put_open(t, key, value):
    """Insert or overwrite (key, value). Return True on success, False if table is full."""
    i = _find_slot_for_insert(t, key)
    if i is None:
        return False  # Table full
    slot = t[i]
    if slot is EMPTY or slot is DELETED:
        t[i] = (key, value)
    else:
        # Overwrite same key
        t[i] = (key, value)
    return True


def get_open(t, key):
    """Return value for key or None if not present."""
    i = _find_slot_for_search(t, key)
    if i is None:
        return None
    return t[i][1]


def delete_open(t, key):
    """Delete key if present. Return True if removed, else False."""
    i = _find_slot_for_search(t, key)
    if i is None:
        return False
    t[i] = DELETED
    return True


if __name__ == "__main__":
    # Optional manual check
    t = make_table_open(7)
    print("Initial:", t)
    put_open(t, "TAG1", "loaded")
    put_open(t, "TAG2", "checked")
    print("After inserts:", t)
    print("Get TAG1:", get_open(t, "TAG1"))
    delete_open(t, "TAG1")
    print("After delete:", t)
    put_open(t, "TAG3", "reused")
    print("After reinsert:", t)
