from importlib import import_module

from django.db import connections

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import (
    ComplexFilterBackend,
    RestFrameworkFilterBackend,
)

from home.pagination import estimate_count, CountEstimatePagination


def split_basename(basename):
    """
    Splits a base name into schema and table names.
    """
    parts = basename.split(".")
    python_path_name = parts[0].lower()
    schema_name = parts[1].lower()
    table_name = parts[2].lower()

    return python_path_name, schema_name, table_name


class GenericViewSet(ReadOnlyModelViewSet):
    """
    """

    """
    A generic viewset which imports the necessary model, serializer, and permission
    for the endpoint.
    """
    index_sql = """
        SELECT DISTINCT a.attname AS index_column
        FROM pg_namespace n
        JOIN pg_class c ON n.oid = c.relnamespace
        JOIN pg_index i ON c.oid = i.indrelid
        JOIN pg_attribute a ON a.attnum = i.indkey[0]
            AND a.attrelid = c.oid
        WHERE n.nspname = %(table_schema)s
            AND c.relname = %(table_name)s
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        python_path_name, schema_name, table_name = split_basename(self.basename)
        api_model = getattr(
            import_module(f"{python_path_name}.models.{schema_name}"),
            f"{table_name}_model",
        )
        api_serializer = getattr(
            import_module(f"{python_path_name}.serializers.{schema_name}"),
            f"{table_name}_serializer",
        )
        api_permission = self.get_permission()

        # Grab the estimated count from the query plan; if its a large table,
        # use the count estimate for Pagination instead of an exact count.
        table_estimate_count = estimate_count(
            f"SELECT * FROM {schema_name}.{table_name}"
        )
        if table_estimate_count > 1000000:
            self.pagination_class = CountEstimatePagination

        self.queryset = api_model.objects.all()
        self.serializer_class = api_serializer

        # Only override permissions if provided.
        if api_permission:
            self.permission_classes = (api_permission,)

        self.filter_backends = (OrderingFilter, SearchFilter)
        self.ordering_fields = "__all__"
        self.search_fields = []

        # Add any columns indexed in the PostgreSQL database to be
        # filterable columns in the API
        index_columns = self.get_indexes(schema_name, table_name)

        # If any columns are indexed, add the appropriate filter backends
        # and set up a dictionary of filter fields
        if len(index_columns):
            self.filter_backends = self.filter_backends + (
                RestFrameworkFilterBackend,
                ComplexFilterBackend,
            )
            self.filter_fields = {}

        # Loop through all of the fields. If the field is indexed, add it
        # to the allowed filter columns. Additionally, if it is a text type,
        # add it to the searchable columns for the data browser.
        for field in api_model._meta.get_fields():
            if field.name in index_columns:
                field_type = field.get_internal_type()
                if field_type in ("CharField", "TextField"):
                    # Add column to searchable fields, with 'starts with' search ('^')
                    # See: http://www.django-rest-framework.org/api-guide/filtering/#searchfilter
                    self.search_fields.append(f"^{field.name}")

                    # Add column to filterable fields with all search options
                    self.filter_fields[field.name] = [
                        "exact",
                        "contains",
                        "startswith",
                        "endswith",
                    ]
                elif field_type in (
                    "IntegerField",
                    "BigIntegerField",
                    "DecimalField",
                    "FloatField",
                ):
                    # Add column to filterable fields with all search options
                    self.filter_fields[field.name] = ["exact", "lt", "lte", "gt", "gte"]
                elif field_type in ("DateField", "DateTimeField", "TimeField"):
                    # Add column to filterable fields with all search options
                    self.filter_fields[field.name] = ["exact", "lt", "lte", "gt", "gte"]

        self.search_fields = tuple(self.search_fields)

    def get_permission(self):
        return None

    def get_indexes(self, schema_name, table_name):
        """
        Return a list of unique columns that are part of an index on a table
        by providing schema name and table name.
        """

        cursor = connections["pgdata"].cursor()

        cursor.execute(
            self.index_sql, {"table_schema": schema_name, "table_name": table_name}
        )

        rows = cursor.fetchall()

        index_columns = []

        for row in rows:
            index_columns.append(row[0])

        return index_columns
