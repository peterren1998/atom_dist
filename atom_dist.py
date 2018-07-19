import math
import subprocess
import sys

catdcd_path = "/Users/peterren/Desktop/Research/catdcd/MACOSXX86/bin/catdcd4.0/catdcd"
dcd_file = sys.argv[1]
pdb_file = sys.argv[2]
index_file = sys.argv[3]
atom_num_1 = sys.argv[4]
atom_num_2 = sys.argv[5]
print(dcd_file)
print(pdb_file)
print(index_file)
print(atom_num_1)
print(atom_num_2)

content = subprocess.Popen([catdcd_path, "-num", dcd_file], stdout=subprocess.PIPE)
content = content.stdout.readlines()
num_frames = int(content[7][14:])
print(num_frames)

distance_over_time = []
distance_file = dcd_file[:-4] + "_" + atom_num_1 + "_" + atom_num_2 + ".dist"
print(distance_file)

for frame_temp in range(num_frames):
    frame = frame_temp+1
    print("Frame: " + str(frame))
    frame_file = pdb_file[:-4] + "_frame_" + str(frame) + ".pdb"

    subprocess.call([catdcd_path, "-o", frame_file, "-otype", "pdb", "-s", pdb_file, "-i", index_file, "-first", str(frame), "-last", str(frame), dcd_file])

    with open(frame_file) as f:
        atoms = f.readlines()

    atom_1_line = atoms[int(atom_num_1)]
    atom_2_line = atoms[int(atom_num_2)]

    # atom_1_attributes = atom_1_line.split()
    # atom_2_attributes = atom_2_line.split()

    # a1x = float(atom_1_attributes[6])
    # a1y = float(atom_1_attributes[7])
    # a1z = float(atom_1_attributes[8])
    # a2x = float(atom_2_attributes[6])
    # a2y = float(atom_2_attributes[7])
    # a2z = float(atom_2_attributes[8])

    a1x = float(atom_1_line[26:38])
    a1y = float(atom_1_line[38:46])
    a1z = float(atom_1_line[46:54])
    a2x = float(atom_2_line[26:38])
    a2y = float(atom_2_line[38:46])
    a2z = float(atom_2_line[46:54])
    print("a1x: " + str(a1x))
    print("a1y: " + str(a1y))
    print("a1z: " + str(a1z))
    print("a2x: " + str(a2x))
    print("a2y: " + str(a2y))
    print("a2z: " + str(a2z))

    r2 = (a1x - a2x)**2 + (a1y - a2y)**2 + (a1z - a2z)**2
    r = math.sqrt(r2)
    print(r)
    distance_over_time.append(r)

    with open(distance_file, "a+") as f:
        f.write(str(r) + "\n")

    subprocess.call(["rm", frame_file])

print(distance_over_time)
