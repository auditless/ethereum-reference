"""Shared fixtures for doctests."""
import pytest
from typing import List
from collections import OrderedDict
import logging

from web3 import Web3, EthereumTesterProvider
import vyper
from solc import compile_files, compile_source


@pytest.fixture(autouse=True)
def web3(doctest_namespace):
    doctest_namespace["web3"] = Web3(EthereumTesterProvider())


def check_compiles_s(web3: Web3, contract_code: str):
    """Check if a Solidity file compiles without running a contract."""
    _ = compile_contracts_s(contract_code)


def check_compiles_v(web3: Web3, contract_code: str):
    """Check if a Vyper file compiles without running a contract."""
    _ = compile_contracts_v(contract_code)


def check_contract_v(web3: Web3, contract_code: str):
    """Verify if a given contract compiles in vyper"""
    # Compile the code
    compiled = compile_specific_vyper_contract(contract_code)

    # Deploy
    _test_compiled_snippet(web3, compiled)

    # At this point if there hasn't been an exception, the run is a success


def check_contract_s(web3: Web3, contract_code: str):
    """Verify if a given contract compiles in solidity"""
    # Compile the code
    compiled = compile_single_contract(contract_code)

    # Deploy
    _test_compiled_snippet(web3, compiled)

    # At this point if there hasn't been an exception, the run is a success


def check_named_contract_s(web3: Web3, contract_code: str, name: str):
    """Verify if the given named contract compiles in solidity"""
    # Compile the code
    compiled = compile_named_contract(contract_code, name)

    # Deploy
    _test_compiled_snippet(web3, compiled)

    # At this point if there hasn't been an exception, the run is a success


def check_local_s(web3: Web3, snippet: str):
    """Verify if piece of code compiles if placed in a
    constructor function of an empty contract of solidity code"""

    # Build the code using a template
    lines = snippet.split("\n")
    indented_snippet = ("\n" + " " * 8).join(lines)
    code = f"""contract DeployOnly {{
    constructor() public {{
        {indented_snippet}
    }}
}}
"""

    check_contract_s(web3, code)


def check_local_v(web3: Web3, snippet: str):
    """Verify if piece of code compiles if placed in a
    constructor function of an empty contract of vyper code"""

    # Build the code using a template
    lines = snippet.split("\n")
    indented_snippet = ("\n" + " " * 4).join(lines)
    code = f"""
@public
def __init__():
    {indented_snippet}
"""

    # Compile the code
    compiled = compile_specific_vyper_contract(code)

    # Deploy
    _test_compiled_snippet(web3, compiled)

    # At this point if there hasn't been an exception, the run is a success


def check_global_s(web3: Web3, snippet: str):
    """Verify if piece of code compiles if placed in an
    empty solidity contract body"""

    # Build the code using a template
    code = f"""contract DeployOnly {{
    {snippet}
    constructor() public {{
    }}
}}
"""

    check_contract_s(web3, code)


def check_global_constructor_s(
    web3: Web3, global_snippet: str, constructor_snippet: str
):
    """Verify if piece of code compiles if placed in an
    empty solidity contract body"""

    # Build the code using a template
    code = f"""contract DeployOnly {{
    {global_snippet}
    constructor() public {{
        {constructor_snippet}
    }}
}}
"""

    check_contract_s(web3, code)


def check_global_v(web3: Web3, snippet: str):
    """Verify if piece of code compiles if placed in an
    empty vyper contract body"""

    # Build the code using a template
    code = f"""
{snippet}

@public
def __init__():
    pass
"""

    # Compile the code
    compiled = compile_specific_vyper_contract(code)

    # Deploy
    _test_compiled_snippet(web3, compiled)

    # At this point if there hasn't been an exception, the run is a success


def check_s(web3: Web3, global_snippet: str, local_snippet: str):
    """Verify if piece of code compiles if placed in
    an empty contract of solidity code"""

    # Build the code using a template
    lines = local_snippet.split("\n")
    indented_snippet = ("\n" + " " * 8).join(lines)
    code = f"""contract DeployOnly {{
    {global_snippet}
    constructor() public {{
        {indented_snippet}
    }}
}}
"""

    check_contract_s(web3, code)


def check_v(web3: Web3, global_snippet: str, local_snippet: str):
    """Verify if piece of code compiles if placed in
    an empty contract of vyper code"""

    # Build the code using a template
    lines = local_snippet.split("\n")
    indented_snippet = ("\n" + " " * 4).join(lines)
    code = f"""
{global_snippet}

@public
def __init__():
    {indented_snippet}
"""

    # Compile the code
    compiled = compile_specific_vyper_contract(code)

    # Deploy
    _test_compiled_snippet(web3, compiled)

    # At this point if there hasn't been an exception, the run is a success


def _test_compiled_snippet(web3, compiled):
    bytecode = compiled["bin"]
    abi = compiled["abi"]
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)


def compile_contracts_s(source: str, **compiler_kwargs):
    """Compile Solidity source code."""
    return compile_source(source, **compiler_kwargs)


def compile_contracts_v(source: str, **compiler_kwargs):
    """Compile Vyper source code."""
    return compile_specific_vyper_contract(source)


def compile_single_contract(source: str, **compiler_kwargs):
    """Compile Solidity source code containing a single contract."""
    # pylint: disable=fixme
    # TODO: Add vyper support
    compiled_all = compile_source(source, **compiler_kwargs)
    if len(list(compiled_all.keys())) > 1:
        raise Exception("Can only handle single contracts.")
    compiled = compiled_all[next(iter(compiled_all))]
    return compiled


def compile_named_contract(source: str, name: str, **compiler_kwargs):
    """Compile named contract in Solidity source code."""
    # pylint: disable=fixme
    # TODO: Add vyper support
    compiled_all = compile_source(source, **compiler_kwargs)
    for key in compiled_all:
        if name in key:
            return compiled_all[key]
    raise Exception("Named contract not found in compiled artifacts.")


def compile_specific_contract(source: str, contract_name: str, **compiler_kwargs):
    """Compile Solidity source code with a specific contract."""
    compiled_all = compile_source(source, **compiler_kwargs)
    mod_contract_name = f"<stdin>:{contract_name}"
    if mod_contract_name not in compiled_all:
        raise Exception(f"Contract {contract_name} not in source")
    compiled = compiled_all[mod_contract_name]
    return compiled


def compile_single_contract_from_files(
    paths: List[str], contract: str, **compiler_kwargs
):
    """Compile a contract from Solidity or Vyper source files."""
    # Solidity compilation
    if str(paths[0]).endswith(".sol"):
        compiled_all = compile_files(paths, **compiler_kwargs)
        if contract is None:
            if len(list(compiled_all.keys())) > 1:
                raise Exception(
                    "Multiple contracts available, "
                    + "please select a single contract."
                )
            return compiled_all[next(iter(compiled_all))]
        for key in compiled_all:
            if key.endswith(f":{contract}"):
                return compiled_all[key]
        raise Exception(
            f"No contract with name {contract} found in {compiled_all.keys()}"
        )

    # Vyper compilation
    codes: OrderedDict = OrderedDict()
    for filename in paths:
        with open(filename, "r") as code_file:
            codes[filename] = code_file.read()
    return _compile_vyper_sources(codes, paths[0])


def _compile_vyper_sources(codes, name: str):
    """Compile a list of Vyper contracts using the first one."""
    output = vyper.compiler.compile_codes(
        codes,
        output_formats=["bytecode", "bytecode_runtime", "abi"],
        exc_handler=vyper_exc_handler,
    )
    contract = output[name]

    # Adapt Vyper output to solc conventional output
    result = {
        "bin-runtime": contract["bytecode_runtime"][2:],
        "bin": contract["bytecode"][2:],
        "abi": contract["abi"],
    }
    return result


def compile_specific_vyper_contract(source: str):
    """Compile Vyper contract from source str."""
    codes = OrderedDict()
    codes["main"] = source
    return _compile_vyper_sources(codes, "main")


def get_abi(compiled):
    """Retrieve ABI from compiled representation."""
    return compiled["abi"]


def get_bytecode(compiled):
    """Retrieve bytecode from compiled representation.

    Also removes the tail end containing any non-hex characters."""
    raw_bytecode = compiled["bin"]
    match = re.search("[^a-f0-9]", raw_bytecode)
    if match:
        return raw_bytecode[: match.start()]
    return raw_bytecode


def vyper_exc_handler(contract_name, exception):
    """Handle vyper compiler exception."""
    logging.error("Error compiling: %s", contract_name)
    raise exception
