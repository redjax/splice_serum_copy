# Splice Serum Copy

Copy downloaded Splice Serum presets (`.fxp` files) from a source to a number of destinations (on the same host).

## Setup

- Copy `src/settings.toml` to `src/settings.local.toml`
- Edit `src/settings.local.toml`
  - If you are using multiple environments, pay attention to the `[dev]` and `[prod]` tags. Otherwise, set all values in the `[default]` section
  - Edit `src_dir`
    - Set a `name` and `path`
  - Edit `tar_dirs`
    - Follow the existing examples to create any number of local file paths for destination directories.
      - These target dirs should exist on the local machine.
- Install project with PDM
  - `pdm install`

## Usage

After copying `src/settings.toml` to `src/settings.local.toml` and editing the environment (see [setup section](#setup)), launch the app using one of the following methods

- Easy method:
  - Execute `pdm run start`
- Alternative method:
  - Set an environment (dev/prod)
    - **NOTE**: Make sure you have finished the [setup](#setup)
    - Linux:
      - `export ENV_FOR_DYNACONF=dev|prod`
    - Windows:
      - `$env:ENV_FOR_DYNACONF=dev|prod`
  - Execute the app
    - `cd src`
    - `pdm run python splice_serum_copy`
  