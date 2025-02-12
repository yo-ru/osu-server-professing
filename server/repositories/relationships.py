from typing import Any

from server import clients

READ_PARAMS = """
    account_id,
    target_id,
    relationship
"""


async def create(
    account_id: int,
    target_id: int,
    relationship: str,
) -> dict[str, Any]:
    _relationship = await clients.database.fetch_one(
        query=f"""
            INSERT INTO relationships (account_id, target_id, relationship)
            VALUES (:account_id, :target_id, :relationship)
            RETURNING {READ_PARAMS}
        """,
        values={
            "account_id": account_id,
            "target_id": target_id,
            "relationship": relationship,
        },
    )

    assert _relationship is not None
    return _relationship


async def fetch_all(
    account_id: int | None = None,
    relationship: str | None = None,
) -> list[dict[str, Any]]:
    relationships = await clients.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS}
            FROM relationships
            WHERE account_id = COALESCE(:account_id, account_id)
            AND relationship = COALESCE(:relationship, relationship)
        """,
        values={"account_id": account_id, "relationship": relationship},
    )
    return relationships


async def remove(
    account_id: int,
    target_id: int,
) -> dict[str, Any] | None:
    _relationship = await clients.database.fetch_one(
        query=f"""
            DELETE FROM relationships
            WHERE account_id = :account_id
            AND target_id = :target_id
            RETURNING {READ_PARAMS}
        """,
        values={
            "account_id": account_id,
            "target_id": target_id,
        },
    )
    return _relationship
