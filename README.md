# Memory Hierarchy Simulation

## Introduction

Memory architecture plays a vital role in computer system design and development. One of the basic concepts in this field is the memory hierarchy, which includes registers, cache memory, main memory, and peripheral memory. This memory hierarchy simulation tool allows users to explore complex concepts such as cache replacement policies and investigate the impact of these policies on system performance.

## Project Description

This project simulates a memory hierarchy including multiple cache levels, main memory, and external memory. It supports various cache replacement policies and provides a user interface for configuring the memory hierarchy, running simulations, and viewing results.

## Features

1. **Memory Hierarchy Implementation**:
   - First Level Cache (L1)
   - Second Level Cache (L2)
   - Third Level Cache (L3)
   - Main Memory (RAM)
   - External Memory (e.g., Hard Disk, Flash Memory)

2. **Cache Replacement Policies**:
   - Least Recently Used (LRU)
   - First-In, First-Out (FIFO)
   - Random
   - Most Recently Used (MRU)
   - Second Chance
   - Least Frequently Used (LFU)
   - Least Frequently Recently Used (LFRU)

3. **Simulation of Memory Access**:
   - Supports sequential and random access patterns.
   - Allows manual, sequential, and random address inputs during runtime.

4. **Performance Analysis**:
   - Analyzes hit rates, miss rates, and access times.
   - Displays results in text and graphical formats.

5. **User Interface**:
   - Configurable parameters for the memory hierarchy.
   - Visualization of simulation results and cache contents.

## Setup

### Prerequisites

- Python 3.8+
- Tkinter (for the GUI)
- NumPy
- Pandas

### Directory Structure

- `src/`: Contains the source code
  - `memory_hierarchy.py`: Memory hierarchy implementation
  - `simulation.py`: Memory access simulation
  - `performance_analysis.py`: Performance analysis
  - `cache_policies.py`: Cache replacement policies
  - `ui.py`: User interface implementation

## Usage

1. Navigate to the `src` directory:

    ```sh
    cd src
    ```

2. Run the simulation tool:

    ```sh
    python ui.py
    ```

### User Interface

1. **Configure Simulation Parameters**:
   - Select the number of cache levels (1, 2, or 3).
   - Specify the size of each cache level.
   - Set the block size.
   - Choose a cache replacement policy.
   - Select an access pattern (Sequential or Random).
   - Specify the number of memory accesses.

2. **Run Simulation**:
   - Click the "Run Simulation" button to start the simulation.
   - A new window will display the results and cache contents.

3. **Access Addresses Manually**:
   - In the results window, choose "Manual" from the access mode combo box.
   - Enter the addresses and click the "Access" button to access them.

## Example

After setting up the simulation parameters and running the simulation, you will see a report with the following information:

- Total number of accesses
- Number of hits and misses
- Hit rate and miss rate
- Contents of each cache level

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas or improvements.

## License

This project is licensed under the MIT License.

---

## Author

Shahpoory

## Contact

For any questions or suggestions, please contact [Shahpoorymohammadhossein@gmail.com].

---

### Notes

- Make sure to test different configurations to see how they affect the simulation results.
- Handle exceptions gracefully and ensure that user inputs are validated to prevent errors during runtime.
