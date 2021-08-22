import pickle
import numpy as np

# The camera matrix

x = np.array([[977.4105363, 0.0,          710.85510632],
             [  0.0,        948.47764572, 382.80313717],
             [  0.0,        0.0,          1.0       ]])

# Serialize

payload = pickle.dumps(x)
print(payload)

with open('lifecam.cmat', 'bw') as f:
    f.write(payload)

# Deserialize

with open('lifecam.cmat', 'br') as f:
    y = pickle.loads(f.read())
    print(y)
