"""Create the reference."""

from yattag import Doc, indent
import sh

from .html import code, comment, empty, table_section
from .conftest import (
    check_local_v,
    check_local_s,
    check_global_s,
    check_global_v,
    check_s,
    check_v,
    check_contract_s,
    check_named_contract_s,
    check_global_constructor_s,
    check_compiles_s,
    check_compiles_v,
)
import solc


@code
def version_s():
    """
    >>> str(sh.solc("--version"))[50:65]
    'Version: 0.6.10'
    """
    return """$ solc --version
Version: 0.6.10"""


@code
def version_v():
    """
    >>> str(sh.vyper("--version"))[:8]
    '0.1.0b17'
    """
    return """$ vyper --version
0.1.0b17 (0.1.0 Beta 17)"""


@comment
def syntax_s():
    return "Solidity loosely borrows its syntax from Javascript and C"


@comment
def syntax_v():
    return "Vyper syntax is valid Python 3 syntax (but the opposite is not true)"


@code
def constant_s():
    r"""
    >>> check_global_s(web3, "uint constant TOTAL_SUPPLY = 10000000;")
    """
    return "uint constant TOTAL_SUPPLY = 10000000;"


@code
def constant_v():
    r"""
    >>> check_global_v(web3, "TOTAL_SUPPLY: constant(uint256) = 10000000")
    """
    return "TOTAL_SUPPLY: constant(uint256) = 10000000"


@code
def assignment_s():
    r"""
    >>> check_local_s(web3, "uint v; v = 1;")
    """
    return "v = 1;"


@code
def assignment_v():
    r"""
    >>> check_local_v(web3, "v: uint256= 0\nv = 1")
    """
    return "v = 1"


@code
def par_assignment_s():
    r"""
    >>> check_local_s(web3, "uint x; uint y; (x, y) = (0, 1);")
    """
    return "(x, y) = (0, 1);"


@code
def swap_s():
    r"""
    >>> check_local_s(web3, "uint x; uint y; (x, y) = (y, x);")
    """
    return "(x, y) = (y, x);"


@code
def compound_assignment_s():
    r"""
    >>> check_local_s(web3, "uint x = 0; x += 1;")
    """
    return "-=, *=, /=, %=, |=, &=, ^="


@code
def increment_decrement_s():
    r"""
    >>> check_local_s(web3, "uint i = 0; i++; ++i; i--; --i;")
    """
    return "i++, ++i, i--, --i"


@code
def increment_decrement_v():
    r"""
    >>> check_local_v(web3, "v: uint256= 0\nv += 1\nv -= 1")
    """
    return "i += 1, i -= 1"


@code
def set_default_s():
    r"""
    >>> check_local_s(web3, "uint v = 1; delete v;")
    """
    return "delete v // doesn't work with mappings"


@code
def set_default_v():
    r"""
    >>> check_local_v(web3, "v: uint256= 1\nclear(v)")
    """
    return "clear(v) # doesn't work with mappings"


@code
def null_test_s():
    r"""
    >>> check_local_s(web3, "uint v; bool b = v == 0;")
    """
    return "v == 0"


@code
def null_test_v():
    r"""
    >>> check_local_v(web3, "v: uint256= 0\nb: bool=v == 0")
    """
    return "v == 0"


@code
def true_false_s():
    r"""
    >>> check_local_s(web3, "bool x = true;")
    """
    return "true false"


@code
def true_false_v():
    r"""
    >>> check_local_v(web3, "x: bool= True")
    """
    return "True False"


@code
def conditional_expression_s():
    r"""
    >>> check_local_s(web3, "uint x; uint v = x > 0 ? x : -x;")
    """
    return "x > 0 ? x : -x"


@code
def interface_s():
    r"""
    >>> check_compiles_s(web3, "interface HelloWorld { function hello() external pure; }\ncontract Test {}")
    """
    return """interface HelloWorld {
    function hello() external pure;
    function world(int) external pure;
}"""


@code
def interface_v():
    r"""
    >>> check_compiles_v(web3, "contract HelloWorld:\n  def hello(): modifying\n\n@public\ndef test(addr: address):\n  HelloWorld(addr).hello()")
    """
    return """contract HelloWorld:
    def hello(): modifying
    def world(uint256): modifyingo"""


@code
def interface_type_s():
    r"""
    >>> check_compiles_s(web3, "interface HelloWorld { function hello() external pure; }\ncontract Test { bytes4 public hello_world = type(HelloWorld).interfaceId;}")
    """
    return """interface HelloWorldWithEvent {
    event Event();
    function hello() external pure;
    function world(int) external pure;
}

contract Test {
    bytes4 public hello_world_with_event = type(HelloWorldWithEvent).interfaceId;
}"""


@code
def min_max_v():
    r"""
    >>> check_local_v(web3, "x: uint256= 0\ny: uint256= 0\nz: uint256= max(x, y)")
    """
    return "max(x, y)"


@code
def binary_hex_literals_s():
    r"""
    >>> check_local_s(web3, "uint x = 0x52; string memory s = hex\"52\";")
    """
    return 'uint x = 0x52\nstring memory s = hex"52"'


@code
def binary_hex_literals_v():
    r"""
    >>> check_local_v(web3, "a: address= 0x14d465376c051Cbcd80Aa2d35Fd5df9910f80543")
    >>> check_local_v(web3, "b: bytes32= b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'")
    >>> check_local_v(web3, "c: bytes32= 0x1234567812345678123456781234567812345678123456781234567812345678")
    >>> check_local_v(web3, "b: bytes[1] = 0b00010001")
    """
    return (
        "a: address= 0x14d465376c051Cbcd80Aa2d35Fd5df9910f80543\n"
        + r"b: bytes32= b'\x01\x02\x03\x04\x05\x06... (32 bytes)"
        + "\n"
        + "c: bytes32= 0x010203040506... (32 bytes)"
        + "\n"
        + "d: bytes[1] = 0b00010001"
    )


@code
def string_type_s():
    r"""
    >>> check_local_s(web3, "string memory s = \"abc\";")
    """
    return "string"


@code
def string_type_v():
    r"""
    >>> check_local_v(web3, "s: string[100]= \"abc\"")
    """
    return "string[N]  # N is a fixed number"


@code
def bytes_type_s():
    return "bytes  // dynamic\nbytes1, bytes2, ..., bytes32  // packed\nbytes[N]  // N is a fixed number, unpacked"


@code
def bytes_type_v():
    r"""
    >>> check_local_v(web3, "example_bytes: bytes[100] = b\"\x01\x02\x03\"")
    """
    return "bytes32\nbytes[N]  # N is a fixed number"


@code
def string_literal_s():
    r"""
    >>> check_local_s(web3, "string memory s = \"don't \\\"no\\\"\";")
    >>> check_local_s(web3, "string memory s = 'don\"t \\'no\\'';")
    """
    return "\"don't \\\"no\\\"\"\n'don\"t \\'no\\''"


@code
def string_literal_v():
    r"""
    >>> check_local_v(web3, "s: string[100] = \"don't \\\"no\\\"\"")
    >>> check_local_v(web3, "s: string[100] = 'don\"t \\'no\\''")
    """
    return "\"don't \\\"no\\\"\"\n'don\"t \\'no\\''"


@code
def string_length_s():
    r"""
    >>> check_local_s(web3, "string memory s = \"abc\"; require(bytes(s).length == 3);")
    """
    return "bytes(s).length"


@code
def string_length_v():
    r"""
    >>> check_local_v(web3, "s: string[100] = \"abc\"\nassert len(s) == 3")
    """
    return "len(s)"


@code
def string_literal_escapes_s():
    r"""
    >>> check_local_s(web3, "string memory s = \"\\\\ \\\'\\\"\\b\\f\";")
    >>> check_local_s(web3, "string memory s = \"\\n \\r \\t \\v \\x01 \\u0001\";")
    """
    return r"""\<newline> (escapes an actual newline)
\\ (backslash)
\' (single quote)
\" (double quote)
\b (backspace)
\f (form feed)
\n (newline)
\r (carriage return)
\t (tab)
\v (vertical tab)
\xNN (hex escape)
\uNNNN (unicode escape)"""


@code
def string_literal_escapes_v():
    r"""
    >>> check_local_v(web3, "s: string[100]= \"\\\\ \\\'\\\"\\b\\f \\a\"")
    >>> check_local_v(web3, "s: string[100]= \"\\n \\r \\t \\v \\x01 \\u0001\"")
    >>> check_local_v(web3, "s: string[100]= \"\\u00010001\"")
    """
    return r"""\<newline> (escapes an actual newline)
\\ (backslash)
\' (single quote)
\" (double quote)
\a (bell)
\b (backspace)
\f (form feed)
\n (newline)
\r (carriage return)
\t (tab)
\v (vertical tab)
\ooo (octal escape)
\xNN (hex escape)
\uNNNN (unicode escape)
\uNNNNNNNN (unicode escape)"""


@code
def slice_s():
    r"""
    >>> check_contract_s(web3, '''
    ... contract Proxy {
    ...     function decode(bytes calldata _payload) external {
    ...         bytes4 sig = abi.decode(_payload[:4], (bytes4));
    ...     }
    ... }''')
    """
    return "abi.decode(_payload[:4], (bytes4))\n// array slices only implemented for calldata arrays"


@code
def slice_v():
    r"""
    >>> check_local_v(web3, "b: bytes[100] = b\"\x01\x02\x03\"\nassert len(slice(b, 0, 2)) == 2")
    """
    return "slice(x, _start, _len)"


@code
def string_comparison_s():
    r"""
    >>> check_local_s(web3, "require(keccak256(abi.encodePacked(\"abc\")) == keccak256(abi.encodePacked(\"abc\")));")
    """
    return "keccak256(abi.encodePacked(s1)) == keccak256(abi.encodePacked(s2))"


@code
def string_comparison_v():
    r"""
    >>> check_local_v(web3, "assert keccak256(\"abc\") == keccak256(\"abc\")")
    """
    return "keccak256(s1) == keccak256(s2)"


@code
def string_concatenation_s():
    r"""
    Read more here: https://solidity.readthedocs.io/en/v0.5.3/frequently-asked-questions.html?highlight=encodepacked#can-i-concatenate-two-strings
    >>> check_local_s(web3, "require(keccak256(abi.encodePacked(\"ab\", \"c\")) == keccak256(abi.encodePacked(\"abc\")));")
    """
    return "abi.encodePacked(s1, s2)"


@code
def string_concatenation_v():
    r"""
    >>> check_local_v(web3, "assert keccak256(concat(\"ab\", \"c\")) == keccak256(\"abc\")")
    """
    return "concat(s1, s2)"


@code
def array_literal_s():
    r"""
    >>> check_local_s(web3, "uint8[3] memory a = [1, 2, 3]; a[0] = 2; require(a.length == 3);")
    """
    return "[1, 2, 3]"


@code
def array_literal_v():
    r"""
    >>> check_local_v(web3, "a: uint256[3] = [1, 2, 3]\na[0] = 2")
    """
    return "[1, 2, 3]"


@code
def struct_s():
    r"""
    >>> check_s(web3, "struct Pair { uint x; uint y; }", "Pair memory pair = Pair(2, 3); require(pair.y > pair.x);")
    """
    return """struct Pair {
    uint x;
    uint y;
}  // Creating a struct

Pair memory pair = Pair(2, 3);  // Instantiating a struct variable
require(pair.y > pair.x);  // Accessing elements"""


@code
def struct_v():
    r"""
    >>> check_v(web3, "struct Pair:\n  x: uint256\n  y: uint256", "pair: Pair = Pair({x: 2, y: 3})\nassert pair.y > pair.x")
    """
    return """struct Pair:
    x: uint256
    y: uint256  # Creating a struct

pair: Pair = Pair({x: 2, y: 3})  # Instantiating a struct variable
assert pair.y > pair.x  # Accessing elements"""


@code
def mapping_delete_v():
    r"""
    >>> check_v(web3, "m: map(uint256, uint256)", "self.m[2] = 2\nclear(self.m[2])")
    """
    return "clear(m[2])"


@code
def immutable_s():
    r"""
    >>> check_global_constructor_s(web3, "uint immutable x;", "x = 1;")
    """
    return """uint immutable x; // have to be assigned in the constructor"""


@code
def define_f_s():
    r"""
    >>> check_global_s(web3, "function add2(uint x, uint y) public pure returns (uint) { return x + y; }")
    """
    return """function add2(uint x, uint y) public pure returns (uint) {
    return x + y;
}"""


@code
def function_argument_storage_location_s():
    r"""
    >>> check_global_s(web3, "function first(uint[] calldata x) public pure returns (uint) { return x[0]; }")
    >>> check_global_s(web3, "function first(uint[] memory x) public pure returns (uint) { return x[0]; }")
    """
    return """function first(uint[] calldata x) public pure returns (uint) {
    // this function doesn't copy x to memory
    return x[0];
}

function first(uint[] memory x) public pure returns (uint) {
    // this function first copies x to memory
    return x[0];
}"""


@code
def define_f_v():
    r"""
    >>> check_global_v(web3, "@public\ndef add2(x: uint256, y: uint256) -> uint256:\n  return x + y")
    """
    return """@public
def add2(x: uint256, y: uint256) -> uint256:
    return x + y"""


@code
def if_s():
    r"""
    >>> check_local_s(web3, "uint a = 3; if (a > 2) { a += 1; } else { a -= 1; }")
    """
    return """if (a > 2) {
    ...
else if (a == 0) {
    ...
} else {
    ...
}"""


@code
def if_v():
    r"""
    >>> check_local_v(web3, "a: uint256 = 3\nif a > 2:\n  a += 1\nelse:\n  a -= 1")
    """
    return """if a > 2:
    ...
elif a == 0:
    ...
else:
    ..."""


@code
def for_s():
    r"""
    >>> check_local_s(web3, "uint a = 3; for (uint i = 0; i < 3; i++) { a += 1; }")
    """
    return """for (uint i = 0; i < 3; i++) {
    ...
}"""


@code
def for_v():
    r"""
    >>> check_local_v(web3, "a: uint256 = 3\nfor i in range(3):\n  a += 1")
    """
    return """for i in range(3):
    ..."""


@code
def while_s():
    r"""
    >>> check_local_s(web3, "uint a = 3; while (a > 0) { a--; }")
    """
    return """while (a > 0) {
    ...
}"""


@code
def do_while_s():
    r"""
    >>> check_local_s(web3, "uint a = 3; do { a--; } while (a > 0);")
    """
    return """do {
    ...
} while (a > 0);"""


@code
def exceptions_s():
    r"""
    >>> check_named_contract_s(web3, '''
    ...     interface DataFeed { function getData(address token) external returns (uint value); }
    ...     contract FeedConsumer {
    ...         DataFeed feed;
    ...         uint errorCount;
    ...         function rate(address token) public returns (uint value, bool success) {
    ...             require(errorCount < 10);
    ...             try feed.getData(token) returns (uint v) {
    ...                 return (v, true);
    ...             } catch Error(string memory) {
    ...                 errorCount++;
    ...                 return (0, false);
    ...             } catch (bytes memory) {
    ...                 errorCount++;
    ...                 return (0, false);
    ...             }
    ...         }
    ...     }\n''', "FeedConsumer")
    """
    return """
interface DataFeed { function getData(address token) external returns (uint value); }

contract FeedConsumer {
    DataFeed feed;
    uint errorCount;
    function rate(address token) public returns (uint value, bool success) {
        // Permanently disable the mechanism if there are
        // more than 10 errors.
        require(errorCount < 10);
        try feed.getData(token) returns (uint v) {
            return (v, true);
        } catch Error(string memory /*reason*/) {
            // This is executed in case
            // revert was called inside getData
            // and a reason string was provided.
            errorCount++;
            return (0, false);
        } catch (bytes memory /*lowLevelData*/) {
            // This is executed in case revert() was used
            // or there was a failing assertion, division
            // by zero, etc. inside getData.
            errorCount++;
            return (0, false);
        }
    }
}"""


def render() -> str:
    """Render the final page."""
    doc, tag, text, line = Doc().ttl()
    trip = [doc, tag, text]
    quad = [doc, tag, text, line]

    # Final reference doc
    with tag("html"):
        with tag("body"):
            with tag("table"):
                with tag("tr"):
                    line("th", "Feature")
                    line("th", "Solidity")
                    line("th", "Vyper")
                with tag("tr"):
                    line("th", "Version")
                    version_s(*trip)
                    version_v(*trip)
                with tag("tr"):
                    line("th", "General notes on syntax")
                    syntax_s(*trip)
                    syntax_v(*trip)
                with tag("tr"):
                    line("th", "Block delimiters")
                    code(lambda: "{ }")(*trip)
                    code(lambda: ":  # Vyper uses Python's off-side rule")(*trip)
                with tag("tr"):
                    line("th", "Statement separator")
                    code(lambda: ";")(*trip)
                    code(lambda: "'\\n' and :")(*trip)
                with tag("tr"):
                    line("th", "End of line comment")
                    code(lambda: "// comment")(*trip)
                    code(lambda: "# comment")(*trip)
                with tag("tr"):
                    line("th", "Multiple line comment")
                    code(lambda: "/* multiple line\ncomment */")(*trip)
                    code(lambda: "# Multiple line\n# comment")(*trip)
                with tag("tr"):
                    line("th", "Constant")
                    constant_s(*trip)
                    constant_v(*trip)
                with tag("tr"):
                    line("th", "Assignment")
                    assignment_s(*trip)
                    assignment_v(*trip)
                with tag("tr"):
                    line("th", "Parallel assignment")
                    par_assignment_s(*trip)
                    comment(lambda: "Tuple to tuple assignment not supported")(*trip)
                with tag("tr"):
                    line("th", "Swap")
                    swap_s(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Compound assignment")
                    compound_assignment_s(*trip)
                    code(lambda: "-=, *=, /=, %=, |=, &=, ^=")(*trip)
                with tag("tr"):
                    line("th", "Increment and decrement")
                    increment_decrement_s(*trip)
                    increment_decrement_v(*trip)
                with tag("tr"):
                    line("th", "Null")
                    comment(
                        lambda: "null doesn't exist in Solidity but any unitialized variables take a default value represented by 0 in memory"
                    )(*trip)
                    comment(
                        lambda: "null doesn't exist in Vyper but any unitialized variables take a default value represented by 0 in memory"
                    )(*trip)
                with tag("tr"):
                    line("th", "Set variable to default value")
                    set_default_s(*trip)
                    set_default_v(*trip)
                with tag("tr"):
                    line("th", "Null test")
                    null_test_s(*trip)
                    null_test_v(*trip)
                with tag("tr"):
                    line("th", "Conditional expression")
                    conditional_expression_s(*trip)
                    comment(lambda: "Conditional expression not supported")(*trip)

                table_section("Contract lifecycle")(*quad)
                with tag("tr"):
                    line("th", "Contract creation")
                    code(lambda: "Contract c = new Contract(args);")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Contract creation with funding")
                    code(lambda: "Contract c = new Contract{value: amount}(args);")(
                        *trip
                    )
                    empty(*trip)
                with tag("tr"):
                    line("th", "Salted contract creation (CREATE2)")
                    code(lambda: "Contract c = new Contract{salt: salt}(args);")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Create forwarder contract")
                    empty(*trip)
                    code(
                        lambda: "contract: address = create_forwarder_to(other_contract, value)"
                    )(*trip)
                with tag("tr"):
                    line("th", "Selfdestruct (Avoid)")
                    code(lambda: "selfdestruct(refundAddr)")(*trip)
                    code(lambda: "selfdestruct(refund_addr)")(*trip)

                table_section("Interfaces")(*quad)
                with tag("tr"):
                    line("th", "Interfaces")
                    interface_s(*trip)
                    interface_v(*trip)
                with tag("tr"):
                    line("th", "Interface type")
                    interface_type_s(*trip)
                    empty(*trip)

                table_section("Operators")(*quad)
                with tag("tr"):
                    line("th", "True and false")
                    true_false_s(*trip)
                    true_false_v(*trip)
                with tag("tr"):
                    line("th", "Falsehoods")
                    code(lambda: "false")(*trip)
                    code(lambda: "False")(*trip)
                with tag("tr"):
                    line("th", "Logical operators")
                    code(lambda: "&& || !")(*trip)
                    code(lambda: "and or not")(*trip)
                with tag("tr"):
                    line("th", "Relational operators")
                    code(lambda: "== != < > <= =>")(*trip)
                    code(lambda: "== != < > <= =>")(*trip)
                with tag("tr"):
                    line("th", "Min and max")
                    empty(*trip)
                    min_max_v(*trip)
                with tag("tr"):
                    line("th", "Arithmetic operators")
                    code(lambda: "+ - * / % ** unary-")(*trip)
                    code(lambda: "+ - * / % ** unary-")(*trip)
                with tag("tr"):
                    line("th", "Integer division")
                    code(lambda: "/")(*trip)
                    code(lambda: "/")(*trip)
                with tag("tr"):
                    line("th", "Bit operators")
                    code(lambda: "<< >> & | ^ ~")(*trip)
                    code(lambda: "<< >> & | ^ ~")(*trip)
                with tag("tr"):
                    line("th", "Binary & hex literals")
                    binary_hex_literals_s(*trip)
                    binary_hex_literals_v(*trip)
                table_section("Data structures")(*quad)
                with tag("tr"):
                    line("th", "String type")
                    string_type_s(*trip)
                    string_type_v(*trip)
                with tag("tr"):
                    line("th", "Bytes type")
                    bytes_type_s(*trip)
                    bytes_type_v(*trip)
                with tag("tr"):
                    line("th", "String literal")
                    string_literal_s(*trip)
                    string_literal_v(*trip)
                with tag("tr"):
                    line("th", "String length")
                    string_length_s(*trip)
                    string_length_v(*trip)
                with tag("tr"):
                    line("th", "String literal escapes")
                    string_literal_escapes_s(*trip)
                    string_literal_escapes_v(*trip)
                with tag("tr"):
                    line("th", "Are strings mutable?")
                    comment(lambda: "Yes")(*trip)
                    comment(lambda: "Yes")(*trip)
                with tag("tr"):
                    line("th", "Slice")
                    slice_s(*trip)
                    slice_v(*trip)
                with tag("tr"):
                    line("th", "String comparison")
                    string_comparison_s(*trip)
                    string_comparison_v(*trip)
                with tag("tr"):
                    line("th", "String concatenation")
                    string_concatenation_s(*trip)
                    string_concatenation_v(*trip)
                with tag("tr"):
                    line("th", "Array literal")
                    array_literal_s(*trip)
                    array_literal_v(*trip)
                with tag("tr"):
                    line("th", "Length")
                    code(lambda: "a.length")(*trip)
                    code(lambda: "len(a)")(*trip)
                with tag("tr"):
                    line("th", "Empty test")
                    code(lambda: "a.length == 0")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Lookup")
                    code(lambda: "a[0]")(*trip)
                    code(lambda: "a[0]")(*trip)
                with tag("tr"):
                    line("th", "Update")
                    code(lambda: "a[0] = 1;")(*trip)
                    code(lambda: "a[0] = 1")(*trip)
                with tag("tr"):
                    line("th", "Out of bounds access")
                    comment(lambda: "Failing assertion")(*trip)
                    comment(lambda: "Failing assertion")(*trip)
                with tag("tr"):
                    line("th", "Add new element")
                    code(lambda: "a.push(3);  # Dynamic arrays")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Remove element")
                    code(lambda: "a.pop();  # Dynamic arrays")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Struct")
                    struct_s(*trip)
                    struct_v(*trip)
                with tag("tr"):
                    line("th", "Mapping size")
                    comment(lambda: "Impossible to know")(*trip)
                    comment(lambda: "Impossible to know")(*trip)
                with tag("tr"):
                    line("th", "Lookup")
                    code(lambda: "m[2]")(*trip)
                    code(lambda: "m[2]")(*trip)
                with tag("tr"):
                    line("th", "Update")
                    code(lambda: "m[2] = 1;")(*trip)
                    code(lambda: "m[2] = 1")(*trip)
                with tag("tr"):
                    line("th", "Missing key behaviour")
                    comment(
                        lambda: "A mapping has no concept of set keys, a mapping always refers to a hashed value that is the same for a given mapping and key"
                    )(*trip)
                    comment(
                        lambda: "A mapping has no concept of set keys, a mapping always refers to a hashed value that is the same for a given mapping and key"
                    )(*trip)
                with tag("tr"):
                    line("th", "Delete key")
                    code(lambda: "m[2] = 0;")(*trip)
                    mapping_delete_v(*trip)
                with tag("tr"):
                    line("th", "Immutable variables")
                    immutable_s(*trip)
                    empty(*trip)
                table_section("Functions")(*quad)
                with tag("tr"):
                    line("th", "Define function")
                    define_f_s(*trip)
                    define_f_v(*trip)
                with tag("tr"):
                    line("th", "Function argument storage location")
                    function_argument_storage_location_s(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Invoke function")
                    code(lambda: "add2(x, y)")(*trip)
                    code(lambda: "add2(x, y)")(*trip)
                with tag("tr"):
                    line("th", "External function calls")
                    code(lambda: "c.f{gas: 1000, value: 4 ether}()")(*trip)
                    code(
                        lambda: "c.f()\nraw_call(address, data, outsize, gas, value, is_delegate_call)"
                    )(*trip)
                table_section("Control flow")(*quad)
                with tag("tr"):
                    line("th", "If statement")
                    if_s(*trip)
                    if_v(*trip)
                with tag("tr"):
                    line("th", "For loop")
                    for_s(*trip)
                    for_v(*trip)
                with tag("tr"):
                    line("th", "While loop")
                    while_s(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Do-While loop")
                    do_while_s(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Return value")
                    code(lambda: "return x + y;")(*trip)
                    code(lambda: "return x + y")(*trip)
                with tag("tr"):
                    line("th", "Break")
                    code(lambda: "break;")(*trip)
                    code(lambda: "break")(*trip)
                with tag("tr"):
                    line("th", "Continue")
                    code(lambda: "continue;")(*trip)
                    code(lambda: "continue")(*trip)
                with tag("tr"):
                    line("th", "Assert")
                    code(lambda: "assert(x > y);")(*trip)
                    code(lambda: "assert x > y")(*trip)
                with tag("tr"):
                    line("th", "Require")
                    code(lambda: "require(x > y);")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Revert")
                    code(lambda: 'require(false, "revert reason")')(*trip)
                    code(lambda: 'raise "revert reason"')(*trip)
                with tag("tr"):
                    line("th", "Exception handling")
                    exceptions_s(*trip)
                    empty(*trip)
                table_section("Misc")(*quad)
                with tag("tr"):
                    line("th", "Comments")
                    code(
                        lambda: """NatSpec conventions:

/// @author Mary A. Botanist
/// @notice Calculate tree age in years, rounded up, for live trees
/// @dev The Alexandr N. Tetearing algorithm could increase precision
/// @param rings The number of rings from dendrochronological sample
/// @return age in years, rounded up for partial years"""
                    )(*trip)
                    code(
                        lambda: """def foo():
    \"\"\"
    @author Mary A. Botanist
    @notice Calculate tree age in years, rounded up, for live trees
    @dev The Alexandr N. Tetearing algorithm could increase precision
    @param rings The number of rings from dendrochronological sample
    @return age in years, rounded up for partial years
    \"\"\"
    ..."""
                    )(*trip)
                with tag("tr"):
                    line("th", "Payment with error on failure (Avoid for Solidity)")
                    code(lambda: "address.transfer()")(*trip)
                    code(lambda: "send(address, value)")(*trip)
                with tag("tr"):
                    line("th", "Payment with false on failure (Avoid for Solidity)")
                    code(lambda: "address.send()")(*trip)
                    empty(*trip)
                with tag("tr"):
                    line("th", "Payment with gas forwarding (WARNING)")
                    code(lambda: "address.call.value().gas()()")(*trip)
                    code(
                        lambda: "raw_call(address, data, outsize, gas, value, is_delegate_call)"
                    )(*trip)
                with tag("tr"):
                    line("th", "Event logging")
                    code(
                        lambda: """event Deposit(
    address indexed _from,
    bytes32 indexed _id,
    uint _value
);

emit Deposit(msg.sender, _id, msg.value);"""
                    )(*trip)
                    code(
                        lambda: """Deposit: event({_from: indexed(address), _id: indexed(bytes32), _value: uint256})

log.Deposit(msg.sender, _id, msg.value)"""
                    )(*trip)
                with tag("tr"):
                    line("th", "Units, global constants and type ranges")
                    code(
                        lambda: """1 ether
1 finney
1 szabo
1 wei
1 seconds
1 minutes
1 hours
1 days
1 weeks
1 years  // deprecated
type(uint).min
type(uint).max
type(int8).min
type(int8).max
..."""
                    )(*trip)
                    code(
                        lambda: """ZERO_ADDRESS
as_wei_value(1, "finney")
as_wei_value(1, "szabo")
as_wei_value(1, "wei")
as_wei_value(1, "babbage")
as_wei_value(1, "shannon")
EMPTY_BYTES32
MAX_INT128
MIN_INT128
MAX_DECIMAL
MIN_DECIMAL
MAX_UINT256
ZERO_WEI

time: timestamp
time_diff: timedelta

# define custom units
units: {
    cm: "centimeter",
    km: "kilometer"
}
a: int128(cm)
b: uint256(km)"""
                    )(*trip)
                with tag("tr"):
                    line("th", "Block and transaction properties")
                    code(
                        lambda: """blockhash(blockNumber)
block.coinbase
block.difficulty
block.gaslimit
block.number

block.timestamp
now  // alias for block.timestamp
gasleft()
msg.data
msg.gas
msg.sender
msg.sig
msg.value
tx.gasprice
tx.origin"""
                    )(*trip)
                    code(
                        lambda: """blockhash(blockNumber)
block.coinbase
block.difficulty

block.number
block.prevhash  # Same as blockhash(block.number - 1)
block.timestamp



msg.gas
msg.sender

msg.value

tx.origin"""
                    )(*trip)

    # Prettify the HTML
    unindented = doc.getvalue()
    return indent(unindented)


if __name__ == "__main__":
    print(render())
