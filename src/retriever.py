def get_retriever(vector_store, current_video):

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 20,
            "fetch_k": 20,
            "filter": {
                "video_name": current_video
            }
        }
    )