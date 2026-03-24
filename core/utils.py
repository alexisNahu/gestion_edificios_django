from django.core.paginator import Paginator

def paginate_data(data, schema, page: int, page_size: int):
    """
    Recibe una lista de objetos de BD, los pagina y los transforma al esquema.
    """
    paginator = Paginator(data, page_size)
    pagina = paginator.get_page(page)

    return {
        "data": [schema.model_validate(e) for e in pagina.object_list],
        "pagination": {
            "paginas_totales": paginator.num_pages,
            "pagina_actual": page,
            "pagina_siguiente": pagina.next_page_number() if pagina.has_next() else None,
            "pagina_previa": pagina.previous_page_number() if pagina.has_previous() else None,
        }
    }

def clean_none_params(params: dict):
    """Limpia diccionarios de valores None para filtros de repo."""
    return {k: v for k, v in params.items() if v is not None}