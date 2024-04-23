# CONTRIBUTING

## Table of Contents
+ [Rules](#rules)
+ [Distribution and Packaging](#distribution-and-packaging)

## Rules
### Open Source Contribution
- Create a fork/branch to your contribution
- Open Pull Request to request to merge your updates
    - Please specify your contribution details in the following in your Pull Request
        + Title: `[category] : [summary]`
        - Body:
            ```
            Author Name: [your-name]
            Files Modified:
                - Files changed here
            Reason/Motivation:
            Summary:
                - Your changes here
            ```
+ Do not force merge directly to the main branch

## Distribution and Packaging
### Pre-Requisites
- (Optional) Create Virtual Environments for isolation testing/usage
    - Create the Virtual Environment container
        ```console
        python -m venv [virtual-environment-name]
        ```
    - Chroot and enter Virtual Environment
        - Linux
            ```bash
            . [virtual-environment-name]/bin/activate
            ```
        - Windows
            ```bash
            .\[virtual-environment-name]\Scripts\activate
            ```

- Change directory into project root directory
    ```bash
    cd [project-root-directory]
    ```

### Development and Testing
- Initial setup
    - Clone repository
        ```bash
        git clone https://github.com/Thanatisia/distinstall-python
        ```
    - Change directory into repository
        ```bash
        cd distinstall-python
        ```
    - Install python package dependencies
        ```bash
        python3 -m pip install -Ur requirements.txt
        ```

- Install framework using pip
    - Locally as development mode
        ```bash
        pip install .
        ```
    - (Optional) Uninstall package
        ```bash
        pip uninstall distinstall-python
        ```

### Building and Installation
- Local installation
    - Install locally as development
        - Clone repository
            ```bash
            git clone https://github.com/Thanatisia/distinstall-python
            ```
        - Change directory into repository
            ```bash
            cd distinstall-python
            ```
        - Install python package dependencies
            ```bash
            python3 -m pip install -Ur requirements.txt
            ```
        - Install python package
            ```bash
            python3 -m pip install .
            ```
        - (Optional) Uninstall package
            ```bash
            python3 -m pip uninstall distinstall-python
            ```
    - Using setuptools
        - Build/Compile static files
            - Explanation
                + This will compile/"package" the source files into an 'egg', .tar and wheel static files for sharing and installation
            ```console
            python setup.py build
            ```
        - Install built files methods
            1. Install built static files using setup.py with setuptools
                - Explanation
                    + This will install all dependencies, pre-requisites using setup.py and install the framework/package defined in setup.py
                ```console
                python setup.py install
                ```
            2. Install built static distribution files
                - tarball
                    ```console
                    pip install dist/[package-name]-[version-number].tar.gz
                    ```
                - wheel
                    ```console
                    pip install dist/[package-name]-[version-number]-[python-version].whl
                    ```
                - egg file
                    ```console
                    pip install dist/[package-name]-[version-number]-[python-version].egg
                    ```

- Remote installation (Recommended)
    - Install from PyPI (WIP)
        ```console
        pip install distinstall-python
        ```
    - Install git package from Git Remote Repository
        - Using pip
            ```console
            pip install git+https://github.com/Thanatisia/distinstall-python{@[branch-tag-name]}
            ```
        - Using requirements.txt
            - Create requirements.txt file
                ```
                # Python packages and dependencies

                ## Git Packages
                distinstall-python @ https://github.com/Thanatisia/distinstall-python{@[branch-tag-name]}
                ```
            - Install requirements.txt file
                ```bash
                pip install -Ur requirements.txt
                ```

## Resources

## References

## Remarks

