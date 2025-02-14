# OpenAI Swarm Examples

This repository contains example implementations for using OpenAI Swarm with Robot Framework.

## Overview

This project demonstrates how to integrate OpenAI Swarm with Robot Framework for automated testing and orchestration. It includes:

- **openai_assistants_functions.py**: A Python module providing assistant-based functionality.
- **rf_swarm_orch.py**: A script to orchestrate OpenAI Swarm with Robot Framework.
- **test_results.csv**: Sample test results generated from execution.

## Prerequisites

To run these examples, ensure you have:

- Python 3.8+
- Robot Framework installed
```sh
  pip install robotframework
```
- OpenAI API credentials
```
export OPEN_AI_KEY=...
```
- Swarm dependencies installed

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/openai-swarm-examples.git
   cd openai-swarm-examples
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the OpenAI Swarm orchestration script:
```sh
python rf_swarm_orch.py
```

Modify the `openai_assistants_functions.py` to customize the assistant’s behavior.

## Example Test Execution

To execute test cases with Robot Framework:
```sh
robot tests/
```
Test results will be stored in `test_results.csv`.

## Resources

- OpenAI Swarm GitHub: [OpenAI Swarm](https://github.com/openai/swarm)
- Robot Framework Documentation: [Robot Framework](https://robotframework.org/)

## License

This project is licensed under the MIT License.