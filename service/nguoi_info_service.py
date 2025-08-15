from db import nguoi_repository

nguoi_repository = nguoi_repository.NguoiRepository()

def get_nguoi_info_service(
    query: str = "",
    page: int = 1,
    page_size: int = 15
):
    try:
        result = nguoi_repository.search_nguoi_paged(query, page, page_size)
        print(f"Found {result['total']} results for query: {query}, page: {page}")
        return {
            "nguoi_list": [n.to_dict() for n in result['nguoi_list']],
            "total": result['total']
        }
    except Exception as e:
        return {"error": str(e)}
