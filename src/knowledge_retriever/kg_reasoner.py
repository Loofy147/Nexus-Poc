from typing import Dict, List
from neo4j import GraphDatabase

class KnowledgeGraphReasoner:
    """
    Performs reasoning over the knowledge graph to find multi-hop paths
    and answer complex questions.
    """

    def __init__(self, neo4j_driver: GraphDatabase.driver):
        self.driver = neo4j_driver
        print("Knowledge Graph Reasoner: Initialized.")

    def multi_hop_reasoning(self, entities: List[Dict], max_hops: int = 1) -> List[Dict]:
        """
        Performs a graph traversal to find connected entities.
        This initial version performs a 1-hop search.
        """
        print(f"Knowledge Graph Reasoner: Performing {max_hops}-hop reasoning for entities: {entities}")
        reasoning_chain = []
        entity_names = [entity['text'] for entity in entities]

        if not entity_names:
            return []

        with self.driver.session() as session:
            # This Cypher query finds all entities that are connected to the
            # starting set of entities within a specified number of hops.
            query = f"""
            MATCH (start:Entity)
            WHERE start.name IN $entity_names
            CALL apoc.path.expandConfig(start, {{
                relationshipFilter: "CONTAINS_ENTITY>",
                labelFilter: "/Entity",
                minLevel: 1,
                maxLevel: {max_hops * 2} // Since we hop from Chunk to Entity
            }}) YIELD path
            WITH path, relationships(path) AS rels, nodes(path) AS nodes
            RETURN
                nodes[0].name AS source,
                nodes[-1].name AS target,
                length(path) as distance
            ORDER BY distance
            LIMIT 20
            """

            # This is a simplified query for the PoC that finds direct connections
            simple_query = """
            MATCH (e1:Entity)-[:CONTAINS_ENTITY]-(c:Chunk)-[:CONTAINS_ENTITY]-(e2:Entity)
            WHERE e1.name IN $entity_names AND e1 <> e2
            RETURN e1.name AS source, "related_through_document" as relationship, e2.name AS target
            LIMIT 10
            """

            result = session.run(simple_query, entity_names=entity_names)

            for record in result:
                reasoning_chain.append({
                    "path": [record["source"], record["target"]],
                    "relations": [record["relationship"]],
                    "confidence": 0.9, # Placeholder confidence
                    "explanation": f"{record['source']} is related to {record['target']} through a shared document."
                })

        print(f"Knowledge Graph Reasoner: Found {len(reasoning_chain)} reasoning paths.")
        return reasoning_chain