def get_retriever(vector_store, current_video=None):
    """
    Returns a retriever.

    If current_video is provided:
        Search only that video.

    If current_video is None:
        Search across all videos.
    """

    if current_video:
        return vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 10,
                "fetch_k": 50,
                "filter": {
                    "video_name": current_video
                }
            }
        )

    return vector_store.as_retriever(
        search_type="mmr",                      # i am using mmr as a retriever
        search_kwargs={
            "k": 20,
            "fetch_k": 70
        }
    )
