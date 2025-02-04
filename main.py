from qiskit import QuantumCircuit, Aer, transpile, execute
from qiskit.circuit import Parameter
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_qubits = 2
num_steps = 100  # Trotter steps
time = 1.0  # Total time of evolution
delta_t = time / num_steps

# Define the observable (e.g., Z operator on the first qubit)
def measure_observable(counts, shots):
    observable_value = 0
    for state, count in counts.items():
        if state[-1] == '0':
            observable_value += count
        else:
            observable_value -= count
    return observable_value / shots

# Define the time evolution operator using Trotter-Suzuki approximation
def trotter_step(circuit, delta_t):
    circuit.rz(2 * np.pi * delta_t, 0)  # Simulate Z term
    circuit.cx(0, 1)
    circuit.rz(2 * np.pi * delta_t, 1)
    circuit.cx(0, 1)

# Quantum Monte Carlo Simulation
observable_results = []
shots = 1024

for i in range(50):  # Monte Carlo iterations
    qc = QuantumCircuit(num_qubits, num_qubits)

    # Initial state preparation (superposition state)
    qc.h(range(num_qubits))

    # Apply Trotterized time evolution
    for _ in range(num_steps):
        trotter_step(qc, delta_t)

    # Measurement
    qc.measure(range(num_qubits), range(num_qubits))

    # Execute the circuit
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    result = execute(compiled_circuit, simulator, shots=shots).result()
    counts = result.get_counts()

    # Measure observable
    observable_value = measure_observable(counts, shots)
    observable_results.append(observable_value)

# Analyze the results
mean_observable = np.mean(observable_results)
variance_observable = np.var(observable_results)

print(f"Estimated Observable Mean: {mean_observable}")
print(f"Estimated Observable Variance: {variance_observable}")

# Plotting results
plt.hist(observable_results, bins=10, edgecolor='black')
plt.title('Quantum Monte Carlo Estimation of Observable')
plt.xlabel('Observable Value')
plt.ylabel('Frequency')
plt.show()
