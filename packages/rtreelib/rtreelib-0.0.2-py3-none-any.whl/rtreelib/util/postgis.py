from typing import Union, Type

try:
    import psycopg2
    import psycopg2.pool
    from psycopg2.extras import DictCursor
except ImportError:
    raise RuntimeError("The following libraries are required to export R-trees to PostGIS: psycopg2")

pool = None


def init_pool(**kwargs):
    pool = psycopg2.pool.SimpleConnectionPool(1, 20, **kwargs)


def create_rtree_tables(conn=None, schema: str = 'public', srid: int = 0, datatype: Union[Type, str] = None,
                        **kwargs):
    try:
        conn = _get_conn(conn, **kwargs)
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(f'''
                CREATE TABLE temp2.rtree
(
  id SERIAL PRIMARY KEY
);

CREATE TABLE temp2.rtree_node
(
  id SERIAL PRIMARY KEY,
  rtree_id INT REFERENCES temp2.rtree (id) NOT NULL,
  level INT NOT NULL,
  bbox GEOMETRY(Polygon, 3857),
  parent_entry_id INT NOT NULL,
  leaf BOOLEAN NOT NULL
);

CREATE INDEX temp2.rtree_node_bbox_idx
  ON temp2.rtree_node
  USING gist (bbox);

CREATE TABLE temp2.rtree_entry
(
  id SERIAL PRIMARY KEY,
  parent_node_id INT REFERENCES temp2.rtree_node (id) NOT NULL,
  bbox GEOMETRY(Polygon, 3857) NOT NULL,
  leaf BOOLEAN NOT NULL,
  data INT
);

CREATE INDEX temp2.rtree_entry_bbox_idx
  ON temp2.rtree_entry
  USING gist (bbox);

ALTER TABLE temp2.rtree_node
  ADD CONSTRAINT rtree_node_parent_entry_id_fkey
  FOREIGN KEY (parent_entry_id)
  REFERENCES temp2.rtree_entry (id);
            ''')
    finally:
        if conn is not None:
            conn.close()


def _get_conn(conn=None, **kwargs):
    if conn is not None:
        return conn
    if pool is not None:
        return pool.getconn()
    if not kwargs:
        raise RuntimeError("Exporting R-tree to PostGIS requires either passing a connection object, initializing a "
                           "connection pool, or providing keyword arguments that can be used to initalize a "
                           "connection. Please check the documentation for details.")
    return psycopg2.connect(**kwargs)
