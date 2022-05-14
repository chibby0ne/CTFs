#!/usr/bin/env python

import hashlib

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"

bUsername_trial = b"GOUGH"
hUsername = hashlib.sha256(bUsername_trial).hexdigest()

dynamic_part =  hUsername[4] + hUsername[5] + hUsername[3] + hUsername[6] + hUsername[2] + hUsername[7] + hUsername[1] + hUsername[8]
assert len(dynamic_part) == len(key_part_dynamic1_trial)

key = key_part_static1_trial + dynamic_part + key_part_static2_trial
print(f"key: {key}")
