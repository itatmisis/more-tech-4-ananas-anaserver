from sklearn.cluster import MiniBatchKMeans


class Trends:
    def __init__(self, n_clusters=5, text_data=None, id_data=None):
        self.n_clusters = n_clusters
        self.text_data = text_data
        self.id_data = id_data
        self.clusterer = MiniBatchKMeans(n_clusters=self.n_clusters).fit(self.text_data)
        self.labels = dict(zip(self.id_data, self.clusterer.labels_))

    def get_trends_label(self, emb):
        label = self.clusterer.predict(emb)
        return label

    def update_clusters(self, text_data, id_data):
        self.text_data = text_data
        self.id_data = id_data
        self.clusterer = MiniBatchKMeans(n_clusters=self.n_clusters).fit(self.text_data)
        self.labels = self.clusterer.labels_
