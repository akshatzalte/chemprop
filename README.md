# Implements `rigr` as a flag (Outdated version)

Use the RIGR featurizer in CLI by adding `--rigr` to train (and infer) your chemprop models. An example notebook can be found [here](./examples/rigr_notebooks). This implementation is **outdated** and currently not present in Chemprop v2. Now, RIGR is available as a choice of multi-hot atom featurization scheme. To use RIGR, add the `--multi-hot-atom-featurizer-mode RIGR` argument to your training or inference script. For notebook users, refer to our [example notebook](). 

See [rigr_home](https://github.com/akshatzalte/chemprop/tree/rigr_home) for more information.

**Reference:**  [RIGR: Resonance Invariant Graph Representation for Molecular Property Prediction]()
