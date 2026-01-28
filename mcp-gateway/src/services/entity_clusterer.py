from dataclasses import dataclass
from typing import Dict, List, Optional

from ..utils.logger import logger


@dataclass
class TrendCluster:
    primary_keyword: str
    related_keywords: List[str]
    cluster_score: float
    suggested_title: str
    combined_authority: float
    rationale: str


class EntityClusterer:
    """Clusters related trending keywords using entity relationships and similarity."""

    MIN_CLUSTER_SCORE = 0.6
    MAX_CLUSTER_SIZE = 4

    RELATION_WEIGHTS = {
        "same_category": 0.8,
        "common_entity": 0.7,
        "semantic_similarity": 0.6,
        "temporal_correlation": 0.5,
    }

    def __init__(self, knowledge_graph_service=None):
        self.kg_service = knowledge_graph_service
        self._entity_cache: Dict[str, dict] = {}

    async def cluster_trends(self, trends: List[dict], max_clusters: int = 5) -> List[TrendCluster]:
        if len(trends) < 2:
            return []

        entity_map = await self._fetch_entities_batch([t["keyword"] for t in trends])
        similarity_matrix = await self._build_similarity_matrix(trends, entity_map)
        clusters = self._hierarchical_clustering(trends, similarity_matrix)

        result_clusters = []
        for cluster_keywords in clusters[:max_clusters]:
            if len(cluster_keywords) < 2:
                continue
            cluster = self._create_cluster_suggestion(cluster_keywords, trends, entity_map, similarity_matrix)
            if cluster and cluster.cluster_score >= self.MIN_CLUSTER_SCORE:
                result_clusters.append(cluster)

        logger.info("Trend clustering completed", input_trends=len(trends), clusters_found=len(result_clusters))
        return result_clusters

    async def _fetch_entities_batch(self, keywords: List[str]) -> Dict[str, dict]:
        entity_map = {}
        for keyword in keywords:
            if keyword in self._entity_cache:
                entity_map[keyword] = self._entity_cache[keyword]
                continue
            try:
                entity_info = await self._fetch_entity_info(keyword)
                self._entity_cache[keyword] = entity_info
                entity_map[keyword] = entity_info
            except Exception as e:
                logger.warning("Failed to fetch entity", keyword=keyword, error=str(e))
                entity_map[keyword] = {"types": [], "related": []}
        return entity_map

    async def _fetch_entity_info(self, keyword: str) -> dict:
        return {"types": [], "related": [], "categories": [], "description": ""}

    async def _build_similarity_matrix(self, trends: List[dict], entity_map: Dict[str, dict]) -> Dict[tuple, float]:
        matrix = {}
        keywords = [t["keyword"] for t in trends]
        for i, kw1 in enumerate(keywords):
            for j, kw2 in enumerate(keywords):
                if i >= j:
                    continue
                similarity = await self._calculate_similarity(
                    kw1, kw2, entity_map.get(kw1, {}), entity_map.get(kw2, {})
                )
                matrix[(kw1, kw2)] = similarity
                matrix[(kw2, kw1)] = similarity
        return matrix

    async def _calculate_similarity(self, kw1: str, kw2: str, entity1: dict, entity2: dict) -> float:
        scores = []

        types1 = set(entity1.get("types", []))
        types2 = set(entity2.get("types", []))
        if types1 and types2:
            common_types = types1 & types2
            scores.append(("same_category", len(common_types) / max(len(types1), len(types2))))

        related1 = set(entity1.get("related", []))
        related2 = set(entity2.get("related", []))
        if related1 and related2:
            common_related = related1 & related2
            scores.append(("common_entity", len(common_related) / max(len(related1), len(related2))))

        words1 = set(kw1.lower().split())
        words2 = set(kw2.lower().split())
        if words1 and words2:
            word_overlap = len(words1 & words2) / max(len(words1), len(words2))
            scores.append(("semantic_similarity", word_overlap))

        if not scores:
            return 0.0

        total_weight = sum(self.RELATION_WEIGHTS.get(rel, 0.5) for rel, _ in scores)
        weighted_sum = sum(self.RELATION_WEIGHTS.get(rel, 0.5) * score for rel, score in scores)
        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _hierarchical_clustering(self, trends: List[dict], similarity_matrix: Dict[tuple, float]) -> List[List[str]]:
        keywords = [t["keyword"] for t in trends]
        clusters: List[List[str]] = [[kw] for kw in keywords]

        while len(clusters) > 1:
            best_score = -1.0
            best_pair = None
            for i, c1 in enumerate(clusters):
                for j, c2 in enumerate(clusters):
                    if i >= j:
                        continue
                    scores = []
                    for kw1 in c1:
                        for kw2 in c2:
                            if (kw1, kw2) in similarity_matrix:
                                scores.append(similarity_matrix[(kw1, kw2)])
                    if scores:
                        avg_score = sum(scores) / len(scores)
                        if avg_score > best_score:
                            best_score = avg_score
                            best_pair = (i, j)

            if best_score < self.MIN_CLUSTER_SCORE or best_pair is None:
                break

            i, j = best_pair
            new_cluster = clusters[i] + clusters[j]
            if len(new_cluster) <= self.MAX_CLUSTER_SIZE:
                clusters = [c for k, c in enumerate(clusters) if k not in (i, j)]
                clusters.append(new_cluster)
            else:
                break

        return [c for c in clusters if len(c) >= 2]

    def _create_cluster_suggestion(
        self,
        cluster_keywords: List[str],
        trends: List[dict],
        entity_map: Dict[str, dict],
        similarity_matrix: Dict[tuple, float],
    ) -> Optional[TrendCluster]:
        keyword_authority = {
            t["keyword"]: t.get("authority_score", 0) for t in trends if t["keyword"] in cluster_keywords
        }
        primary = max(cluster_keywords, key=lambda k: keyword_authority.get(k, 0))
        related = [k for k in cluster_keywords if k != primary]

        scores = []
        for i, kw1 in enumerate(cluster_keywords):
            for kw2 in cluster_keywords[i + 1 :]:
                if (kw1, kw2) in similarity_matrix:
                    scores.append(similarity_matrix[(kw1, kw2)])
        cluster_score = sum(scores) / len(scores) if scores else 0

        individual_authorities = [keyword_authority.get(k, 0) for k in cluster_keywords]
        combined_authority = min(100, max(individual_authorities) + sum(individual_authorities) * 0.1)

        if len(related) == 1:
            suggested_title = f"{primary}: How {related[0]} Changes Everything"
        else:
            suggested_title = f"{primary}: The Complete Guide ({', '.join(related[:2])})"

        strength = "strongly" if cluster_score > 0.8 else "moderately" if cluster_score > 0.6 else "weakly"
        rationale = (
            f"'{primary}' and {related} are {strength} correlated "
            f"(score: {cluster_score:.2f}). Combining these topics can increase "
            f"content authority and capture broader intent."
        )

        return TrendCluster(
            primary_keyword=primary,
            related_keywords=related,
            cluster_score=cluster_score,
            suggested_title=suggested_title,
            combined_authority=combined_authority,
            rationale=rationale,
        )
