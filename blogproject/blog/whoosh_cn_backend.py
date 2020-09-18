from haystack.backends.whoosh_backend import (
    WhooshEngine,
    WhooshHtmlFormatter,
    WhooshSearchBackend,
)  # fixed
from haystack.constants import DJANGO_CT, DJANGO_ID, ID
from haystack.exceptions import SearchBackendError
from haystack.models import SearchResult
from haystack.utils.app_loading import haystack_get_model
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import BOOLEAN, DATETIME
from whoosh.fields import ID as WHOOSH_ID
from whoosh.fields import IDLIST, KEYWORD, NGRAM, NGRAMWORDS, NUMERIC, TEXT, Schema
from whoosh.highlight import ContextFragmenter
from whoosh.highlight import highlight as whoosh_highlight


class WhooshJiebaearchBackend(WhooshSearchBackend):
    def get_analyzer(self):
        return ChineseAnalyzer()

    def build_schema(self, fields):
        schema_fields = {
            ID: WHOOSH_ID(stored=True, unique=True),
            DJANGO_CT: WHOOSH_ID(stored=True),
            DJANGO_ID: WHOOSH_ID(stored=True),
        }
        # Grab the number of keys that are hard-coded into Haystack.
        # We'll use this to (possibly) fail slightly more gracefully later.
        initial_key_count = len(schema_fields)
        content_field_name = ""

        for field_name, field_class in fields.items():
            if field_class.is_multivalued:
                if field_class.indexed is False:
                    schema_fields[field_class.index_fieldname] = IDLIST(
                        stored=True, field_boost=field_class.boost
                    )
                else:
                    schema_fields[field_class.index_fieldname] = KEYWORD(
                        stored=True,
                        commas=True,
                        scorable=True,
                        field_boost=field_class.boost,
                    )
            elif field_class.field_type in ["date", "datetime"]:
                schema_fields[field_class.index_fieldname] = DATETIME(
                    stored=field_class.stored, sortable=True
                )
            elif field_class.field_type == "integer":
                schema_fields[field_class.index_fieldname] = NUMERIC(
                    stored=field_class.stored,
                    numtype=int,
                    field_boost=field_class.boost,
                )
            elif field_class.field_type == "float":
                schema_fields[field_class.index_fieldname] = NUMERIC(
                    stored=field_class.stored,
                    numtype=float,
                    field_boost=field_class.boost,
                )
            elif field_class.field_type == "boolean":
                # Field boost isn't supported on BOOLEAN as of 1.8.2.
                schema_fields[field_class.index_fieldname] = BOOLEAN(
                    stored=field_class.stored
                )
            elif field_class.field_type == "ngram":
                schema_fields[field_class.index_fieldname] = NGRAM(
                    minsize=3,
                    maxsize=15,
                    stored=field_class.stored,
                    field_boost=field_class.boost,
                )
            elif field_class.field_type == "edge_ngram":
                schema_fields[field_class.index_fieldname] = NGRAMWORDS(
                    minsize=2,
                    maxsize=15,
                    at="start",
                    stored=field_class.stored,
                    field_boost=field_class.boost,
                )
            else:
                schema_fields[field_class.index_fieldname] = TEXT(
                    stored=True,
                    analyzer=self.get_analyzer(),
                    field_boost=field_class.boost,
                    sortable=True,
                )

            if field_class.document is True:
                content_field_name = field_class.index_fieldname
                schema_fields[field_class.index_fieldname].spelling = True

        # Fail more gracefully than relying on the backend to die if no fields
        # are found.
        if len(schema_fields) <= initial_key_count:
            raise SearchBackendError(
                "No fields were found in any search_indexes. Please correct this before attempting to search."
            )

        return (content_field_name, Schema(**schema_fields))

    def _process_results(
        self,
        raw_page,
        highlight=False,
        query_string="",
        spelling_query=None,
        result_class=None,
    ):
        from haystack import connections

        results = []

        # It's important to grab the hits first before slicing. Otherwise, this
        # can cause pagination failures.
        hits = len(raw_page)

        if result_class is None:
            result_class = SearchResult

        facets = {}
        spelling_suggestion = None
        unified_index = connections[self.connection_alias].get_unified_index()
        indexed_models = unified_index.get_indexed_models()

        for doc_offset, raw_result in enumerate(raw_page):
            score = raw_page.score(doc_offset) or 0
            app_label, model_name = raw_result[DJANGO_CT].split(".")
            additional_fields = {}
            model = haystack_get_model(app_label, model_name)

            if model and model in indexed_models:
                for key, value in raw_result.items():
                    index = unified_index.get_index(model)
                    string_key = str(key)

                    if string_key in index.fields and hasattr(
                        index.fields[string_key], "convert"
                    ):
                        # Special-cased due to the nature of KEYWORD fields.
                        if index.fields[string_key].is_multivalued:
                            if value is None or len(value) == 0:
                                additional_fields[string_key] = []
                            else:
                                additional_fields[string_key] = value.split(",")
                        else:
                            additional_fields[string_key] = index.fields[
                                string_key
                            ].convert(value)
                    else:
                        additional_fields[string_key] = self._to_python(value)

                del additional_fields[DJANGO_CT]
                del additional_fields[DJANGO_ID]

                if highlight:
                    sa = self.get_analyzer()  # 替换为中文分词
                    formatter = WhooshHtmlFormatter("em")
                    terms = [token.text for token in sa(query_string)]

                    whoosh_result = whoosh_highlight(
                        additional_fields.get(self.content_field_name),
                        terms,
                        sa,
                        ContextFragmenter(),
                        formatter,
                    )
                    additional_fields["highlighted"] = {
                        self.content_field_name: [whoosh_result],
                    }

                result = result_class(
                    app_label,
                    model_name,
                    raw_result[DJANGO_ID],
                    score,
                    **additional_fields,
                )
                results.append(result)
            else:
                hits -= 1

        if self.include_spelling:
            if spelling_query:
                spelling_suggestion = self.create_spelling_suggestion(spelling_query)
            else:
                spelling_suggestion = self.create_spelling_suggestion(query_string)

        return {
            "results": results,
            "hits": hits,
            "facets": facets,
            "spelling_suggestion": spelling_suggestion,
        }


class WhooshJiebaEngine(WhooshEngine):
    backend = WhooshJiebaearchBackend
