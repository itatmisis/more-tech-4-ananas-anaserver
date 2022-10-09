import ananews

best_classifier = "best_classifier.joblib"
best_trunc_svd = "best_trunc_svd.joblib"
bert_model = ananews.nlp.BertWrapper()
summary_writer = ananews.nlp.SummarizationWrapper()

best_pipeline = ananews.pipelines.ItemPipeline(
    classifier=best_classifier, trunc_svd=best_trunc_svd, nlp_model=bert_model
)


async def get_news_embedding(news_text: str) -> list:
    news_emb = best_pipeline.get_embedding(news_text)
    news_emb_list = news_emb.tolist()
    return news_emb_list


async def get_news_summary(news_text: str) -> str:
    news_summary = summary_writer.get_summary(news_text)
    return news_summary
