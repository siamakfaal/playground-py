# Playground (Python)



## Development

### Install Bazelisk

We use Bazel as the build system for Playground. Rather than installing Bazel directly, install Bazelisk by following the instructions on the [Bazelisk GitHub page](https://github.com/bazelbuild/bazelisk).

### Running Examples
- Tic Tac Toe: `bazel run //src/tic_tac_toe`

### Format

Run `./format.sh` in the root of the project to apply Black and isort