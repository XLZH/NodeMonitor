from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "node" (
    "host" VARCHAR(31) NOT NULL  PRIMARY KEY /* the hostname of the node */,
    "cpu_5" VARCHAR(15) NOT NULL  /* average ratio of cpu in 5 seconds */,
    "cpu_60" VARCHAR(15) NOT NULL  /* average ratio of cpu in 60 seconds */,
    "mem_5" VARCHAR(15) NOT NULL  /* average ratio of memory in 5 seconds */,
    "mem_60" VARCHAR(15) NOT NULL  /* average ratio of memory in 60 seconds */,
    "net_rx_5" VARCHAR(31) NOT NULL  /* average receive bytes of network in 5 seconds */,
    "net_tx_5" VARCHAR(31) NOT NULL  /* average send bytes of network in 5 seconds */,
    "net_rx_60" VARCHAR(31) NOT NULL  /* average receive bytes of network in 60 seconds */,
    "net_tx_60" VARCHAR(31) NOT NULL  /* average send bytes of network in 60 seconds */,
    "update" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* time to update the node info */
) /* node status (memory, cpu and network) */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
