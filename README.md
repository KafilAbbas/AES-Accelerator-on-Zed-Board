# AES-128 Encryption on FPGA

## Overview
The Advanced Encryption Standard (AES), standardized by NIST in 2001, is a widely trusted encryption algorithm used in secure communications, finance, and government applications. Its strength and efficiency make it a top choice for protecting sensitive data against cryptographic attacks.

For this project, we implemented the AES-128 variant, which uses a 128-bit key, providing an ideal balance between security and speed. By processing fixed-size data blocks through multiple rounds of substitution, permutation, and transformation, AES-128 offers robust protection for a wide range of applications.

## Project Goals
1. **Implement AES-128 on an FPGA** - Utilize the parallel processing capabilities of an FPGA to optimize encryption speed and efficiency.
2. **Leverage Xilinx Zynq ZedBoard** - Use the FPGA resources of the Zynq ZedBoard for high-speed encryption.
3. **Optimize Data Flow** - Integrate FPGA’s internal Block RAM (BRAM) to streamline data processing and minimize communication delays.

## Implementation Details

### AES-128 Encryption
AES-128 uses a 128-bit key to encrypt data, following these key steps:
- **Substitution** - Byte substitution using an S-box.
- **Permutation** - Shuffling data to prevent patterns.
- **Transformation** - Mixing columns and adding the encryption key to achieve cryptographic strength.

By employing multiple rounds of these transformations, AES-128 ensures that encrypted data is highly secure and resistant to various cryptographic attacks.

### FPGA Architecture
FPGAs are ideal for encryption tasks because they allow parallel processing, which significantly increases speed compared to traditional processors that execute tasks sequentially. For this project:
- **Five AES-128 Modules** - We implemented five encryption modules on the FPGA, each capable of working on a different data block independently and in parallel. This setup reduces overall processing time and maximizes efficiency.
- **Internal Block RAM (BRAM)** - The FPGA’s internal BRAM allowed for seamless data flow between modules, minimizing the delays associated with external communication and ensuring that data encryption could proceed without interruption.

### Platform
- **FPGA Board**: Xilinx Zynq ZedBoard
- **Encryption Algorithm**: AES-128
- **Key Length**: 128 bits
- **Data Block Size**: 128 bits

## Results and Benefits
- **Enhanced Speed**: By fully utilizing the parallel architecture of the FPGA, the AES-128 encryption modules achieved high-speed encryption of multiple data blocks simultaneously.
- **Efficient Resource Utilization**: Using BRAM eliminated data transfer bottlenecks, allowing the FPGA to maintain high processing speeds.
- **Scalability**: The setup can be scaled to add more encryption modules if additional processing power is needed, making it a flexible solution for a variety of encryption needs.

## Conclusion
Our AES-128 implementation on the Xilinx Zynq ZedBoard demonstrates how FPGAs can deliver high-performance, flexible solutions for data security applications. By harnessing the FPGA’s parallel processing capabilities, this setup provides a powerful alternative to traditional encryption methods, supporting efficient and secure data protection across diverse applications.

## Future Work
1. **Explore AES Variants**: Testing other AES variants (such as AES-192 and AES-256) for enhanced security.
2. **Performance Optimization**: Fine-tuning the system to maximize speed without compromising resource efficiency.
3. **Security Enhancements**: Adding additional layers of security or integrating this FPGA setup with other cryptographic protocols.

---

## References
- NIST, "Advanced Encryption Standard (AES)," FIPS PUB 197, 2001.
- Xilinx Zynq ZedBoard documentation for FPGA-specific resources and BRAM utilization.

---

**Author**: Kushagra Singh
