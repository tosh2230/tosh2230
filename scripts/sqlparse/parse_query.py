from sqlparse import parse, tokens
from sqlparse.sql import Statement, Identifier, IdentifierList, TokenList, Token


def check_token_type(token: Token, value=None, alias=None):
    identifier_list = None
    identifier = None
    identifier_value = None
    identifier_alias = None
    token_list = None

    if token.ttype in (
        tokens.Text.Whitespace,
        tokens.Text.Whitespace.Newline,
        tokens.Punctuation,
    ) or token.value in (value, alias):
        return
    elif isinstance(token, IdentifierList):
        identifier_list = token
        for identifier in identifier_list.get_identifiers():
            check_token_type(token=identifier)
    elif isinstance(token, Identifier):
        identifier = token
        identifier_value = identifier.value
        identifier_alias = identifier.get_alias()
        print(
            (
                f"Identifier:: "
                f"value: {identifier_value}, "
                f"parent_name: {identifier.get_parent_name()}, "
                f"real_name: {identifier.get_real_name()}, "
                f"alias: {identifier_alias}"
            )
        )
        # for token in identifier:
        #     check_token_type(
        #         token=token, value=identifier_value, alias=identifier_alias
        #     )
    elif isinstance(token, TokenList):
        token_list = token
        for token in token_list:
            check_token_type(token=token)
    else:
        print(f"Token:: value: {token.value}, type: {token.ttype}")


if __name__ == "__main__":
    query = """
    select
        t.a AS a_col,
        t.b AS b_col,
        COUNT(t.*),
    from
        test_table AS t
    where
        t.a = 0
        and t.b = "aaa"
    group by
        a_col,
        b_col
    order by
        a_col,
        b_col
    ;
    """.strip()

    with open(
        "../../../stairlight/tests/sql/query/google_bigquery_unnest_in_exists.sql"
    ) as f:
        query = f.read()

    parsed_statements: list[Statement] = parse(query)

    for parsed_statement in parsed_statements:
        for token in parsed_statement.tokens:
            check_token_type(token=token)
